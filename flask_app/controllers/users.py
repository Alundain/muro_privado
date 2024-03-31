from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
#importamos todos los modelos
from flask_app.models.user import User
from flask_app.models.message import Message
# importar contraseña
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
    
# encriptar de una contraseña
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form ={
    "first_name": request.form['first_name'],
    "last_name" : request.form['last_name'],
    "email" : request.form['email'],
    "password": pass_encrypt
    }
    new_id = User.save(form)
    session['user_id'] = new_id
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    form = {"id": session['user_id']} # este form tiene el id del usuario y ls sessiom y se necesits psrs identificsr de quien son los mensajes
    user = User.get_by_id(form)
    #obtener lista con todos los usuarios
    all_users = User.get_all()

    #obtener una lista con todos los mensajes (antes debo importar models messages)
    messages = Message.get_my_messages(form)
    #obtener cantidad de mensajes enviados
    cantidad = Message.sent_messages(form)

    return render_template("dashboard.html", user=user, all_users=all_users, messages = messages, cantidad = cantidad)

@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Email no registrado", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")    