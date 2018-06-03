from db_queries.insertion_queries import insert_message
from db_queries.get_queries import find_minimum_unused_message_id, find_user_by_id
from db_queries.simple_get import find_dialog_companions_from, find_dialog_companions_to, get_dialog_between_users

import datetime


def add_message(from_user_id, to_user_id, message):
    now = datetime.datetime.now()
    message_id = find_minimum_unused_message_id()
    insert_message(message_id, from_user_id, to_user_id, now.strftime("%Y-%m-%d"), message)


def get_dialogs_for_user(user_id):
    companions = set()
    for companion in find_dialog_companions_to(user_id):
        companions.add(companion)
    for companion in find_dialog_companions_from(user_id):
        companions.add(companion)
    companions = list(companions)
    dialogs = dict()
    for companion in companions:
        dialogs[companion] = dict()
        dialogs[companion]["messages"] = get_dialog_between_users(user_id, companion)
        comp = find_user_by_id(companion)
        dialogs[companion]["companion_name"] = comp["user_name"] + " " + comp["user_surname"]
    return dialogs
