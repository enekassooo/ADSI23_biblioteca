from .Connection import Connection

db = Connection()


class Tema:
    def __init__(self, id, title, description, creator):
        self.id = id
        self.title = title
        self.creator = creator
        self.description = description
