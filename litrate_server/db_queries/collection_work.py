from db_queries.simple_get import *
from db_queries.insertion_queries import *
import datetime


def add_collection(collection_name, creator_id, poem_ids_list):
    collection_id = find_minimum_unused_collection_id()
    now = datetime.datetime.now()
    insert_collection(collection_id, collection_name, creator_id, now.strftime("%Y-%m-%d"))
    for poem_id in poem_ids_list:
        insert_poem_collection(collection_id, poem_id)
