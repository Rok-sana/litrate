from db_queries.simple_get import *
from db_queries.insertion_queries import *
import datetime
from db_queries.get_queries import get_collection_by_id, get_collection_poems, get_composition_text, \
                                   get_all_collections_query
from db_queries.delete_queries import delete_poem_collection, delete_collection

def add_collection(collection_name, creator_id, poem_ids_list):
    collection_id = find_minimum_unused_collection_id()
    now = datetime.datetime.now()
    insert_collection(collection_id, collection_name, creator_id, now.strftime("%Y-%m-%d"))
    for poem_id in poem_ids_list:
        insert_poem_collection(collection_id, poem_id)


def calculate_rating(poems):
    rating = 0
    for poem in poems:
        rating += poem.rating
    return rating


def get_collection(collection_id, curr_user_id):
    coll = get_collection_by_id(collection_id)
    poems = get_collection_poems(collection_id, curr_user_id)
    coll["rating"] = 0
    for poem in poems:
        poem.text = get_composition_text(poem.id, curr_user_id)
        coll["rating"] += poem.rating
    return coll, poems


def get_creator_collections(creator_id, curr_user_id):
    colls = get_creator_collections_by_creator_id(creator_id)
    for coll in colls:
        poems = get_collection_poems(coll["collection_id"], curr_user_id)
        coll["rating"] = calculate_rating(poems)
    return colls


def get_all_collections(curr_user_id):
    colls = get_all_collections_query()
    for coll in colls:
        poems = get_collection_poems(coll["collection_id"], curr_user_id)
        coll["rating"] = calculate_rating(poems)
    return colls


def delete_collection_by_id(collection_id, curr_user_id):
    coll, poems = get_collection(collection_id, curr_user_id)
    for poem in poems:
        delete_poem_collection(poem.id, collection_id)
    delete_collection(collection_id)


def collection_is_used(collection_id, curr_user_id):
    return False