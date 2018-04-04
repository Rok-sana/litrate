from usefull_classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


# Поиск минимального натурального неиспользованного индекса
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


# Добавления пользователя
def insert_user(user_id, user_login, user_password, user_email, user_type):
    query = "INSERT INTO Users(user_id, user_login, user_password, user_mail, user_type) " \
            "VALUES({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\');".format(user_id, user_login,
                                                                      user_password, user_email, user_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавления писателя
def insert_creator(user_id):
    query = "INSERT INTO Creators(creator_id, rating) " \
            "VALUES({0}, {1});".format(user_id, 0)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление издателя
def insert_publisher(user_id):
    query = "INSERT INTO Publishers(publisher_id, rating) " \
            "VALUES({0}, {1});".format(user_id, 0)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавления типа пользователей
def insert_user_type(user_type):
    query = "INSERT INTO User_types(user_type) " \
            "VALUES(\'{0}\'); ".format(user_type)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)
