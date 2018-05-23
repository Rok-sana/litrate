from db_queries.insertion_queries import *
import os


# Регистрация пользователя (добавление в базу данных соответствующие записи)
def signup_user(email, password, user_type):
    user_id = find_minimum_unused_user_id()
    insert_user(user_id, password, email, user_type)
    if user_type == 'Creator':
        insert_creator(user_id)
        create_user_dir(user_id, True)
    else:
        insert_publisher(user_id)
        create_user_dir(user_id)


# Создает папки для данных пользавателя
def create_user_dir(user_id, creator=False):
    file_path = "data/user_" + str(user_id) + "/"
    ensure_dir(file_path)
    if creator:
        ensure_dir(file_path + "prose/")
        ensure_dir(file_path + "poem/")


# Создает папку по указаному пути, если нету
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
