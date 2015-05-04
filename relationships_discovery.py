from whoosh.query import *

from entities_discovery import *
from graph_functions import draw_graph


def extract_relationships(entities, relationships):
    for key in entities:
        if key not in relationships:
            relationships[key] = []
        for entity in entities:
            if (entity != key):
                relationships[key].append(entity)
    return relationships


def get_all_relationships():
    relationships = dict()
    ix = index.open_dir(index_dir)
    results = ix.searcher().search(Every("title"), limit=None)
    for r in results:
        #print r["title"]
        #print r["body"]
        #print r["link"]
        entities = get_entities_nltk(r["title"] + ";" + r["body"])
        relationships.update(extract_relationships(entities, relationships))
    return relationships


#TRATAR PROBLEMAS COM LOWER CASE, nao reconhece 'portugal'
#def get_relationships(entity):
#    entities = relationships[entity]
#    print entities
#    return " ; ".join(sorted(entities))


# Codigo para gerar um grafo de todas as relacoes
def get_all_relationships_graph():
    relationships = dict()
    relationships_graph = []
    ix = index.open_dir(index_dir)
    results = ix.searcher().search(Every("title"), limit=None)
    for r in results:
        entities = get_entities_nltk(r["title"] + ";" + r["body"])
        if len(entities) > 1:
            list = entities[1:]
            for entity in list:
                relationships_graph.append((entities[0], entity))
        relationships.update(extract_relationships(entities, relationships))
    return relationships, relationships_graph


# Codigo para gerar um grafo das relacoes da procura
def get_specific_relationships_graph(ask):
    relationships_graph = []
    ix = index.open_dir(index_dir)
    with ix.searcher() as searcher:
        query = MultifieldParser(["title", "body"], ix.schema, group=OrGroup).parse(ask.decode("utf-8"))
        results = searcher.search(query, limit=None)
        for r in results:
            entities = get_entities_nltk(r["title"] + ";" + r["body"])
            if len(entities) > 1:
                list = entities[1:]
                for entity in list:
                    relationships_graph.append((entities[0], entity))
    return relationships_graph


def relation_graph(entity):
    news_relations = get_specific_relationships_graph(entity)
    print news_relations
    draw_graph(news_relations)

relation_graph("Ronaldo")