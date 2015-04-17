__author__ = 'goncalograzina'

import feedparser
import nltk
import nltk.data

source_dn = feedparser.parse("http://feeds.dn.pt/DN-Portugal")
source_jn = feedparser.parse("http://feeds.jn.pt/JN-Pais")
source_dn['feed']['title']
source_jn['feed']['title']


from nltk.tree import *

# Tree manipulation

# Extract phrases from a parsed (chunked) tree
# Phrase = tag for the string phrase (sub-tree) to extract
# Returns: List of deep copies;  Recursive
def ExtractPhrases(myTree, phrase):
    myPhrases = []
    if (myTree.label() == phrase):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is Tree):
            list_of_phrases = ExtractPhrases(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases


def entity_discover(titulo, descricao):
    tags = []
    tokens = nltk.word_tokenize(titulo, language="portuguese")
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    #entities = nltk.chunk.ne_chunk(tagged, binary=True)

    persons = ExtractPhrases(entities,'PERSON')
    orgs = ExtractPhrases(entities,'ORGANIZATION')
    gpes = ExtractPhrases(entities,'GPE')
    for phrase in persons:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])

    for phrase in orgs:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])

    for phrase in gpes:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])


    # Taggs and chunks the description
    # Used to identify Entities

    tokens = nltk.word_tokenize(descricao, language="portuguese")
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    #entities = nltk.chunk.ne_chunk(tagged, binary=True)

    persons = ExtractPhrases(entities,'PERSON')
    orgs = ExtractPhrases(entities,'ORGANIZATION')
    gpes = ExtractPhrases(entities,'GPE')
    for phrase in persons:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])

    for phrase in orgs:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])

    for phrase in gpes:
        if phrase[0][0] not in tags:
            tags.append(phrase[0][0])
    return tags


def sentence_discover(titulo, descricao):
    tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    print tokenizer.tokenize(titulo)
    print tokenizer.tokenize(descricao)
