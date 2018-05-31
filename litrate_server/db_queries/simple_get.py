from classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


def get_composition_rating(composition_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT COALESCE(SUM(mark), 0) AS 'rating' " \
            "FROM Compositions_Marks " \
            "WHERE composition_id={0};".format(composition_id)
    return int(database.execute_query(query)['rating'][0])


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
    print(res)
