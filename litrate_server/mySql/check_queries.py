from usefull_classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


# Поиск пользователя по почте или логину
def find_user(email=None, login=None):
    database = MySqlDatabase(DATABASE_CONFIG)
    if email:
        query = "SELECT * " \
                "FROM Users " \
                "WHERE user_mail=\'{0}\';".format(email)
        res = database.execute_query(query)
        if res != {}:
            return res
    if login:
        query = "SELECT * " \
                "FROM Users " \
                "WHERE user_login=\'{0}\';".format(login)
        res = database.execute_query(query)
        if res != {}:
            return res
    return {}


# Поиск писателя
def find_creator(creator_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Creators " \
            "WHERE creator_id={0};".format(creator_id)
    return database.execute_query(query)


# Поиск издателя
def find_publisher(publisher_id):
    database = MySqlDatabase(DATABASE_CONFIG)
    query = "SELECT * " \
            "FROM Publishers " \
            "WHERE publisher_id={0};".format(publisher_id)
    return database.execute_query(query)

