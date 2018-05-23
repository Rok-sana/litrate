from db_queries.insertion_queries import insert_user_type, insert_poem_type, insert_prose_type


def _add_user_types():
    insert_user_type("Publisher")
    insert_user_type("Creator")
    insert_user_type("Moderator")


def _add_prose_types():
    insert_prose_type("детектив")
    insert_prose_type("фантастика")
    insert_prose_type("исторический")
    insert_prose_type("фэнтези")
    insert_prose_type("приключения")
    insert_prose_type("ужасы")
    insert_prose_type("триллер")
    insert_prose_type("любовный роман")
    insert_prose_type("юмор")
    insert_prose_type("психология")
    insert_prose_type("вестерн")


def _add_poem_types():
    insert_poem_type("гражданская")
    insert_poem_type("патриотическая")
    insert_poem_type("философская")
    insert_poem_type("пейзажная")
    insert_poem_type("медитативная")
    insert_poem_type("любовно-пейзажная")


# Добавление основной информации в базу данных
def add_information():
    _add_user_types()
    _add_prose_types()
    _add_poem_types()
