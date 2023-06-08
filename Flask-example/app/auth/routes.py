from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
from app.common.mail import send_email

# mostrar el formulario y procesarlo
@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))
    # instanciamos un ojteto de la clase SignupForm
    form = SignupForm()
    error = None
    # Al hacer esto pueden ocurrir dos cosas en función de si la petición es GET o POST. 
    # Si el usuario simplemente ha accedido a la página que muestra el formulario de registro (GET), 
    # se crea un objeto con los campos vacíos. Por el contrario, si el usuario ha enviado el formulario (POST), 
    # se crea un objeto con los campos inicializados. El valor de estos campos es el que se envía en el cuerpo 
    # de la petición (recuerda que están en request.form).
    if form.validate_on_submit():
        #if request.method == "POST":
        # Si se ha enviado el formulario, se recupera cada uno de los campos del mismo por medio 
        # del diccionario form del objeto request.
        #name = request.form['name']
        #email = request.form['email']
        #password = request.form['password']

        # nueva forma de obtener los valores utilizando flask-WTF
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f"El email {email} ya esta siendo utilizado por otro usuario"
        else:
            # Creamos al usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            # Enviamos un email de bienvenida
            send_email(subject="Bienvenid@ al miniblog",
                        sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                        recipients=[email, ],
                        text_body=f"Hola {name}, bienvenid@ al miniblog de flask",
                        html_body=f"<p>Hola <strong>{name}</strong>, bienvenid@ al miniblog de Flask</p>")

            # Dejamos al usuario logueado
            login_user(user, remember=True)

            # Comprobamos si se pasó por la URL el parámetro next.
            next_page = request.args.get('next', None)
            # Este parámetro lo usaremos para redirigir al usuario a la página que se indica en el mismo.
            if not next_page or urlsplit(next_page).netloc != "":
                # Si no se especifica, simplemente lo redirigimos a la página de inicio.
                next_page = url_for("public.index")

            # Siempre que se procesa un formulario correctamente, es una buena práctica hacer un redirect para evitar 
            # envíos duplicados de datos si el usuario recarga la página o hace clic en el botón atrás del navegador.
            return redirect(next_page)
    # En caso de que no se haya enviado el formulario, se devuelve como respuesta la página que muestra 
    # el formulario de registro.
    return render_template("auth/signup_form.html", form=form, error=error)

@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    # comprobamos si el usuario actual ya está autenticado.
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    # comprobamos si los datos enviados en el formulario son válidos. 
    # En ese caso, intentamos recuperar el usuario a partir del email con get_user().
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # Si existe un usuario con dicho email y la contraseña coincide, procedemos a autenticar al usuario 
            # llamando al método login_user de Flask-login.
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("public.index")
            return redirect(next_page)
    return render_template("auth/login_form.html", form=form)

@auth_bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))