import json
import os

CONST_WORD = "word"
CONST_QUERY = "query"
CONST_ENTITY = "entity"
CONST_RELATIONS = "relations"


def most_searched_query():
    data = read_stats(CONST_QUERY)
    return get_max_value(data)


def most_searched_keyword():
    data = read_stats(CONST_WORD)
    return get_max_value(data)


def most_popular_entity():
    data = read_stats(CONST_ENTITY)
    return get_max_value(data)


def keyword_with_most_relations():
    data = read_stats(CONST_RELATIONS)
    return " ; ".join(get_max_relation_value(data))


def add_searched_query(ask):
    current_dict = read_stats(CONST_QUERY)

    if current_dict.has_key(ask):
        current_dict[ask] += 1
    else:
        current_dict[ask] = 1

    with open('statistics/searched_query.json', 'w') as squery:
        json.dump(current_dict, squery)


def add_searched_word(ask):
    search = ask.split(" ")
    current_dict = read_stats(CONST_WORD)

    for word in search:
        if current_dict.has_key(word):
            current_dict[word] += 1
        else:
            current_dict[word] = 1

    with open('statistics/searched_word.json', 'w') as squery:
        json.dump(current_dict, squery)


def add_entity_stats(entities):
    search = entities.split(" ")
    current_dict = read_stats(CONST_ENTITY)

    for word in search:
        if current_dict.has_key(word):
            current_dict[word] += 1
        else:
            current_dict[word] = 1

    with open('statistics/entities_counter.json', 'w') as squery:
        json.dump(current_dict, squery)


def add_relation(relations):

    current_set = read_stats(CONST_RELATIONS)

    for relation in relations:
        if relation[0] in current_set:
            if not relation[1] in current_set[relation[0]]:
                current_set[relation[0]].append(relation[1])
        else:
            current_set[relation[0]] = [relation[1]]

    with open('statistics/entity_relations.json', 'w') as squery:
        json.dump(current_set, squery, indent=4)


def read_stats(which):
    if which == CONST_WORD:
        with open('statistics/searched_word.json', 'r') as squery:
            diction = json.load(squery)
        return diction
    elif which == CONST_QUERY:
        with open('statistics/searched_query.json', 'r') as squery:
            diction = json.load(squery)
        return diction
    elif which == CONST_ENTITY:
        with open('statistics/entities_counter.json', 'r') as squery:
            diction = json.load(squery)
        return diction
    elif which == CONST_RELATIONS:
        if os.stat("statistics/entity_relations.json").st_size == 0:
            return dict()
        else:
            with open('statistics/entity_relations.json', 'r') as squery:
                diction = json.load(squery)
        return diction
    else:
        return 0


def get_max_value(dic):
    if len(dic.keys()) != 0:
        maxx = max(dic.values())
        keys = [x for x, y in dic.items() if y == maxx]
        return keys[0] if len(keys) == 1 else keys
    else:
        return "No Entities"


def get_max_relation_value(data):
    max_value = 0
    entities = []

    for key in data:
        if len(data[key]) >= max_value:
            max_value = len(data[key])
            entities.append(key)

    return entities


def save_relations(relations):

    relation_set = set()

    for relation in relations:
        relation_set.add((relation[0], relation[1]))

    if relation_set:
        add_relation(relation_set)


def update_entity_counter(entities):
    entity_counter = read_stats(CONST_ENTITY)

    for entity in entities:
        if entity in entity_counter:
            entity_counter[entity] += 1
        else:
            entity_counter[entity] = 1

    with open('statistics/entities_counter.json', 'w') as squery:
        json.dump(entity_counter, squery, indent=4)


print "Most searched keyword(s): " + most_searched_keyword()
print "Most searched query(ies): " + most_searched_query()
print "Most popular entity: " + most_popular_entity()
print "Entity(ies) with most relations: " + keyword_with_most_relations()