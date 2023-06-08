import os
from app import create_app
from flask import send_from_directory

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

"""
¡ATENCIÓN! Debido a temas de rendimiento, los recursos estáticos (hojas de estilo, javascript, imágenes, …) 
deben ser servidos por un servidor web, como NGINX o Apache, o desde un CDN. 
Lo que aquí te voy a contar es solamente informativo y para ser usado con el servidor de pruebas que incorpora Flask. 
En la siguiente lección veremos cómo servir los recursos estáticos desde un servidor de producción.
"""
@app.route('/media/posts/<filename>')
def media_posts(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['POSTS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)
