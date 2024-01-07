
from flask import Flask, render_template, request, make_response, redirect, g

from controller.LibraryController import LibraryController
from model import Connection, Book, User

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


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


def admin():

	user_id = request.user.identity()


	query = "SELECT * FROM User u JOIN Admin a ON u.id = a.user_id WHERE u.id = ?"
	result = db.select_one(query, (user_id,))


	es_administrador = result is not None

	return render_template('index.html', es_administrador=es_administrador)
@app.route('/gestionLibros')
def gestionLibros():
	libro = library.añadir_libro()
	print("Se ha añadido el usuario correctamente")
	return render_template('gestionlibros.html', book=libro)


@app.route('/gestionUsuarios')
def gestionUsuarios():
	usuario = library.añadir_usuario()
	print("Se ha añadido el usuario correctamente")
	return render_template('gestionUsuarios.html', user=usuario)



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
