from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.message import Message

@app.route("/send_message", methods=['POST'])
def send_message(): 
    #verificar que el usuario inicio sesión 
    if 'user_id' not in session:
        return redirect("/")
    #verificar que la info sea correcta 
    '''
     if not Message.strip():
        flash("El mensaje no puede estar vacio", "message")
        return redirect("/dashboard")
    '''
    #guardar el mensaje 
    Message.save(request.form)
    return redirect("/dashboard")

@app.route("/delete_message/<int:id>")
def delete_message(id):
    form = {"id" : id}
    Message.delete_message(form)
    return redirect("/dashboard")

