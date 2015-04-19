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


def get_relationships(relationships):
    ix = index.open_dir(index_dir)
    results = ix.searcher().search(Every("title"), limit=15)
    for r in results:
        entities = get_entities(r["title"] + " " + r["body"])
        relationships.update(extract_relationships(entities, relationships))
    return relationships


# CODIGO DE TESTE
#relationships = get_relationships(dict())
#entities = relationships["Portugal"]
#for entry in sorted(entities):
#    print entry