from classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG


# Добавления пользователя
def insert_user(user_id, user_password, user_email, user_type):
    query = "INSERT INTO Users(user_id, user_password, user_mail, user_type, " \
            "                  user_name, user_surname, user_patronymic, user_additional_info) " \
            "VALUES({0}, \'{1}\', \'{2}\', \'{3}\', " \
            "       \'{4}\', \'{5}\', \'{6}\', \'{7}\');".format(user_id, user_password,
                                                                 user_email, user_type,
                                                                 '', '', '', '')
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


# Добавление типа стихотворения
def insert_collection(collection_id, collection_name, creator_id, post_date):
    query = "INSERT INTO Collections(collection_id, collection_name, creator_id, post_date) " \
            "VALUES({0}, \'{1}\', {2}, {3}); ".format(collection_id, collection_name, creator_id, post_date)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


# Добавление типа стихотворения
def insert_poem_collection(collection_id, poem_id):
    query = "INSERT INTO Poems_Collections(collection_id, poem_id) " \
            "VALUES({0}, {1}); ".format(collection_id, poem_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)

