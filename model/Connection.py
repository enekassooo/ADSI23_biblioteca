import random
import sqlite3

class Connection:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Connection, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.con = sqlite3.connect("datos.db", check_same_thread=False)
            self.cur = self.con.cursor()
            self.__initialized = True
            self.create_tables_if_not_exist()
        
    def create_tables_if_not_exist(self):
        tables = ["Author", "Book", "User", "User_Book", "Session", "Admin", "Ejemplo"]
        for table in tables:
            if not self.table_exists(table):
                self.create_table(table)

    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        result = self.select(query)
        return len(result) > 0
    
    
 
    
    def create_table(self, table_name):
        
        if table_name == "User_Book":
            self.cur.execute("""
                CREATE TABLE User_Book(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES User(id),
                    FOREIGN KEY(book_id) REFERENCES Book(id)
                )
            """)
        elif table_name == "Admin":
            self.cur.execute("""
            CREATE TABLE Admin(
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES User(id)
            )
        """)

        for _ in range(40):
            user_id = random.randint(1, 4)  # Valores de usuario entre 1 y 4
            book_id = random.randint(1, 300)  # Valores de book_id entre 1 y 300
            self.cur.execute("INSERT INTO User_Book (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        self.cur.execute("INSERT INTO Admin (user_id) VALUES (?)", (1,))
        self.con.commit() 
        

    def select(self, sentence, parameters=None):
        print(f"Ejecutando consulta: {sentence}")
        print(f"Con parámetros: {parameters}")
        if parameters:
            self.cur.execute(sentence, parameters)
        else:
            self.cur.execute(sentence)
        rows = self.cur.fetchall()
        return [x for x in rows]

    def insert(self, sentence, parameters=None):
        if parameters:
            self.cur.execute(sentence, parameters)
        else:
            self.cur.execute(sentence)
        self.con.commit()
        answ = self.cur.rowcount
        return answ

    def update(self, sentence, parameters=None):
        if parameters:
            self.cur.execute(sentence, parameters)
        else:
            self.cur.execute(sentence)
        self.con.commit()

    def delete(self, sentence, parameters=None):
        if parameters:
            self.cur.execute(sentence, parameters)
        else:
            self.cur.execute(sentence)
        answ = self.cur.rowcount
        self.con.commit()
        return answ
