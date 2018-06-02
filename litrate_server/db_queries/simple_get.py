from classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


def get_composition_rating(composition_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT COALESCE(SUM(mark), 0) AS 'rating' " \
            "FROM Compositions_Marks " \
            "WHERE composition_id={0};".format(composition_id)
    return int(database.execute_query(query)['rating'][0])


def get_prose(prose_id, curr_user_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Proses " \
            "WHERE prose_id={0};".format(prose_id)
    res = database.execute_query(query)
    prose = dict()
    if res:
        for k in res:
            prose[k] = res[k][0]
        print(prose)
        if prose["creator_id"] != curr_user_id and prose["status"] == "Private":
            return dict()
    return prose


# Жанры прозаических произведений
def get_prose_types(prose_id=None):
    if prose_id:
        database = MySqlDatabase(DATABASE_CONFIG)
        query = "SELECT prose_type " \
                "FROM Types_Proses " \
                "WHERE prose_id={0};".format(prose_id)
        res = database.execute_query(query)
        if res:
            return res["prose_type"]
        else:
            return res
    else:
        database = MySqlDatabase(DATABASE_CONFIG)
        query = "SELECT * " \
                "FROM Prose_types;"
        return database.execute_query(query)["prose_type"]


# Жанры стихотворений
def get_poem_types(poem_id=None):
    if poem_id:
        database = MySqlDatabase(DATABASE_CONFIG)
        query = "SELECT poem_type " \
                "FROM Types_Poems " \
                "WHERE poem_id={0};".format(poem_id)
        res = database.execute_query(query)
        if res:
            return res["poem_type"]
        else:
            return res
    else:
        database = MySqlDatabase(DATABASE_CONFIG)
        query = "SELECT * " \
                "FROM Poem_types;"
        return database.execute_query(query)["poem_type"]


# Поиск информации писателя
def find_creator_info(creator_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Creators " \
            "WHERE creator_id={0};".format(creator_id)
    res = database.execute_query(query)
    if res:
        res["country"] = res["country"][0]
        res["creator_id"] = res["creator_id"][0]
        res["city"] = res["city"][0]
    return res


# Поиск информации издателя
def find_publisher_info(publisher_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Publishers " \
            "WHERE publisher_id={0};".format(publisher_id)
    return database.execute_query(query)


# Поиск минимального натурального неиспользованного идентификатора пользователя
def find_minimum_unused_user_id():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT min(unused) AS unused " \
            "FROM ( " \
            "SELECT MIN(t1.user_id)+1 as unused " \
            "FROM Users AS t1 " \
            "WHERE NOT EXISTS (SELECT * FROM Users AS t2 WHERE t2.user_id = t1.user_id+1) " \
            "UNION " \
            "SELECT 1 " \
            "FROM DUAL " \
            "WHERE NOT EXISTS (SELECT * FROM Users WHERE user_id = 1) " \
            ") AS subquery;"
    return database.execute_query(query, False)['unused'][0]


# Поиск минимального натурального неиспользованного идентификатора
def find_minimum_unused_sent_collection_offer():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT min(unused) AS unused " \
            "FROM ( " \
            "SELECT MIN(t1.offer_id)+1 as unused " \
            "FROM Sent_Collections AS t1 " \
            "WHERE NOT EXISTS (SELECT * FROM Sent_Collections AS t2 WHERE t2.offer_id = t1.offer_id+1) " \
            "UNION " \
            "SELECT 1 " \
            "FROM DUAL " \
            "WHERE NOT EXISTS (SELECT * FROM Sent_Collections WHERE offer_id = 1) " \
            ") AS subquery;"
    return database.execute_query(query, False)['unused'][0]


# Поиск минимального натурального неиспользованного идентификатора
def find_minimum_unused_sent_prose_offer():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT min(unused) AS unused " \
            "FROM ( " \
            "SELECT MIN(t1.offer_id)+1 as unused " \
            "FROM Sent_Proses AS t1 " \
            "WHERE NOT EXISTS (SELECT * FROM Sent_Proses AS t2 WHERE t2.offer_id = t1.offer_id+1) " \
            "UNION " \
            "SELECT 1 " \
            "FROM DUAL " \
            "WHERE NOT EXISTS (SELECT * FROM Sent_Proses WHERE offer_id = 1) " \
            ") AS subquery;"
    return database.execute_query(query, False)['unused'][0]


# Поиск минимального натурального неиспользованного идентификатора произведения
def find_minimum_unused_composition_id():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT min(unused) AS unused " \
            "FROM ( " \
            "SELECT MIN(t1.composition_id)+1 as unused " \
            "FROM Compositions AS t1 " \
            "WHERE NOT EXISTS (SELECT * FROM Compositions AS t2 WHERE t2.composition_id = t1.composition_id+1) " \
            "UNION " \
            "SELECT 1 " \
            "FROM DUAL " \
            "WHERE NOT EXISTS (SELECT * FROM Compositions WHERE composition_id = 1) " \
            ") AS subquery;"
    return database.execute_query(query, False)['unused'][0]


# Поиск минимального натурального неиспользованного идентификатора
def find_minimum_unused_collection_id():
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT min(unused) AS unused " \
            "FROM ( " \
            "SELECT MIN(t1.collection_id)+1 as unused " \
            "FROM Collections AS t1 " \
            "WHERE NOT EXISTS (SELECT * FROM Collections AS t2 WHERE t2.collection_id = t1.collection_id+1) " \
            "UNION " \
            "SELECT 1 " \
            "FROM DUAL " \
            "WHERE NOT EXISTS (SELECT * FROM Collections WHERE collection_id = 1) " \
            ") AS subquery;"
    return database.execute_query(query, False)['unused'][0]


def get_creators_collections(creator_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Collections " \
            "WHERE creator_id={0};".format(creator_id)
    res = database.execute_query(query)
    colls = []
    if res:
        for i in range(len(res["collection_id"])):
            colls.append(dict())
            for k in res:
                colls[i][k] = res[k][i]
    return colls


def get_collection_by_id(collection_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Collections " \
            "WHERE collection_id={0};".format(collection_id)
    res = database.execute_query(query)
    coll = dict()
    if res:
        for k in res:
            coll[k] = res[k][0]
    return coll


def get_creator_collections_by_creator_id(creator_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Collections " \
            "WHERE creator_id={0};".format(creator_id)
    res = database.execute_query(query)
    colls = []
    if res:
        for i in range(len(res["collection_id"])):
            colls.append(dict())
            for k in res:
                colls[i][k] = res[k][i]
    return colls


def find_collection_to_publisher(collection_id, publisher_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Sent_Collections " \
            "WHERE collection_id={0} AND publisher_id={1};".format(collection_id, publisher_id)
    res = database.execute_query(query)
    offer = []
    if res:
        for k in res:
            offer[k] = res[k][0]
    return offer


def find_prose_to_publisher(prose_id, publisher_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Sent_Proses " \
            "WHERE prose_id={0} AND publisher_id={1};".format(prose_id, publisher_id)
    res = database.execute_query(query)
    offer = []
    if res:
        for k in res:
            offer[k] = res[k][0]
    return offer
