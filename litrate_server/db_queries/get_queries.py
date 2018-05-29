from classes.Poem import *
from classes.Prose import *
from db_queries.simple_get import *
from misc.configs import USER_TYPES


# Поиск пользователя по почте
def find_user_by_email(email):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Users " \
            "WHERE user_mail=\'{0}\';".format(email)
    res = database.execute_query(query)
    user = dict()
    if res:
        for k in res:
            user[k] = res[k][0]
    return user


#
def find_user_by_id(user_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Users " \
            "WHERE user_id={0};".format(user_id)
    res = database.execute_query(query)
    user = dict()
    if res:
        for k in res:
            user[k] = res[k][0]
    return user


#
def find_users_by_param_set(user_name=None, user_surname=None, rating_desc=True):
    values = ''
    if user_name is not None:
        values += "user_name LIKE \'%" + user_name + "%\' AND "
    if user_surname is not None:
        values += "user_surname LIKE \'%" + user_surname + "%\' AND "
    if values:
        values = values[:-4]
        database = MySqlDatabase(DATABASE_CONFIG)
        query = "SELECT * " \
                "FROM Users " \
                "WHERE {0};".format(values)
        res = database.execute_query(query)
        users = []
        if res:
            for i in range(len(res["user_id"])):
                users.append(dict())
                for k in res:
                    users[i][k] = res[k][i]
                if users[i]["user_type"] == USER_TYPES.CREATOR:
                    users[i].update(find_creator_info(users[i]["user_id"]))
                    users[i]["rating"] = get_creator_rating(users[i]["user_id"])
                else:
                    users[i].update(find_publisher_info(users[i]["user_id"]))
            if rating_desc:
                users.sort(key=lambda user: -user["rating"])
        return users
    return []


#
def get_creators_compositions(creator_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Compositions " \
            "WHERE creator_id={0};".format(creator_id)
    res = database.execute_query(query)
    comp = []
    if res:
        for i in range(len(res["composition_id"])):
            comp.append(get_true_composition(Composition(res["composition_id"][i],
                                    res["composition_name"][i],
                                    res["creator_id"][i],
                                    res["posting_date"][i],
                                    res["composition_type"][i],
                                    res["modifier"][i])))
    return comp


def get_all_compositions():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Compositions;"
    res = database.execute_query(query)
    comp = []
    if res:
        for i in range(len(res["composition_id"])):
            comp.append(get_true_composition(Composition(res["composition_id"][i],
                                    res["composition_name"][i],
                                    res["creator_id"][i],
                                    res["posting_date"][i],
                                    res["composition_type"][i],
                                    res["modifier"][i])))
    return comp


def get_composition(composition_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Compositions " \
            "WHERE composition_id={0};".format(composition_id)
    comp = database.execute_query(query)
    if comp:
        return Composition(comp["composition_id"][0],
                           comp["composition_name"][0],
                           comp["creator_id"][0],
                           comp["posting_date"][0],
                           comp["composition_type"][0],
                           comp["modifier"][0])
    return None


def get_like_to_composition_from_user(composition_id, user_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT mark " \
            "FROM Compositions_Marks " \
            "WHERE composition_id={0} AND user_id={1};".format(composition_id, user_id)
    res = database.execute_query(query)
    return int(res['mark'][0]) if res else None


def get_creator_rating(creator_id):
    compositions = get_creators_compositions(creator_id)
    creator_rating = 0
    if compositions:
        for comp in compositions:
            creator_rating += get_composition_rating(comp.id)
    return int(creator_rating)


def get_true_composition(comp):
    if not comp:
        return None
    if comp.composition_type == "Prose":
        return Prose(comp.id, comp.name, comp.creator_id,
                     comp.posting_date, comp.composition_type,
                     comp.modifier, get_prose_types(comp.id))
    else:
        return Poem(comp.id, comp.name, comp.creator_id,
                    comp.posting_date, comp.composition_type,
                    comp.modifier, get_poem_types(comp.id))


def get_creator_prose(creator_id):
    compositions = get_creators_compositions(creator_id)
    prose = []
    for comp in compositions:
        if comp.composition_type == "Prose":
            prose.append(comp)
    return prose


def get_creator_poem(creator_id):
    compositions = get_creators_compositions(creator_id)
    poem = []
    for comp in compositions:
        if comp.composition_type == "Poem":
            poem.append(comp)
    return poem


def get_creator_all_types(creator_id):
    compositions = get_creators_compositions(creator_id)
    poem_types = dict()
    prose_types = dict()
    for comp in compositions:
        if comp.composition_type == "Prose":
            for prose_type in comp.prose_type:
                if not prose_types.get(prose_type):
                    prose_types[prose_type] = 0
                prose_types[prose_type] += 1
        else:
            for poem_type in comp.poem_type:
                if not poem_types.get(poem_type):
                    poem_types[poem_type] = 0
                poem_types[poem_type] += 1
    return poem_types, prose_types
