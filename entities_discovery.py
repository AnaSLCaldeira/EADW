from news_searcher import *
import nltk
from nltk.tree import *


def extract_entities(myTree):
    myPhrases = []
    if (myTree.label() == "NE"):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = extract_entities(child)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases


def get_entities(news):
    tags = []
    tagged_tokens = nltk.pos_tag(nltk.word_tokenize(news, language="portuguese"))
    named_entities = extract_entities(nltk.chunk.ne_chunk(tagged_tokens, binary=True))
    for entity in named_entities:
        phrase = []
        for i in range(len(entity)):    #ha entidades com mais do que uma palavra
            phrase.append(entity[i][0])
        tags.append(" ".join(phrase))
    return sorted(set(tags))


# CODIGO DE TESTE
#news = news_searcher("portugal")
#for entry in news:
#    entities = " ; ".join(get_entities(entry[0][0] + " " + entry[0][1])) + "\n"
#    print "Score: " + str(entry[1])
#    print "Titulo: " + entry[0][0]
#    print "Descricao: " + entry[0][1]
#    print "Link: " + entry[0][2]
#    print "Entidades: " + entities