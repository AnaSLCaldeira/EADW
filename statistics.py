import json

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
    return get_max_value(data)


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
        with open('statistics/entity_relations.json', 'r') as squery:
            diction = json.load(squery)
        return diction
    else:
        return 0


def get_max_value(dic):
    maxx = max(dic.values())
    keys = [x for x, y in dic.items() if y == maxx]
    return keys[0] if len(keys) == 1 else keys


def save_relations(relations):
    current_dict = read_stats(CONST_RELATIONS)

    for relation in relations:
        if not relation[0] in current_dict:
            current_dict[relation[0]] = relation[1]

    with open('statistics/entity_relations.json', 'w') as squery:
        json.dump(current_dict, squery)


#print "Most searched keyword(s): " + most_searched_keyword()
#print "Most searched query(ies): " + most_searched_query()