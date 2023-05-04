import os
from flask import flash
from flask_citas_dojo.config.mysqlconnection import connectToMySQL
from flask_citas_dojo.models import modelo_base
from flask_citas_dojo.models import usuarios
from flask_citas_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Favorita(modelo_base.ModeloBase):

    modelo = 'favoritas'
    campos = ['id_cita', 'id_usuario']

    def __init__(self, data):
        self.id_cita = data['id_cita']
        self.id_usuario = data['id_usuario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def delete_favorita(cls,data):

        query = 'DELETE FROM favoritas WHERE id_cita = %(id_cita)s and id_usuario = %(id_usuario)s'

        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)


        return resultado