from whoosh.query import *

from entities_discovery import *
from graph_functions import draw_graph
from entities_discovery import remove_duplicates
from statistics import read_stats


def extract_relationships(entities, relationships):
    for key in entities:
        print key
        if key not in relationships:
            relationships[key] = []
        for entity in entities:
            if entity != key:
                relationships[key].append(entity)
    return relationships


def get_all_relationships():
    relationships = dict()
    ix = index.open_dir(index_dir)
    results = ix.searcher().search(Every("title"), limit=None)
    for r in results:
        entities = get_entities_nltk(r["title"] + ";" + r["body"])
        #relationships.update(extract_relationships(entities, relationships))
        #entities = get_entities_nltk(entry[0][0] + ";" + entry[0][1])
        entities = remove_small_not_in_dbpedia(entities)
        entities = remove_duplicates(entities)
        relations = get_news_relations(r["title"], entities)
        relations.extend(get_news_relations(r["body"], entities))
        save_relations(relations)
    return relationships


#TRATAR PROBLEMAS COM LOWER CASE, nao reconhece 'portugal'
#def get_relationships(entity):
#    entities = relationships[entity]
#    print entities
#    return " ; ".join(sorted(entities))


# # Codigo para gerar um grafo de todas as relacoes
# def get_all_relationships_graph():
#     relationships = dict()
#     relationships_graph = []
#     ix = index.open_dir(index_dir)
#     results = ix.searcher().search(Every("title"), limit=None)
#     for r in results:
#         entities = get_entities_nltk(r["title"] + ";" + r["body"])
#         if len(entities) > 1:
#             list = entities[1:]
#             for entity in list:
#                 relationships_graph.append((entities[0], entity))
#         relationships.update(extract_relationships(entities, relationships))
#     return relationships, relationships_graph
#
#
# # Codigo para gerar um grafo das relacoes da procura
# def get_specific_relationships_graph(ask):
#     relationships_graph = []
#     ix = index.open_dir(index_dir)
#     with ix.searcher() as searcher:
#         query = MultifieldParser(["title", "body"], ix.schema, group=OrGroup).parse(ask.decode("utf-8"))
#         results = searcher.search(query, limit=None)
#         for r in results:
#             all_entities = get_entities_nltk(r["title"] + ";" + r["body"])
#             entities = remove_duplicates(all_entities)
#             if len(entities) > 1:
#                 list = entities[1:]
#                 for entity in list:
#                     relationships_graph.append((entities[0], entity))
#     return relationships_graph


def get_relations_by_query(ask):
    relations = read_stats("relations")
    relationships_graph = []

    if ask in relations:
        for item in relations[ask]:
            relationships_graph.append((ask, item))

    for key in relations:
        for value in relations[key]:
            if ask in value:
                relationships_graph.append((key, ask))

    return relationships_graph


def process_all_news_relations():
    ix = index.open_dir(index_dir)
    results = ix.searcher().search(Every("title"), limit=None)
    for r in results:
        entities = get_entities_nltk(r["title"] + ";" + r["body"])
        entities = remove_small_not_in_dbpedia(entities)
        entities = remove_duplicates(entities)
        relations = get_news_relations(r["title"], entities)
        relations.extend(get_news_relations(r["body"], entities))
        save_relations(relations)
        update_entity_counter(entities)


def get_all_relations_graph():
    relations = read_stats("relations")
    relationships_graph = []

    for key in relations:
        for rel_list in relations[key]:
            for item in rel_list:
                relationships_graph.append((key, item))

    return relationships_graph


def print_relation_graph(entity):
    news_relations = get_relations_by_query(entity)
    draw_graph(news_relations)
    return news_relations


def print_all_relations_graph():
    news_relations = get_all_relations_graph()
    draw_graph(news_relations)
    return news_relations


#print print_relation_graph("Portugal")
#print print_all_relations_graph()
#print relation_graph("PSD")
process_all_news_relations()