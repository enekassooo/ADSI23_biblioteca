from flask import request

from model import Connection, Book, User
from model.tools import hash_password

db = Connection()


class LibraryController:
    __instance = None

    def _new_(cls):
        if cls.__instance is None:
            cls._instance = super(LibraryController, cls).__new_(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def search_books(self, title="", author="", limit=6, page=0):
        count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
        res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit * page))
        books = [
            Book(b[0], b[1], b[2], b[3], b[4])
            for b in res
        ]
        return books, count

    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_recomendaciones(self, user):
        librosleidos = db.select("SELECT book_id FROM User_Book WHERE user_id = ?", (user,))
        recomendaciones = []
        autores_leidos = db.select(
            "SELECT DISTINCT author FROM Book WHERE id IN (SELECT book_id FROM User_Book WHERE user_id = ?)", (user,))
        for autor in autores_leidos:
            libros_recomendados = db.select("SELECT * FROM Book WHERE author = ?", (autor[0],))
            for libro in libros_recomendados:
                autor_info = db.select("SELECT * FROM Author WHERE id = ?", (libro[2],))
                libro_info_list = list(libro)
                libro_info_list.append(autor_info[0][1])
                libro_info = tuple(libro_info_list)
                recomendaciones.append(libro_info)

        return recomendaciones

    def añadir_usuario(self, nombre, email, contraseña):
        db.insert("INSERT INTO User(name, email, password) VALUES (?, ?, ?)", (nombre, email, contraseña))
        return

    def eliminar_usuario(self, userid):
        db.delete("DELETE FROM User WHERE id = ?", (userid,))
        print(f"User con ID {userid} eliminado correctamente")
        return
    def añadir_libro(self, titulo, autor, portada, desc):
        db.insert("INSERT INTO Book(title, author, cover, description) VALUES (?, ?, ?, ?)",
                  (titulo, autor, portada, desc))
        return

    def eliminar_libro(self, libroid):
        db.delete("DELETE FROM Book WHERE id = ?", (libroid,))
        print(f"Libro con ID {libroid} eliminado correctamente")
        return

    def es_admin(self, user_id):
        result = db.select("SELECT * FROM User u JOIN Admin a ON u.id = a.user_id WHERE u.id = ?", (user_id,))
        es_administrador = bool(result)
        return es_administrador

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