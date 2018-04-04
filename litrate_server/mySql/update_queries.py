from usefull_classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG
from usefull_classes.forms import *
from misc.configs import USER_TYPES


def _make_user_update_query_params(user_info_form):
    values = ""
    for att_name, att_value in super(type(user_info_form), user_info_form).fields():
        values += att_name.text + "=" + att_value + ", "
    values = values[0:-2]
    return values


def _make_update_query_params(user_info_form):
    values = ""
    for att_name, att_value in user_info_form.fields():
        values += att_name.text + "=" + att_value + ", "
    values = values[0:-2]
    return values


def update_user_info(user_id, user_info_form, user_type):
    values = _make_user_update_query_params(user_info_form)
    query = "UPDATE Users SET {0} " \
            "WHERE user_id={1};".format(values, user_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    if user_type == USER_TYPES.CREATOR:
        update_creator_info(user_id, user_info_form)
    elif user_type == USER_TYPES.PUBLISHER:
        update_publisher_info(user_id, user_info_form)
    else:
        pass
    database.execute_query(query)


def update_creator_info(creator_id, user_info_form):
    values = _make_update_query_params(user_info_form)
    query = "UPDATE Creators SET {0} " \
            "WHERE creator_id={1};".format(values, creator_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)


def update_publisher_info(publisher_id, user_info_form):
    values = _make_update_query_params(user_info_form)
    query = "UPDATE Publishers SET {0} " \
            "WHERE publisher_id={1};".format(values, publisher_id)
    database = MySqlDatabase(DATABASE_CONFIG)
    database.execute_query(query)
