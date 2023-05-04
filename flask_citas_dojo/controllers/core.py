import os
from flask import redirect, render_template, request, flash, session, url_for
from flask_citas_dojo import app
from flask_bcrypt import Bcrypt
from flask_citas_dojo.models.usuarios import Usuario
from flask_citas_dojo.models.citas import Cita
from flask_citas_dojo.models.favoritas import Favorita
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    datos_todas_citas = []
    datos_favoritas_citas = []

    if 'idusuario' in session:
        data = {
            "id_usuario":int(session['idusuario'])
            }
        datos_todas_citas = Cita.get_all_citas_menos_favoritas(data)
        datos_favoritas_citas = Cita.get_all_citas_favoritas(data)

    if 'rollback_autor' in session:
        data_form = {
        'autor':session['rollback_autor'],
        'mensaje':session['rollback_mensaje'],
        }
        session.pop('rollback_autor')
        session.pop('rollback_mensaje')
    else:
        data_form = {
        'autor':'',
        'mensaje':'',
        }

    return render_template("main.html", sistema=nombre_sistema, todas_citas = datos_todas_citas, citas_favoritas = datos_favoritas_citas, datos_form = data_form)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    #validaciones del objeto usuario
    if not Usuario.validar(request.form):
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['password_reg'])

    data = {
        'usuario' : request.form['user'],
        'nombre' : request.form['name'],
        'apellido' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido


    return redirect('/')

@app.route('/logout')
def logout():
    print("log out!")
    session.clear()
    return redirect('/login')