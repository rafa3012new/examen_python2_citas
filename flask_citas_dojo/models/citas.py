import os
from flask import flash
from flask_citas_dojo.config.mysqlconnection import connectToMySQL
from flask_citas_dojo.models import modelo_base
from flask_citas_dojo.models import usuarios
from flask_citas_dojo.models import favoritas
from flask_citas_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Cita (modelo_base.ModeloBase):

    modelo = 'citas'
    campos = ['autor', 'mensaje', 'publicador']

    def __init__(self, data):
        self.id = data['id']
        self.autor = data['autor']
        self.mensaje = data['mensaje']
        self.publicador = data['publicador']
        self.nombre_publicador = data['nombre_publicador'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favoritas = []


    # #si da tiempo
    # @classmethod
    # def buscar(cls, dato):
    #     query = "select * from citas where id = %(dato)s"
    #     data = { 'dato' : dato }
    #     results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

    #     if len(results) < 1:
    #         return False
    #     return cls(results[0])


    #si da tiempo
    @classmethod
    def update(cls,data):
        query = 'UPDATE citas SET autor = %(autor)s, mensaje = %(mensaje)s, publicador = %(publicador)s WHERE id = %(id)s;'
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return resultado


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del campo {campo} no puede ser menor o igual a {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):


        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid


        if 'autor' in data:
            is_valid = cls.validar_largo(data, 'autor', 2)
            if is_valid == False: no_create = False

        if 'mensaje' in data:
            is_valid = cls.validar_largo(data, 'mensaje', 10)
            if is_valid == False: no_create = False



        return no_create

    @classmethod
    def get_all_citas_menos_favoritas(cls,data):


        #SE ARMA LA CONSULTA
        query = "select *, CONCAT(u.nombre, ' ', u.apellido) as nombre_publicador from citas c left join usuarios u on c.publicador = u.id where c.id not in (select id_cita from favoritas where id_usuario = %(id_usuario)s);"


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)
        

        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        citas = []
        for result in results:
            citas.append(cls(result))

        return citas


    @classmethod
    def get_all_citas_favoritas(cls,data):


        #SE ARMA LA CONSULTA
        query = "select *, CONCAT(u.nombre, ' ', u.apellido) as nombre_publicador from citas c left join usuarios u on c.publicador = u.id where c.id in (select id_cita from favoritas where id_usuario = %(id_usuario)s);"


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)



        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        citas = []
        for result in results:
            citas.append(cls(result))

        return citas



    @classmethod
    def get_all_mis_citas(cls,data):

        #SE ARMA LA CONSULTA
        query = "select *,CONCAT(u.nombre, ' ', u.apellido) as nombre_publicador from citas c left join usuarios u on c.publicador = u.id where c.publicador = %(id_usuario)s;"


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)


        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        citas = []
        for result in results:
            citas.append(cls(result))

        return citas

