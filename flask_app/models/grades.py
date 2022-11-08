from flask_app.config.mysqlconnection import connectToMySQL #Importación de la conexión con bd
from flask import flash #flash es el encargado de enviar mensajes/errores

from datetime import datetime #Manipular fechas

class Grade:

    def __init__(self, data):
        #data = Diccionario con todas las columnas de grade
        self.id = data['id']
        self.alumno = data['alumno']
        self.stack = data['stack']
        self.fecha = data['fecha']
        self.calificacion = data['calificacion']
        self.cinturon = data['cinturon']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @staticmethod
    def valida_calificacion(formulario):
        es_valido = True

        if formulario['alumno'] == '':
            flash('Alumno no puede ser vacío', 'grades')
            es_valido = False
        
        if formulario['calificacion'] == '':
            flash('Ingresa una calificación', 'grades')
            es_valido = False
        else:
            if int(formulario['calificacion']) < 1 or int(formulario['calificacion']) > 10:
                flash('Calificación debe ser entre 1 y 10', 'grades')
                es_valido = False
        
        if formulario['fecha'] == '':
            flash('Ingrese una fecha', 'grades')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['fecha'], '%Y-%m-%d') #Estamos transformando un texto a formato de fecha
            hoy = datetime.now() #Me da la fecha de hoy
            if hoy < fecha_obj:
                flash('La fecha debe ser en pasado', 'grades')
                es_valido = False
        
        return es_valido
    

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO grades (alumno, stack, fecha, calificacion, cinturon, user_id) VALUES (%(alumno)s, %(stack)s, %(fecha)s, %(calificacion)s, %(cinturon)s, %(user_id)s)"
        result = connectToMySQL('beltreviewer').query_db(query, formulario)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM grades"
        results = connectToMySQL('beltreviewer').query_db(query) #Lista de Diccionarios

        grades = []
        for grade in results:
            #grade = Diccionario con todas las columnas y valores de grades
            grades.append(cls(grade)) #1.- cls(grade) crea una instancia en base al diccionario 2.- grades.append() me agrega esa instancia a la lista de calificaciones
        
        return grades