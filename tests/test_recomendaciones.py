from . import BaseTestClass
from bs4 import BeautifulSoup

class TestRecomendaciones(BaseTestClass):

    def test_recomendaciones_pagina_autenticado(self):
        # Supongamos que ya estás autenticado con un usuario
        resultado = self.client.get('/recomendaciones')
        self.assertEqual(200, resultado.status_code)
        self.assertIn('Recomendaciones', resultado.get_data(as_text=True))
        

    def test_recomendaciones_pagina_no_autenticado(self):
        # Si el usuario no está autenticado, debe redirigirlo a la página de inicio de sesión
        resultado = self.client.get('/recomendaciones', follow_redirects=True)
        self.assertEqual(200, resultado.status_code)  
        self.assertIn('Login', resultado.get_data(as_text=True))  

    def test_recomendaciones_funciona(self):
        # Supongamos que ya estás autenticado con un usuario
        resultado = self.client.get('/recomendaciones')
        self.assertEqual(200, resultado.status_code)
        # Verifica que la página contiene recomendaciones y otros elementos esperados
        pagina = BeautifulSoup(resultado.data, features="html.parser")
        recomendaciones = pagina.find_all('div', class_='recomendacion')
        self.assertGreater(len(recomendaciones), 0)  

    def test_recomendaciones_no_ha_leido(self):
        # Prueba cuando el usuario no tiene libros en su biblioteca
        # Supongamos que ya estás autenticado con un usuario que no tiene libros
        resultado = self.client.get('/recomendaciones')
        self.assertEqual(200, resultado.status_code)
        
    def test_recomendaciones_no_identificado(self):
        # Prueba cuando no hay usuario autenticado
        self.logout()
        resultado = self.client.get('/recomendaciones', follow_redirects=True)
        self.assertEqual(200, resultado.status_code)

    def test_recomendaciones_post(self):
        # Prueba el comportamiento ante una solicitud POST 
        resultado = self.client.post('/recomendaciones')
        self.assertEqual(405, resultado.status_code) 