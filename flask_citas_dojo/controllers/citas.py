import os
from flask import redirect, render_template, request, flash, session, url_for, Blueprint
from flask_citas_dojo import app
from flask_bcrypt import Bcrypt
from flask_citas_dojo.models.usuarios import Usuario
from flask_citas_dojo.models.citas import Cita
from flask_citas_dojo.models.favoritas import Favorita
from datetime import datetime, timedelta

citas = Blueprint('citas', __name__)

bcrypt = Bcrypt(app)



@citas.route("/editarcita/<id>")
def editarcita(id):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    datos_cita = Cita.get_by_id(int(id))
    datos_cita = datos_cita[0]



    if 'rollback_autor' in session:
        data = {
        'id':id,
        'autor':session['rollback_autor'],
        'mensaje':session['rollback_mensaje'],
        }
        session.pop('rollback_autor')
        session.pop('rollback_mensaje')
    else:

        data = {
         'id':id,
         'autor':datos_cita['autor'],
         'mensaje':datos_cita['mensaje'],
        }


    return render_template('form.html',datos_cita=data)



@citas.route("/procesar_cita", methods=["POST"])
def procesar_cita():


    data ={
            'autor':request.form['autor'],
            'mensaje':request.form['mensaje'],
            'publicador':int(session['idusuario'])
           }


    validar = Cita.validar(data)

    if not validar:
        if request.form['operacion'] == 'Nueva Cita':
            session['rollback_autor'] = request.form['autor']
            session['rollback_mensaje'] = request.form['mensaje']
            return redirect('/')

        if request.form['operacion'] == 'Editar Cita':
            session['rollback_autor'] = request.form['autor']
            session['rollback_mensaje'] = request.form['mensaje']
            return redirect('/citas/editarcita/'+str(request.form['id']))


    try:
        if request.form['operacion'] == 'Nueva Cita':
            Cita.save(data)

        if  request.form['operacion'] == 'Editar Cita':
            data['id'] = int(request.form['id'])
            Cita.update(data)
        
        flash("Datos de Cita almacenada con exito!","success")
        print("cita guardado con exito!",flush=True)
    except Exception as error:
        print(f"error al guardar el cita, valor del error : {error}",flush=True)

    return redirect('/')


@citas.route("/agregarfavoritas/<id>")
def agregarfavoritas(id):

    data={
       'id_usuario':int(session['idusuario']),
       'id_cita':int(id)
         }

    Favorita.save(data)

    return redirect('/')


@citas.route("/removerfavoritas/<id>")
def removerfavoritas(id):

    data={
       'id_usuario':int(session['idusuario']),
       'id_cita':int(id)
         }

    Favorita.delete_favorita(data)

    return redirect('/')


@citas.route("/detallecita/<id_publicador>")
def detalle_cita(id_publicador):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    data = {"id_usuario":int(id_publicador)
            }

    datos_cita = Cita.get_all_mis_citas(data)
    

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template('detail.html',sistema=nombre_sistema,mis_citas=datos_cita)


@citas.route("/eliminarcita/<id>")
def eliminarcita(id):
    

    try:
        Cita.delete(int(id))
        flash('Se elimino el cita con exito','success')
        print(f"Eliminacion de cita con exito {id}",flush=True)
    except Exception as error:
        print("error al eliminar la cita",flush=True)

    return redirect('/')