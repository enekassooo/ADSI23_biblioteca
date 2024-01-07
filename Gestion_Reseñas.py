import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('datos.db')
cursor = conn.cursor()

# Crear tabla de libros si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        autor TEXT,
        reseña TEXT
    )
''')
conn.commit()

# Crear tabla de usuarios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre_usuario TEXT,
        contraseña TEXT
    )
''')
conn.commit()

# Crear tabla de historial de préstamos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS historial_prestamos (
        id INTEGER PRIMARY KEY,
        id_usuario INTEGER,
        id_libro INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
        FOREIGN KEY (id_libro) REFERENCES libros(id)
    )
''')
conn.commit()

# Función para agregar o actualizar reseñas
def agregar_resena(id_libro, id_usuario, reseña):
    cursor.execute('SELECT * FROM libros WHERE id = ?', (id_libro,))
    libro = cursor.fetchone()

    if libro:
        cursor.execute('SELECT * FROM historial_prestamos WHERE id_usuario = ? AND id_libro = ?', (id_usuario, id_libro))
        prestamo = cursor.fetchone()

        if prestamo:
            cursor.execute('SELECT * FROM libros WHERE id = ?', (id_libro,))
            libro_actualizado = cursor.fetchone()
            
            if libro_actualizado[3]:
                # Si ya tiene una reseña, actualizarla
                cursor.execute('UPDATE libros SET reseña = ? WHERE id = ?', (reseña, id_libro))
            else:
                # Si no tiene una reseña, agregar una nueva
                cursor.execute('UPDATE libros SET reseña = ? WHERE id = ?', (reseña, id_libro))

            conn.commit()
            print('Reseña agregada o actualizada con éxito.')
        else:
            print('El usuario no ha prestado este libro.')
    else:
        print('Libro no encontrado.')

# Ejemplo de uso
# Supongamos que el usuario con ID 1 (ya logueado) quiere agregar o actualizar la reseña del libro con ID 3
# agregar_resena(3, 1, '¡Un libro increíble! Lo recomiendo.')
