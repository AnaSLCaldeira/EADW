import pickle
import unicodedata  # para retirar os acentos

import nltk
from nltk.tree import *
from nltk.corpus import mac_morpho

from news_searcher import *
from statistics import save_relations, update_entity_counter


def parse_dbpedia():
    entities = []
    with open("entities/DBpediaEntities-PT-0.1/locations.txt", 'r') as f:
        for line in f:
            entity = line.split("/")[4].replace("_", " ").replace("\n", "")
            entities.append(unicodedata.normalize('NFKD', entity.decode("UTF-8")).encode('ASCII', 'ignore'))
    with open("entities/DBpediaEntities-PT-0.1/organizations.txt", 'r') as f:
        for line in f:
            entity = line.split("/")[4].replace("_", " ").replace("\n", "")
            entities.append(unicodedata.normalize('NFKD', entity.decode("UTF-8")).encode('ASCII', 'ignore'))
    with open("entities/DBpediaEntities-PT-0.1/persons.txt", 'r') as f:
        for line in f:
            entity = line.split("/")[4].replace("_", " ").replace("\n", "")
            entities.append(unicodedata.normalize('NFKD', entity.decode("UTF-8")).encode('ASCII', 'ignore'))
    with open("entities/siglas.txt", 'r') as f:
        for line in f:
            entity = line.split(" - ")
            entities.append(entity[0])
            entities.append(unicodedata.normalize('NFKD', entity[1].decode("UTF-8")).encode('ASCII', 'ignore'))
    return entities


def parse_dbpedia_entities():
    parsed = []
    for entity in dbpedia_entities:
        split_entity = entity.split(" ")
        for i in range(len(split_entity)):
            parsed.append(split_entity[i])
    return parsed


def simplify_tag(t):
    if "+" in t:
        return t[t.index("+") + 1:]
    else:
        return t


def train_tagger():
    tagged_sents = mac_morpho.tagged_sents()
    tagged_sents = [[(w, simplify_tag(t)) for (w, t) in sent] for sent in tagged_sents if sent]
    tagger0 = nltk.DefaultTagger("N")
    tagger1 = nltk.UnigramTagger(tagged_sents, backoff=tagger0)
    tagger2 = nltk.BigramTagger(tagged_sents, backoff=tagger1)

    output = open("tagger.pkl", "wb")
    pickle.dump(tagger2, output, -1)
    output.close()

    return tagger2


def get_tagger():
    try:
        input = open("tagger.pkl", "rb")
        tagger = pickle.load(input)
        input.close()
    except Exception:
        tagger = train_tagger()
    return tagger


def entity_in_dbpedia(entity):
    if entity in dbpedia_entities:
        return True


def entity_in_partial_dbpedia(entity):
    if entity in dbpedia_partial_entities:
        return True


# para remover "Portas" quando existe essa e "Paulo Portas"; traz problemas com "Portugal" e "Vodafone Portugal"
def remove_duplicates(entities):
    result = list(set(entities))
    entities2 = entities[:]
    # print entities
    # for index, entity in enumerate(entities):
    #     for index2, entity2 in enumerate(entities2):
    #         if entity in entity2 and index != index2:  # verifica se a entidade e substring de outra
    #             print entity
    #             entities.remove(entity)
    #             entities2.remove(entity)
    return result


# http://www.nltk.org/book/ch07.html
def extract_entities(chunked):
    entities = []
    if chunked.label() == "E":
        chunked = str(chunked).split(" ")[1:]
        entity = []

        for item in chunked:
            if item != "":  #o tagger esta a por alguns com ""
                word = item.split("/")[0]  #para retirar tag
                if word != "":  #ha um caso em que no meio do texto aparece <em> </em> e provocava erro sem isto
                    if word[0].isupper() or word in special_words:
                        entity.append(word)

        if len(entity) > 0 and entity[0] in special_words:
            entity.remove(entity[0])
        if len(entity) > 0 and entity[-1] in special_words:
            entity.remove(entity[-1])
        if len(entity) > 0:
            entities.append(" ".join(entity))
    for child in chunked:
        if type(child) is Tree:
            entities.extend(extract_entities(child))
    return sorted(set(entities))


def get_entities_nltk(news):
    words = nltk.word_tokenize(news, language="portuguese")
    tagged_words = tagger.tag(words)
    for index in range(len(tagged_words)):
        if tagged_words[index][1] == "":  #o tagger devolve alguns tags a null e isso da erro no chunker
            aux = list(tagged_words[index])  #os tuplos sao imutaveis
            aux[1] = "N"
            tagged_words[index] = tuple(aux)
    chunked = cp.parse(tagged_words)
    entities = extract_entities(chunked)
    return entities


#se for usada, nao devolve algumas entidades de uma palavra, como "Passos". Se nao for, devolve muitas entidades que nao o sao, como "Resgate" e "TSU"
def remove_small_not_in_dbpedia(entities):
    entities_after_dbpedia = []
    for entity in entities:
        if len(entity.split(" ")) == 1:  #o tagger nao funciona bem para entidades de uma palavra
            if entity_in_dbpedia(entity):
                entities_after_dbpedia.append(entity)
        else:
            entities_after_dbpedia.append(entity)
    return entities_after_dbpedia


def get_news_entities(ask):
    news = news_searcher(ask)
    result = ""
    for entry in news:
        entities = get_entities_nltk(entry[0][0] + ";" + entry[0][1])
        entities = remove_small_not_in_dbpedia(entities)
        entities = remove_duplicates(entities)
        relations = get_news_relations(entry[0][0], entities)
        relations.extend(get_news_relations(entry[0][1], entities))
        save_relations(relations)
        update_entity_counter(entities)
        result += "Score: " + str(entry[1]) + "\nTitulo: " + entry[0][0] + "\nDescricao: " + entry[0][1] + "\nLink: " + \
                  entry[0][2] + "\nEntidades: " + " ; ".join(entities) + "\n\n"
    return result


def search_for_relation():
    return False


def check_is_entity(keywords):
    entities = remove_small_not_in_dbpedia(keywords)

    if not entities:
        return False
    else:
        return True


def get_news_relations(news, entities):

    relations = []

    if len(entities) == 1:
        return []

    # retrieves verbs from the title and description
    words = nltk.word_tokenize(news, language='portuguese')
    tagged = tagger.tag(words)
    verbs = []
    for item in tagged:
        if item[1] == "V":
            verbs.append(item[0])

    for i in range(0, len(entities)):
        if not (i+1) >= len(entities):
            start = entities[i]
            end = entities[i+1]

        for verb in verbs:
            x = re.findall(u'(.+){0}(.+){1}(.+){2}(.+)'.format(start, verb, end), news)
            if x:
                relation = [start, end, verb] # verb is sent to save in a file
                relations.append(relation)
    return relations


dbpedia_entities = parse_dbpedia()
dbpedia_partial_entities = parse_dbpedia_entities()
tagger = get_tagger()
grammar = "E: {<N|NPROP>+}"  #agrupa nomes e nomes proprios
cp = nltk.RegexpParser(grammar)
special_words = ["da", "das", "de", "do", "dos"]

#print get_news_entities("Jorge")

#nao encontra mediterraneo