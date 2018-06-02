from db_queries.get_queries import *
from db_queries.update_queries import update_composition_modifier
import codecs


def rewrite_file(composition_id, text, curr_user_id):
    comp = get_composition(composition_id, curr_user_id)
    if not comp:
        return
    path = "data/user_" + str(comp.creator_id) + "/" + \
           comp.composition_type.lower() + "/" + str(composition_id)
    with codecs.open(path, "w", encoding="utf8") as f:
        f.write(text)


def change_composition_modifier(composition_id):
    comp = get_composition(composition_id, session.get("user_id"))
    if not comp:
        return
    if comp.modifier == "Private":
        update_composition_modifier(composition_id, "Public")
    elif not composition_is_used(composition_id):
        update_composition_modifier(composition_id, "Private")
    else:
        return False
    return True


def composition_is_used(composition_id):
    if poem_collections_id(composition_id):
        return True
    return False
