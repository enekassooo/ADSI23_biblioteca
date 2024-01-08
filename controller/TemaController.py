from model.Tema import Tema
from model.Connection import Connection

db = Connection()


class TemaController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TemaController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def search_temas(self, title="", limit=6, page=0):
        count = db.select(
            "SELECT count() FROM Tema WHERE title LIKE ?",
            (f"%{title}%",),
        )[0][0]

        res = db.select(
            "SELECT * FROM tema t WHERE title LIKE ? LIMIT ? OFFSET ?",
            (f"%{title}%", limit, limit * page),
        )
        temas = [Tema(t[0], t[1], t[2], t[3]) for t in res]
        return temas, count

    def get_tema_details(self, tema_id):
        res = db.select("SELECT * FROM tema WHERE id = ?", (tema_id,))
        print("AQUII")
        print(res)
        tema = Tema(res[0], res[1], res[2], res[3])
        return tema
