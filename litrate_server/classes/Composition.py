from db_queries.simple_get import get_composition_rating

class Composition:
    def __init__(self, id, name, creator_id, posting_date, composition_type, modifier):
        self.id = id
        self.name = name
        self.creator_id = creator_id
        self.posting_date = posting_date
        self.composition_type = composition_type
        self.modifier = modifier
        self.rating = 0
        self.recalculate_rating()

    def recalculate_rating(self):
        self.rating = get_composition_rating(self.id)

    def get_info(self):
        return "id: {0}, " \
                "name: {1}, " \
                "creator_id: {2}, " \
                "posting_date: {3}, " \
                "composition_type: {4}, " \
                "modifier: {5} ".format(self.id, self.name, self.creator_id,
                                        self.posting_date, self.composition_type, self.modifier)

    def __str__(self):
        res = "Composition:" + self.get_info() + ";"
        return res
