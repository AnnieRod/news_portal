from flask import request, redirect, render_template,session, flash
from flask_base import app
from flask_base.models.journalist import Journalist
from flask_base.models.newsletter import Category, Newsletter
from flask_base.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

## Home
# @app.route("/")
# def start_page():
#     return render_template("index.html", all_categories = Category.load_categories())


## Crea usuario de base para luego tomar su id y crear PERIODISTA
@app.route("/journalist/create", methods = ['POST'])
def create_user():
    if not Journalist.validate_journalist(request.form):
        return redirect("/journalist/register")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user': request.form['user'],
        'password': pw_hash
    }

    user_id = User.save_user(data)
    jour_data = {
        'credential': request.form['credential'],
        'user_id' :user_id
    }
    journalist_id = Journalist.save_journalist(jour_data)

    flash("Periodista creado, gracias! :)", "register")
    session['journalist_id'] = journalist_id 
    return redirect("/journalist/register")

# Renderiza pagina de login/register
@app.route("/journalist/register")
def form_journalist():
    return render_template("loginjournal.html")

# Procesamiento de login
@app.route ("/journalist/login", methods = ['POST'])
def login_journalist():
    data = {
        "email" : request.form["email"]
    }
    journalist_db = Journalist.get_login(data)
    if not journalist_db:
        flash("Email/contraseña incorrectos", "login")
        return redirect("/journalist/register")

    if not bcrypt.check_password_hash(journalist_db.password, request.form['password']):
        flash("Email/contraseña incorrectos", "login")
        return redirect("/journalist/register")
    
    session['journalist_id'] = journalist_db.id
    return redirect("/journalist/dashboard")

##Dashboard o perfil con info del periodista
@app.route("/journalist/dashboard")
def dash_journalist():
    if 'journalist_id' not in session:
        return redirect("/journalist/register")
        
    data = {
        "id" : session['journalist_id']
    }
    
    journalist = Journalist.get_creator_profile(data)
    news = Newsletter.news_by_id(data)
    last = Newsletter.get_last_published(data)
    all_categories = Category.load_categories()
    all_news= Newsletter.news_by_author(data)

    return render_template("dashjournal.html", journalist = journalist, news = news, all_categories = all_categories, last = last, all_news = all_news)