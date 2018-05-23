from classes.Composition import *


class Prose(Composition):
    def __init__(self, id, name, creator_id, posting_date, composition_type,
                 modifier, prose_type):
        super().__init__(id, name, creator_id, posting_date, composition_type,
                         modifier)
        self.prose_type = prose_type

    def __str__(self):
        res = "Prose: " + self.get_info() + ", prose_types: " + str(self.prose_type) + ";"
        return res
