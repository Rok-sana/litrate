from mySql.insertion_queries import insert_user_type


# Добавление основной информации в базу данных
def add_information():
    insert_user_type("Publisher")
    insert_user_type("Creator")
    insert_user_type("Moderator")
