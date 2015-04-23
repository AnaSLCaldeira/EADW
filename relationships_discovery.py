from entities_discovery import *
from whoosh.query import *


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
        entities = get_entities_nltk(r["title"] + " " + r["body"])
        relationships.update(extract_relationships(entities, relationships))
    return relationships


#TRATAR PROBLEMAS COM LOWER CASE, nao reconhece 'portugal'
def get_relationships(entity):
    entities = relationships[entity]
    #print entities
    return " ; ".join(sorted(entities))

relationships = get_all_relationships()
print get_relationships("Portugal")