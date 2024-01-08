<<<<<<< HEAD
from asyncio import current_task
import curses
from datetime import datetime, timedelta  
=======
from flask import request

>>>>>>> 65f5c4ecf976c0366863d56a79b8c0cebbc3f2d4
from model import Connection, Book, User
from model.tools import hash_password
from flask import flash, redirect, url_for

db = Connection()


<<<<<<< HEAD
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False

		return cls.__instance
=======
class LibraryController:
    __instance = None
>>>>>>> 65f5c4ecf976c0366863d56a79b8c0cebbc3f2d4

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
<<<<<<< HEAD
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
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
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None
	def get_recomendaciones(self, user):
		librosleidos = db.select("SELECT book_id FROM User_Book WHERE user_id = ?", (user,))
		recomendaciones = []
		autores_leidos = db.select("SELECT DISTINCT author FROM Book WHERE id IN (SELECT book_id FROM User_Book WHERE user_id = ?)", (user,))
		for autor in autores_leidos:
			libros_recomendados = db.select("SELECT * FROM Book WHERE author = ?", (autor[0],))
			for libro in libros_recomendados:
				autor_info = db.select("SELECT * FROM Author WHERE id = ?", (libro[2],))
				libro_info_list = list(libro)
				libro_info_list.append(autor_info[0][1])
				libro_info = tuple(libro_info_list)
				recomendaciones.append(libro_info)
			
		return recomendaciones




	def get_book(self, titulo, autor, usuario_id):
		# Obtener el ID del autor basado en el nombre
		author_id = db.select("SELECT id FROM Author WHERE name = ?", (autor,))
		self.realizar_devoluciones_60_d(db)
		if author_id and len(author_id) > 0:
			print(f"Author ID: {author_id}, Titulo: {titulo}")
			author_id_scalar = author_id[0][0]
			libr = db.select("SELECT id FROM Book WHERE author = ? AND title = ?", (author_id_scalar, titulo))

			if libr and len(libr) > 0:
				# Verificar si el libro tiene una reserva
				existing_reservations = db.select("SELECT id FROM Reserva WHERE libro_id = ?", (libr[0][0],))

				if not existing_reservations:
					# Añadir una reserva si el libro no tiene una reserva existente
					fecha_actual = datetime.now()
					db.insert("INSERT INTO Reserva (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
							(fecha_actual, None, usuario_id, libr[0][0]))
					
					print("Reserva hecha correctamente")
					#fecha_prue = fecha_actual - timedelta(days=365)
					#db.insert("INSERT INTO Reserva (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
					#		(fecha_prue, None, usuario_id, libr[0][0]))
				else:
					print("El libro ya tiene una reserva.")
			else:
				print("Libro no encontrado.")
		return 


	def devolver_book(self, titulo, autor, usuario_id):
		# Obtener el ID del autor basado en el nombre
		author_id = db.select("SELECT id FROM Author WHERE name = ?", (autor,))
		self.realizar_devoluciones_60_d(db)
		if author_id and len(author_id) > 0:
			print(f"Author ID: {author_id}, Titulo: {titulo}")
			author_id_scalar = author_id[0][0]
			libr = db.select("SELECT id FROM Book WHERE author = ? AND title = ?", (author_id_scalar, titulo))

			if libr and len(libr) > 0:
				# Verificar si el libro tiene una reserva
				existing_reservations = db.select("SELECT * FROM Reserva WHERE libro_id = ?", (libr[0][0],))
				#f_inic = db.select("SELECT fecha_inicio FROM Reserva WHERE libro_id = ?", (libr[0][0],))

				if existing_reservations:
					f_inic = existing_reservations[0][1]
					# Añadir una devolucion
					fecha_actual = datetime.now()
					db.insert("INSERT INTO Devolucion (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
							(f_inic, fecha_actual, usuario_id, libr[0][0]))
					db.delete("DELETE FROM Reserva WHERE libro_id = ?", (libr[0][0],) )
				else:
					print("El libro no lo tienes reservado, no se puede devolver.")
			else:
				print("Libro no encontrado.")
		return None


	def realizar_devoluciones_60_d(self, db):
		# Obtener todas las reservas existentes
		reservas = db.select("SELECT * FROM Reserva")

		for reserva in reservas:
			reserva_id = reserva[0]
			#fecha_i = db.select("SELECT	fecha_inicio FROM Reserva WHERE id = ?",(reserva_id,))
			fecha_i = datetime.strptime(reserva[1], "%Y-%m-%d %H:%M:%S.%f")
			fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			u_id = reserva[3]
			libro_id = reserva[4]
			#u_id = db.select("SELECT usuario_id FROM Reserva WHERE id = ?",(reserva_id,))
			#libro_id = db.select("SELECT libro_id FROM Reserva WHERE id = ?",(reserva_id,))

			# Calcular la cantidad de días transcurridos desde la fecha de inicio
			dias_transcurridos = (datetime.now() - fecha_i).days
	
			# Verificar si han pasado más de 60 días
			if dias_transcurridos > 60:
				# Eliminar automáticamente la reserva
				db.insert("INSERT INTO Devolucion (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
							(fecha_i, fecha_actual, u_id, libro_id))
				db.delete("DELETE FROM Reserva WHERE id = ?", (reserva_id,))
				print(f"Reserva ID {reserva_id} para el libro ID {libro_id} eliminada automáticamente (más de 60 días).")



		'''
		#prueba
		fecha_actual = datetime.now()
		fecha_prue = fecha_actual - timedelta(days=365)
		db.insert("INSERT INTO Reserva (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
				(fecha_prue, None, usuario_id, 9))
		db.insert("INSERT INTO Reserva (fecha_inicio, fecha_fin, usuario_id, libro_id) VALUES (?, ?, ?, ?)",
				(fecha_prue, None, usuario_id, 8))
		#fin_prueba
		'''

	def get_reservas(self, user_id):
		reservas_info = db.select("""
		SELECT Book.*, Reserva.fecha_inicio
		FROM Reserva
		JOIN Book ON Reserva.libro_id = Book.id
		WHERE Reserva.usuario_id = ?
		""", (user_id,))

		return reservas_info
	
	def get_devoluciones(self, user_id):
		devolucion_info = db.select("""
		SELECT Book.*, Devolucion.fecha_fin
		FROM Devolucion
		JOIN Book ON Devolucion.libro_id = Book.id
		WHERE Devolucion.usuario_id = ?
		""", (user_id,))

		return devolucion_info
=======
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
>>>>>>> 65f5c4ecf976c0366863d56a79b8c0cebbc3f2d4
