from classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


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


# Добавления пользователя
def insert_user(user_id, user_password, user_email, user_type):
    query = "INSERT INTO Users(user_id, user_password, user_mail, user_type) " \
            "VALUES({0}, \'{1}\', \'{2}\', \'{3}\');".format(user_id, user_password,
                                                             user_email, user_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавления писателя
def insert_creator(user_id):
    query = "INSERT INTO Creators(creator_id) " \
            "VALUES({0});".format(user_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление издателя
def insert_publisher(user_id):
    query = "INSERT INTO Publishers(publisher_id) " \
            "VALUES({0});".format(user_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавления типа пользователей
def insert_user_type(user_type):
    query = "INSERT INTO User_types(user_type) " \
            "VALUES(\'{0}\'); ".format(user_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление произведения
def insert_composition(composition_id, name, creator_id, date, type):
    query = "INSERT INTO Compositions(composition_id, composition_name, creator_id, " \
            "posting_date, modifier, composition_type) " \
            "VALUES({0}, \'{1}\', {2}, \'{3}\', \'Private\', \'{4}\'); ".format(composition_id, name,
                                                                            creator_id, date, type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление стихотворения
def insert_poem(poem_id):
    query = "INSERT INTO Poems(poem_id) " \
            "VALUES({0}); ".format(poem_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление прозаического произведения
def insert_prose(prose_id):
    query = "INSERT INTO Proses(prose_id) " \
            "VALUES({0}); ".format(prose_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление типа стихотворения
def insert_poem_type(poem_type):
    query = "INSERT INTO Poem_types(poem_type) " \
            "VALUES(\'{0}\'); ".format(poem_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление типа прозаического произведения
def insert_prose_type(prose_type):
    query = "INSERT INTO Prose_types(prose_type) " \
            "VALUES(\'{0}\'); ".format(prose_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление типа конкретного прозаического произведения
def insert_prose_composition_type(prose_id, prose_type):
    query = "INSERT INTO Types_Proses(prose_type, prose_id) " \
            "VALUES(\'{0}\', {1}); ".format(prose_type, prose_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление типа конкретного стихотворения
def insert_poem_composition_type(poem_id, poem_type):
    query = "INSERT INTO Types_Poems(poem_type, poem_id) " \
            "VALUES(\'{0}\', {1}); ".format(poem_type, poem_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление оценки от пользователя
def insert_compositions_marks(composition_id, user_id, mark):
    query = "INSERT INTO Compositions_Marks(composition_id, user_id, mark) " \
            "VALUES({0}, {1}, {2}); ".format(composition_id, user_id, mark)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)
