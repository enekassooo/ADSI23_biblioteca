from flask import Flask, render_template, request, make_response, redirect, g
from .TemaController import TemaController
from controller.LibraryController import LibraryController

from model import Connection, Book, User

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')

library = LibraryController()
foro_controller = TemaController()

@app.before_request
def get_logged_user():
    if '/css' not in request.path and '/js' not in request.path:
        token = request.cookies.get('token')
        time = request.cookies.get('time')
        if token and time:
            request.user = library.get_user_cookies(token, float(time))
            if request.user:
                request.user.token = token
                g.user = request.user


@app.after_request
def add_cookies(response):
    if 'user' in dir(request) and request.user and request.user.token:
        session = request.user.validate_session(request.user.token)
        response.set_cookie('token', session.hash)
        response.set_cookie('time', str(session.time))
    return response


@app.route('/')
def index():
    user = getattr(request, 'user', None)
    if user is None:
        return render_template('index.html')

    admin = library.es_admin(user.id)
    if admin:
        return render_template('indexadmin.html')
    else:
        return render_template('index.html')


@app.route('/catalogue')
def catalogue():
    title = request.values.get("title", "")
    author = request.values.get("author", "")
    page = int(request.values.get("page", 1))
    books, nb_books = library.search_books(title=title, author=author, page=page - 1)
    total_pages = (nb_books // 6) + 1
    return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
                           total_pages=total_pages, max=max, min=min)


@app.route('/recomendaciones')
def recomendaciones():
    user = request.user.identity()
    print("El usuario es:", user)
    recomended_books = library.get_recomendaciones(user)
    print("Recomendaciones:", recomended_books)
    return render_template('recomendaiones.html', rbooks=recomended_books)


@app.route('/gestionLibros', methods=['GET', 'POST'])
def gestionLibros():
    if request.method == 'POST':
        libroid = request.form.get("id", "")
        if libroid:
            library.eliminar_libro(libroid)
            print(f"Se ha eliminado el libro con ID {libroid}")
        else:
            print(f"No se va a borrar un libro")

        titulo = request.form.get("titulo", "")
        autor = request.form.get("autor", "")
        portada = request.form.get("portada", "")
        desc = request.form.get("descripcion", "")
        if titulo and autor and desc:
            library.añadir_libro(titulo, autor, portada, desc)
            print("Se ha añadido el libro correctamente")

    return render_template('gestionlibros.html')


@app.route('/gestionusuarios', methods=['GET', 'POST'])
def gestionUsuarios():
    if request.method == 'POST':
        userid = request.form.get("id", "")
        if userid:
            library.eliminar_usuario(userid)
            print(f"Se ha eliminado el usuario con ID {userid}")
        else:
            print(f"No se va a borrar el usuario")

        nombre = request.form.get("nombre", "")
        email = request.form.get("email", "")
        contraseña = request.form.get("contraseña", "")
        if nombre and email and contraseña:
            library.añadir_usuario(nombre, email, contraseña)
            print("Se ha añadido el usuario correctamente")

    return render_template('gestorusuarios.html')



@app.route('/reserva', methods=['GET', 'POST'])
def reservas():
    # Obtener el id del usuario desde la sesión
    user_id = request.user.identity()
    reserv = library.get_reservas(user_id)
    print("la lista es" ,reserv)

    if request.method == 'POST':
        # Si es una solicitud POST, obtener los datos del formulario
        titulo_libro = request.form['titulo_libro']
        autor_libro = request.form['autor_libro']

        # Obtener información del libro y crear la reserva si existe
        libro_info = library.get_book(titulo_libro, autor_libro, user_id)

        return render_template('reserva.html', libro_info=libro_info)
    
    # Renderizar la plantilla reserva.html si el método no es POST
    return render_template('reserva.html', lista_reserv=reserv)



@app.route('/devolver', methods=['GET', 'POST'])
def devolver():
    # Obtener el id del usuario desde la sesión
    user_id = request.user.identity()
    devolucion = library.get_devoluciones(user_id)
    print("la lista es" ,devolucion)
    if request.method == 'POST':
        # Si es una solicitud POST, obtener los datos del formulario
        titulo_libro = request.form['titulo_libro']
        autor_libro = request.form['autor_libro']

        # Obtener información del libro y crear devolución
        libro_info = library.devolver_book(titulo_libro, autor_libro, user_id)

        return render_template('devolver.html', libro_info=libro_info)

    # Renderizar la plantilla devoluciona.html si el método no es POST
    return render_template('devolver.html', lista_devoluciones = devolucion)




@app.route('/gestionlibros')
def gestionlibros():
	return render_template('gestionlibros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in dir(request) and request.user and request.user.token:
        return redirect('/')
    email = request.values.get("email", "")
    password = request.values.get("password", "")
    user = library.get_user(email, password)
    if user:
        session = user.new_session()
        resp = redirect("/")
        resp.set_cookie('token', session.hash)
        resp.set_cookie('time', str(session.time))
    else:
        if request.method == 'POST':
            return redirect('/login')
        else:
            resp = render_template('login.html')
    return resp


@app.route('/logout')
def logout():
    path = request.values.get("path", "/")
    resp = redirect(path)
    resp.delete_cookie('token')
    resp.delete_cookie('time')
    if 'user' in dir(request) and request.user and request.user.token:
        request.user.delete_session(request.user.token)
        request.user = None
        resp = render_template('index.html')
    return resp

@app.route("/foro")
def foro():
    title = request.values.get("title", "")
    # creator = request.values.get("creator", "")
    page = int(request.values.get("page", 1))
    temas, nb_temas = foro_controller.search_temas(title=title, page=page - 1)
    total_pages = (nb_temas // 6) + 1
    return render_template(
        "foro.html",
        temas=temas,
        title=title,
        # creator=creator,
        current_page=page,
        total_pages=total_pages,
        max=max,
        min=min,
    )

@app.route("/foro/<int:tema_id>")
def tema_detail(tema_id):
    tema = foro_controller.get_tema_details(tema_id)
    return render_template("detail.html", tema=tema)
