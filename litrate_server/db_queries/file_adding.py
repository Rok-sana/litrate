from db_queries.insertion_queries import *
from db_queries.get_queries import *
from db_queries.composition_work import rewrite_file

import datetime


def add_poem_by_file(file, name, poem_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    file_path = "data/user_" + str(creator_id) + "/poem/" + str(composition_id)
    now = datetime.datetime.now()
    file.save(file_path)
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Poem")
    insert_poem(composition_id)
    for pt in poem_types:
        insert_poem_composition_type(composition_id, pt)


def add_poem_by_text(text, name, poem_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    now = datetime.datetime.now()
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Poem")
    insert_poem(composition_id)
    rewrite_file(composition_id, text)
    for pt in poem_types:
        insert_poem_composition_type(composition_id, pt)


def add_prose_by_file(file, name, prose_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    file_path = "data/user_" + str(creator_id) + "/prose/" + str(composition_id)
    now = datetime.datetime.now()
    file.save(file_path)
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Prose")
    insert_prose(composition_id)
    for pt in prose_types:
        insert_prose_composition_type(composition_id, pt)


def add_prose_by_text(text, name, prose_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    now = datetime.datetime.now()
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Prose")
    insert_prose(composition_id)
    rewrite_file(composition_id, text)
    for pt in prose_types:
        insert_poem_composition_type(composition_id, pt)


def add_avatar(file, user_id):
    file_path = "data/user_" + str(user_id) + "/avatar"
    file.save(file_path)


def validated_file(file):
    file.save("data/temp")
    try:
        with open("data/temp") as f:
            for line in f:
                pass
    except UnicodeDecodeError:
        return False
    return True


