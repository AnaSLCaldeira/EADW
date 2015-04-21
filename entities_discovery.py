from news_searcher import *
import nltk
from nltk.tree import *


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


def get_news_entities(ask):
	news = news_searcher(ask)
	result = ""
	for entry in news:
	    entities = " ; ".join(get_entities(entry[0][0] + " " + entry[0][1]))
	    result += "Score: " + str(entry[1]) + "\nTitulo: " + entry[0][0].encode("UTF-8") + "\nDescricao: " + entry[0][1].encode("UTF-8") + "\nLink: " + entry[0][2].encode("UTF-8") + "\nEntidades: " + entities + "\n\n"
	return result

dbpedia_entities = parse_dbpedia()