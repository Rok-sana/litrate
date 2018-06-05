from db_queries.insertion_queries import insert_collection_to_publisher, insert_prose_to_publisher
from db_queries.simple_get import find_minimum_unused_sent_collection_offer, \
                                  find_minimum_unused_sent_prose_offer, \
                                  find_prose_to_publisher, find_collection_to_publisher
from db_queries.get_queries import get_collections_id_to_publisher, get_composition, get_proses_id_to_publisher, \
                        get_creator_prose
from db_queries.collection_work import get_collection, get_creator_collections
import datetime
from db_queries.update_queries import update_sent_prose_status, update_sent_collection_status


def send_collection_to_publisher(collection_id, publisher_id):
    if find_collection_to_publisher(collection_id, publisher_id):
        return False
    offer_id = find_minimum_unused_sent_collection_offer()
    now = datetime.datetime.now()
    insert_collection_to_publisher(offer_id, collection_id, publisher_id, now.strftime("%Y-%m-%d"))
    return True


def send_prose_to_publisher(prose_id, publisher_id):
    if find_prose_to_publisher(prose_id, publisher_id):
        return False
    offer_id = find_minimum_unused_sent_prose_offer()
    now = datetime.datetime.now()
    insert_prose_to_publisher(offer_id, prose_id, publisher_id, now.strftime("%Y-%m-%d"))
    return True


def get_collections_to_publisher_by_status(publisher_id, status, curr_user_id):
    colls_id = get_collections_id_to_publisher(publisher_id, status)
    colls = [get_collection(coll_id, curr_user_id)[0] for coll_id in colls_id]
    return colls


def get_proses_to_publisher_by_status(publisher_id, status, curr_user_id):
    proses_id = get_proses_id_to_publisher(publisher_id, status)
    proses = [get_composition(prose_id, curr_user_id) for prose_id in proses_id]
    return proses


def get_creator_non_sent_proses(creator_id, publisher_id, curr_user_id):
    proses = get_creator_prose(creator_id, curr_user_id)
    correct_proses = []
    for prose in proses:
        if prose.modifier == "Public" and not find_prose_to_publisher(prose.id, publisher_id):
            correct_proses.append(prose)
    return correct_proses


def get_creator_non_sent_collections(creator_id, publisher_id, curr_user_id):
    collections = get_creator_collections(creator_id, curr_user_id)
    correct_collections = []
    for collection in collections:
        print(collection)
        if not find_collection_to_publisher(collection["collection_id"], publisher_id):
            correct_collections.append(collection)
    return correct_collections


def get_sent_prose_status(prose_id, publisher_id):
    find_prose_to_publisher(prose_id, publisher_id)


def modify_sent_prose_status(offer_id, status):
    update_sent_prose_status(offer_id, status)


def modify_sent_collection_status(offer_id, status):
    update_sent_collection_status(offer_id, status)

