from classes.Composition import *


class Poem(Composition):
    def __init__(self, id, name, creator_id, posting_date, composition_type,
                 modifier, poem_type):
        super().__init__(id, name, creator_id, posting_date, composition_type,
                         modifier)
        self.poem_type = poem_type

    def __str__(self):
        res = "Poem: " + self.get_info() + ", poem_types: " + str(self.poem_type) + ";"
        return res
