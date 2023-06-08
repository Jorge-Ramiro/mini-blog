import datetime, pytz
from slugify import slugify
from sqlalchemy.exc import IntegrityError


from app import db

time_zone = datetime.datetime.now(pytz.timezone("Etc/GMT+6"))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=time_zone)
    image_name = db.Column(db.String(256))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='asc(Comment.created)') # añadimos una relación con la tabla comment, llamada comments para que desde un post podamos acceder de manera sencilla a su listado de comentarios.

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f"{slugify(self.title)}-{count}"

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return Post.query.all()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return db.session.get(Post, id) # Post.query.get(id) código legacy
    
    # Método que permite paginar las consultas a las tablas limitando el número de registros por página.
    @staticmethod
    def all_paginated(page=1, per_page=20):
        # ordenamos por nombre de titulo de a-z y por fecha de creación reciente-antigua
        return Post.query.order_by(Post.title.asc(), Post.created.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Método que permite obtener el número total de post que hay publicados
    @staticmethod
    def get_count_all():
        return Post.query.count()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='SET NULL'))
    user_name = db.Column(db.String(80))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=time_zone)

    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()