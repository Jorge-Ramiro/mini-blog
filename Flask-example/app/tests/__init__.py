import unittest

from app import create_app, db
from app.auth.models import User

# clase base para nuestros test
class BaseTestClass(unittest.TestCase):
    # Esta clase implementa el método setUp(), que se ejecuta justo antes de cada test.
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
            # Creamos un usuario administrador
            BaseTestClass.create_user("admin", "admin@xyz.com", "1111", True)
            # Creamos un usuario invitado
            BaseTestClass.create_user("prueba", "prueba@xyz.com", "1111", False)
    
    # También se implementa el método tearDown(). Básicamente, este método borra las tablas 
    # de la base de datos tras finalizar cada test.
    def tearDown(self) -> None:
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, email, password, is_admin):
        user = User(name, email)
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user
    
    def login(self, email, password):
        return self.client.post("/login", data= dict(
            email=email,
            password=password
        ), follow_redirects=True)