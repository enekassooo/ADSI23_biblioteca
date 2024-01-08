from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'datos.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, historial_reservas TEXT, reseñas TEXT, amigos TEXT, referidos TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil/<int:usuario_id>')
def perfil(usuario_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
    usuario = c.fetchone()
    conn.close()
    return render_template('perfil.html', usuario=usuario)

@app.route('/recomendaciones_amigos/<int:usuario_id>', methods=['GET', 'POST'])
def recomendaciones_amigos(usuario_id):
    if request.method == 'POST':
        # Procesar solicitud de amistad (aceptar o rechazar)
        # Actualizar la base de datos y la lista de amistades del usuario

    # Obtener lista de recomendaciones de amigos
    return render_template('recomendaciones_amigos.html', usuario_id=usuario_id)

@app.route('/referidos/<int:usuario_id>', methods=['GET', 'POST'])
def referidos(usuario_id):
    if request.method == 'POST':
        if 'agregar_referente' in request.form:
            # Procesar la adición de un referente
            # Actualizar la base de datos con el nuevo referido

    # Obtener información de referidos
    return render_template('referidos.html', usuario_id=usuario_id)

if __name__ == '__main__':
    app.run(debug=True)
