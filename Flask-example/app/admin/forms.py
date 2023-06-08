from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)], id="floatingTitle")
    content = TextAreaField('Contenido', id="floatingContent")
    post_image = FileField('Imagen de cabecera', validators=[FileAllowed(['jpg', 'png'], 'Sólo permiten imágenes')],
                            id="formFile") # Permite elegir que tipos de archivos se permiten
    submit = SubmitField('Enviar')

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')