__author__ = 'goncalograzina'

from Extraction import news_searcher
from discover import entity_discover
from discover import sentence_discover
import operator

# Procura 01/04/2015
#result = news_searcher("lotados bombeiros")
result = news_searcher("dispensava")
#result = news_searcher("Afonso lotados dispensava")
#result = news_searcher("protocolo")

ordered = sorted(result.items(), key=operator.itemgetter(0), reverse=True)


def discover(tree):
    for key in tree:
        tags = entity_discover(key[1][0], key[1][1])
        entidades = " ; ".join(tags)

        print "Score: "+ str(key[0])
        print "Titulo: "+ key[1][0]
        print "Descricao: "+ key[1][1]
        print "Link: "+ key[1][2]
        print "Entidades: "+ entidades
        print "\n"


def sentences(tree):
    for key in tree:
        tags = sentence_discover(key[1][0], key[1][1])

discover(ordered)
#sentences(ordered)