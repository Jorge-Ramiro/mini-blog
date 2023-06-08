from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model, UserMixin):

    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return db.session.get(User, id) # this code is legacy -> User.query.get(id)

    # Se ha sustituido la función get_user(email) por el método estático get_by_email(email) de la clase User.
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return User.query.all()
    
    # Método que permite obtener el número total de post que hay publicados
    @staticmethod
    def get_count_all():
        return User.query.count()