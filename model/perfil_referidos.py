from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from tools import hash_password 

app = Flask(__name__)

def get_usuario_autenticado():
    user_id = session.get('user_id')
    if user_id:
        return User.get_by_id(user_id)
    return None

@app.route('/perfil')
def perfil():
    usuario_actual = get_usuario_autenticado()

    if not usuario_actual:
        return redirect(url_for('inicio'))
    usuario = User(usuario_actual.id, "NombreUsuario", "email@ejemplo.com")

    return render_template('perfil.html', usuario=usuario)

@app.route('/referidos', methods=['GET', 'POST'])
def referidos():
    usuario_actual = get_usuario_autenticado()

    if not usuario_actual:
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        referente = request.form['codigo_referente']
        usuario_actual.add_referido(referente)

    return render_template('referidos.html', usuario=usuario_actual)


if __name__ == '__main__':
    app.run(debug=True)
