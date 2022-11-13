import os

from flask import redirect, render_template, request, flash, session
from flask_base import app
from flask_base.models.journalist import Journalist
from flask_base.models.newsletter import Category, Newsletter

@app.route("/")
def index():
    if 'reader_id' and 'journalist_id' not in session:
        last = Newsletter.last_published()
        all_news_user= Newsletter.all_published()
        all_categories = Category.load_categories()
        return render_template("index.html", last = last, all_news_user=all_news_user, all_categories = all_categories)
    
    ##Pasar este data genera error, cambiar que id va en cada consulta que citas abajo    
    data = {
        "id" : session['journalist_id']
    }
    
    journalist = Journalist.get_journalist(data)
    news = Newsletter.news_by_id(data)
    last = Newsletter.last_published()
    all_categories = Category.load_categories()
    all_news= Newsletter.news_by_author(data)
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")  
    return render_template("index.html", sistema=nombre_sistema, journalist = journalist, news = news, last = last, all_categories = all_categories, all_news = all_news)

@app.route("/about")
def about():
    
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")    
    return render_template("about.html", sistema=nombre_sistema)

@app.route("/contact")
def contact():
    
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")    
    return render_template("contact.html", sistema=nombre_sistema)

##CIERRE DE SESIÓN DE CUALQUIER TIPO DE USER
@app.route('/logout') 
def logout(): 
    session.clear()
    return redirect('/')

##Ruta de opcion de entrar a perfil en menu desplegable, nos hacia falta ese "acceso directo"
@app.route('/profile')
def redirect_profile():
    if 'journalist_id' in session:
        return redirect("/journalist/dashboard")
    elif 'reader_id' in session: 
        return redirect("/reader/dashboard")
    else:
        return redirect("/")