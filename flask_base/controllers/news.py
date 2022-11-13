import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask import request, redirect, render_template,session, flash, send_from_directory, url_for
from flask_base import app
from datetime import datetime
from flask_base.models.images import Image
from flask_base.models.newsletter import Category, Newsletter
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## Renderiza pagina de crear noticia
@app.route("/news/create")
def form_news():
    return render_template("createnews.html", all_categories = Category.load_categories())

@app.route('/uploads/<name>')
def download_file(name):
    print("QUIERO VER IMAGE---->", name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/news/upload", methods = ['GET','POST'])
def create_news():
    if request.method == 'POST':
        if 'journalist_id' not in session:
            return redirect("/journalist/register")
        if not Newsletter.validate_news(request.form):
            return redirect("/news/create")
        print('in post of file')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename =f"{int(datetime.utcnow().timestamp())}{secure_filename(file.filename)}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    data = {
        'title': request.form['title'],
        'resume': request.form['resume'],
        'content': request.form['content'],
        'category_id' : request.form['category_id'],
        'journalist_id' : session['journalist_id'],
    }

    noticia=Newsletter.publish_news(data)
    new_image={
        'name': filename,
        'new_id':noticia,
    }
    print("VER IMAGE 44444--->",new_image)
    image = Image.save(new_image)
    if data == False:
        flash('algo errado paso con la creacion de la noticia', 'error')
        return redirect ('/contact')
    flash('Exito al crear nueva noticia', 'success')
    return redirect("/journalist/dashboard")

## Render plantilla noticia individual - funciona, pasa plantilla y la info a mostrar
@app.route("/news/<int:id>")
def render_news(id):
    if 'journalist_id' not in session:
        return redirect("/")
    flash("registrese", "error")
    data = {
        "id" : id
    }
    news = Newsletter.individual_newsletter(data)
    return render_template("newstemplate.html", news = news)

@app.route("/news/category/<int:id>")
def category_page(id):
    data = {
        "id" : id
    }
    categories = Category.get_all(data)

    return render_template("categorypage.html", all_categories = Category.load_categories(), all_news = Newsletter.news_by_category(data), categories = categories)