from mySql.insertion_queries import *
import datetime


def add_poem(file, name, poem_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    file_path = "data/user_" + str(creator_id) + "/poem/" + str(composition_id)
    now = datetime.datetime.now()
    file.save(file_path)
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Poem")
    insert_poem(composition_id)
    for pt in poem_types:
        insert_poem_composition_type(composition_id, pt)


def add_prose(file, name, prose_types, creator_id):
    composition_id = find_minimum_unused_composition_id()
    file_path = "data/user_" + str(creator_id) + "/prose/" + str(composition_id)
    now = datetime.datetime.now()
    file.save(file_path)
    insert_composition(composition_id, name, creator_id, now.strftime("%Y-%m-%d"), "Prose")
    insert_prose(composition_id)
    for pt in prose_types:
        insert_prose_composition_type(composition_id, pt)


