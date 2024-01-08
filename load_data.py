import hashlib
import sqlite3
import json

salt = "library"


con = sqlite3.connect("datos.db")
cur = con.cursor()


### Create tables
cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
		email varchar(30),
		password varchar(32)
	)
""")
cur.execute("""
    CREATE TABLE User_Book(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES User(id),
        FOREIGN KEY(book_id) REFERENCES Book(id)
    )
""")
cur.execute("""
	CREATE TABLE Admin(
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES User(id)
    )
""")
cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
""")
cur.execute("""
    CREATE TABLE Reserva (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_inicio DATE,
        fecha_fin DATE,
        usuario_id INTEGER,
        libro_id INTEGER,  
        FOREIGN KEY(usuario_id) REFERENCES User(id),
        FOREIGN KEY(libro_id) REFERENCES Book(id)  
    )
""")
cur.execute("""
    CREATE TABLE Devolucion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_inicio DATE,
        fecha_fin DATE,
        usuario_id INTEGER,
        libro_id INTEGER,  
        FOREIGN KEY(usuario_id) REFERENCES User(id),
        FOREIGN KEY(libro_id) REFERENCES Book(id)  
    )
""")

cur.execute("DROP TABLE IF EXISTS User_Book")


### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros:
	res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	if res.rowcount == -1:
		cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
		con.commit()
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	author_id = res.fetchone()[0]

	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, cover, description.strip()))

	con.commit()



