import os

from flask import request, redirect, render_template,session, flash
from flask_base import app
from flask_base.models.newsletter import Category
from flask_base.models.reader import Reader
from flask_base.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/reader/create", methods = ['POST'])
def create_reader():
    if not Reader.validate_reader(request.form):
        return redirect("/reader/register")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user': request.form['user'],
        'password': pw_hash
    }

    user_id = User.save_user(data)
    reader_data = {
        'subscription': request.form['subscription'],
        'user_id' :user_id
    }
    reader_id = Reader.save_reader(reader_data)

    flash("Lector creado, gracias! :)", "register")
    session['reader_id'] = reader_id 
    return redirect("/reader/register")

# Renderiza pagina de login/register
@app.route("/reader/register")
def form_reader():
    return render_template("loginreader.html")

# Procesamiento de login
@app.route ("/reader/login", methods = ['POST'])
def login_reader():
    data = {
        "email" : request.form["email"]
    }
    reader_db = Reader.get_login(data)
    if not reader_db:
        flash("Email/contraseña incorrectos", "login")
        return redirect("/reader/register")

    if not bcrypt.check_password_hash(reader_db.password, request.form['password']):
        flash("Email/contraseña incorrectos", "login")
        return redirect("/reader/register")
    
    session['reader_id'] = reader_db.id
    return redirect("/reader/dashboard")

##Dashboard o perfil con info del lector
@app.route("/reader/dashboard")
def dash_reader():
    if 'reader_id' not in session:
        return redirect("/reader/register")
    data = {
        "id" : session['reader_id']
    }

    reader = Reader.get_reader_profile(data)
    all_categories = Category.load_categories()
    return render_template("dashreader.html", reader = reader, all_categories = all_categories) 


