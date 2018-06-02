from classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG
from db_queries.get_queries import *
import os


def delete_compositions_marks(composition_id, user_id):
    query = "DELETE FROM Compositions_Marks " \
            "WHERE composition_id={0} AND user_id={1}; ".format(composition_id, user_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


def delete_composition(composition_id):
    composition = get_composition(composition_id, session["user_id"])
    if composition.composition_type == "Poem":
        delete_poem(composition_id, composition.creator_id)
    else:
        delete_prose(composition_id, composition.creator_id)
    query = "DELETE FROM Compositions " \
            "WHERE composition_id={0}; ".format(composition_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


def delete_poem(poem_id, creator_id):
    query = "DELETE FROM Poems " \
            "WHERE poem_id={0}; ".format(poem_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)
    file_path = "data/user_" + str(creator_id) + "/poem/" + str(poem_id)
    os.remove(file_path)


def delete_prose(prose_id, creator_id):
    query = "DELETE FROM Proses " \
            "WHERE prose_id={0}; ".format(prose_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)
    file_path = "data/user_" + str(creator_id) + "/prose/" + str(prose_id)
    os.remove(file_path)


def delete_poem_collection(poem_id, collection_id):
    query = "DELETE FROM Poems_Collections " \
            "WHERE poem_id={0} AND collection_id={1}; ".format(poem_id, collection_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


def delete_collection(collection_id):
    query = "DELETE FROM Collections " \
            "WHERE collection_id={0}; ".format(collection_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)