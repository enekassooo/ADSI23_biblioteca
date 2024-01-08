# Importamos las librerías necesarias
import os
import sqlite3
from flask import Flask, render_template, request

# Creamos la aplicación Flask
app = Flask(__name__)

# Conectamos con la base de datos
db = sqlite3.connect("datos.db")

# Definimos una función para obtener el usuario actual
def get_current_user():
    # Obtenemos el ID del usuario actual
    user_id = request.cookies.get("user_id")

    # Si el ID del usuario es None, significa que el usuario no está autenticado
    if user_id is None:
        return None

    # Obtenemos los datos del usuario de la base de datos
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", [user_id])
    user = cursor.fetchone()

    return user

# Definimos una función para obtener las solicitudes de amistad pendientes del usuario actual
def get_pending_friend_requests(user):
    # Obtenemos la lista de solicitudes de amistad pendientes
    cursor = db.cursor()
    cursor.execute("SELECT * FROM solicitudes_amistad WHERE usuario_receptor = ?", [user.id])
    solicitudes_amistad = cursor.fetchall()

    return solicitudes_amistad

# Definimos una función para aceptar una solicitud de amistad
def aceptar_solicitud_amistad(user, solicitud_amistad):
    # Actualizamos el estado de la solicitud de amistad a "aceptada"
    cursor = db.cursor()
    cursor.execute("UPDATE solicitudes_amistad SET estado = 'aceptada' WHERE id = ?", [solicitud_amistad.id])
    db.commit()

    # Añadimos el usuario que envió la solicitud de amistad a la lista de amigos del usuario actual
    cursor.execute("INSERT INTO amigos (usuario_1, usuario_2) VALUES (?, ?)", [user.id, solicitud_amistad.usuario_emisor])
    db.commit()

# Definimos una función para rechazar una solicitud de amistad
def rechazar_solicitud_amistad(solicitud_amistad):
    # Eliminamos la solicitud de amistad de la base de datos
    cursor = db.cursor()
    cursor.execute("DELETE FROM solicitudes_amistad WHERE id = ?", [solicitud_amistad.id])
    db.commit()

# Definimos una función para obtener el código de referido del usuario actual
def get_referido_code(user):
    return user.referido_code

# Definimos una función para añadir un referido
def añadir_referido(user, referido_code):
    # Actualizamos el código de referido del usuario actual
    cursor = db.cursor()
    cursor.execute("UPDATE usuarios SET referido_code = ? WHERE id = ?", [referido_code, user.id])
    db.commit()

# Definimos la ruta para el perfil del usuario
@app.route("/perfil")
def perfil():
    # Obtenemos el usuario actual
    user = get_current_user()

    # Si el usuario es None, significa que el usuario no está autenticado
    if user is None:
        return render_template("login.html")

    # Obtenemos las solicitudes de amistad pendientes del usuario
    solicitudes_amistad = get_pending_friend_requests(user)

    # Obtenemos el código de referido del usuario
    referido_code = get_referido_code(user)

    return render_template("perfil.html", user=user, solicitudes_amistad=solicitudes_amistad, referido_code=referido_code)

# Definimos la ruta para gestionar las solicitudes de amistad
@app.route("/perfil/solicitudes-amistad")
def solicitudes_amistad():
    # Obtenemos el usuario actual
    user = get_current_user()

    # Si el usuario es None, significa que el usuario no está autenticado
    if user is None:
        return render_template("login.html")

    # Obtenemos las solicitudes de amistad pendientes del usuario
    solicitudes_amistad = get_pending_friend_requests(user)

    return render_template("solicitudes_
