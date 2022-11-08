from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importar los modelos
from flask_app.models.users import User
from flask_app.models.grades import Grade

@app.route('/new/grade')
def new_grade():
    #Revisamos que ya inició sesión la persona
    if 'user_id' not in session:
        return redirect('/')
    
    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id te regrese un objeto de usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #Recibir una instancia de usuario en base a su ID

    return render_template('new_grade.html', user=user)

@app.route('/create/grade', methods=['POST'])
def create_grade():
    #Revisar si ya inició sesión mi usuario
    if 'user_id' not in session:
        return redirect('/')
    
    #Validar que la información de Calificación este correcta
    if not Grade.valida_calificacion(request.form):
        return redirect('/new/grade')

    #Guardar calificación
    Grade.save(request.form)

    #Redirijo a dashboard
    return redirect('/dashboard')