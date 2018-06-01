from db_queries.simple_get import *
from db_queries.insertion_queries import *
import datetime
from db_queries.get_queries import get_collection_by_id, get_collection_poems_id, get_composition_text


def add_collection(collection_name, creator_id, poem_ids_list):
    collection_id = find_minimum_unused_collection_id()
    now = datetime.datetime.now()
    insert_collection(collection_id, collection_name, creator_id, now.strftime("%Y-%m-%d"))
    for poem_id in poem_ids_list:
        insert_poem_collection(collection_id, poem_id)


def get_collection(collection_id, curr_user_id):
    coll = get_collection_by_id(collection_id)
    poems = get_collection_poems_id(collection_id, curr_user_id)
    for poem in poems:
        poem.text = get_composition_text(poem.id, curr_user_id)
    return coll, poems