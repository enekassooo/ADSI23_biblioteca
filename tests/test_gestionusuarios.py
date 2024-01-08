from . import BaseTestClass
from bs4 import BeautifulSoup
class TestGestionUsuarios(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_gestion_usuarios(self):

        resultado = self.app.get('/gestionusuarios')
        self.assertEqual(200, resultado.status_code)
        self.assertIn(b'gestorusuarios.html', resultado.data)

    def test_post_eliminar_usuario(self):

        datos_usuario = {
            'id': '?'
        }
        resultado = self.app.post('/gestionusuarios', data=datos_usuario)
        self.assertEqual(200, resultado.status_code)
        self.assertIn(b'Se ha eliminado el usuario', resultado.data)

    def test_post_añadir_usuario(self):

        datos_usuario = {
            'nombre': '?',
            'email': '?',
            'contraseña': '?'
        }
        resultado = self.app.post('/gestionusuarios', data=datos_usuario)
        self.assertEqual(200, resultado.status_code)
        self.assertIn(b'Se ha añadido el usuario correctamente', resultado.data)


