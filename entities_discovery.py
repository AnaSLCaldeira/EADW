from news_searcher import *
import nltk
from nltk.tree import *
from nltk.corpus import mac_morpho
from nltk.corpus import floresta

def parse_dbpedia():
	entities = []
	with open ("entities/DBpediaEntities-PT-0.1/locations.txt", 'r') as f:
		for line in f:
			entities.append(line.split("/")[4].replace("_", " ").replace("\n", ""))
	with open ("entities/DBpediaEntities-PT-0.1/organizations.txt", 'r') as f:
		for line in f:
			entities.append(line.split("/")[4].replace("_", " ").replace("\n", ""))
	with open ("entities/DBpediaEntities-PT-0.1/persons.txt", 'r') as f:
		for line in f:
			entities.append(line.split("/")[4].replace("_", " ").replace("\n", ""))
	with open ("entities/siglas.txt", 'r') as f:
		for line in f:
			entity = line.split(" - ")
			entities.append(entity[0])
			entities.append(entity[1])
	return entities


def get_entities(news):
	news_entities = []
	words = nltk.word_tokenize(news, language="portuguese")
	for index, word in enumerate(words):
		word = word.encode("UTF-8")
		if not word[0].isupper():
			continue
		else:
			if index < (len(words)-1) and words[index+1][0].isupper(): # verifica se existe outra palavra com letra maiuscula (muito provavelmente estao relacionadas) - estender para ver mais que 2? VER FORCAS ARMADAS
				if word + " " + words[index+1].encode("UTF-8") in dbpedia_entities:
					news_entities.append(word + " " + words[index+1].encode("UTF-8"))
			else:
				if word in dbpedia_entities: #verifica se a palavra e uma entidade
					news_entities.append(word)
	return sorted(set(news_entities))


def simplify_tag(t):
	if "+" in t:
		return t[t.index("+")+1:]
	else:
		return t


def train_tagger():
	#tagged_sents = floresta.tagged_sents(simplify_tags=True) nao funciona
	tagged_sents = floresta.tagged_sents()
	tagged_sents = [[(w,simplify_tag(t)) for (w,t) in sent] for sent in tagged_sents if sent]
	tagger0 = nltk.DefaultTagger('n')
	tagger1 = nltk.UnigramTagger(tagged_sents, backoff=tagger0)
	tagger2 = nltk.BigramTagger(tagged_sents, backoff=tagger1)
	return tagger2


#http://www.nltk.org/book/ch07.html
def extract_entities(chunked):
	entities = []
	if chunked.label() == "E":
		entity = str(chunked).split(" ")[1:]
		entity2 = []
		for item in entity:
			word = item.split("/")[0] #para retirar tag
			if word[0].isupper():
				entity2.append(word)
		if len(entity2) > 0:
			entities.append(" ".join(entity2))
	for child in chunked:
	    if (type(child) is Tree):
	        entities.extend(extract_entities(child))
	return sorted(set(entities))


def get_entities_nltk(news):
	words = nltk.word_tokenize(news, language="portuguese")
	tagged_words = tagger.tag(words)
	chunked = cp.parse(tagged_words)
	entities = extract_entities(chunked)
	return entities


def get_news_entities(ask):	
	news = news_searcher(ask)
	result = ""
	for entry in news:
		entities = " ; ".join(get_entities_nltk(entry[0][0] + ";" + entry[0][1]))
		result += "Score: " + str(entry[1]) + "\nTitulo: " + entry[0][0] + "\nDescricao: " + entry[0][1] + "\nLink: " + entry[0][2] + "\nEntidades: " + entities + "\n\n"
	return result


dbpedia_entities = parse_dbpedia()
tagger = train_tagger()
grammar = r"""E: {<n|prop>+}""" #agrupa nomes e nomes proprios
cp = nltk.RegexpParser(grammar)
print get_news_entities("Portugal")