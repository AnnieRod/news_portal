import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask_base.models.modelo_base import ModeloBase
from flask import flash



class Category:
    data_name = "portal_noticias"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def load_categories(cls):  
        query = "SELECT * FROM categories;"
        results = connectToMySQL(cls.data_name).query_db(query)
        all_categories = []
        for category in results:
            category['images.name'] = ''       ## Por qué a esto aca? 
            all_categories.append(cls(category))
        return all_categories
    
    @classmethod
    def get_all(cls, data):  
        query = "SELECT * FROM categories WHERE id = %(id)s;"
        results = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(results[0])

class Newsletter: 
    data_name = "portal_noticias"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.resume = data['resume']
        self.content = data['content']
        self.category_id = data['category_id']
        self.journalist_id = data['journalist_id']
        # self.image = data['name']
        self.image = data.get('name', "")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def publish_news(cls,data):
        query = "INSERT INTO news (title, resume, content, category_id, journalist_id, created_at, updated_at) VALUES (%(title)s, %(resume)s, %(content)s, %(category_id)s, %(journalist_id)s, NOW(), NOW());"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        print("AQUI QUIERO VER 22222-->",result)
        return result 

    ##CONTADOR de noticias publicadas POR UN PERIODISTA by ID
    @classmethod
    def news_by_id(cls, data):
        query = "SELECT COUNT(news.id) AS total FROM news WHERE journalist_id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query,data)
        if len(result) < 1:
            return False
        return result

    ## TRAE NOTICIA MAS RECIENTE PUBLICADA POR PERIODISTA BY ID, usada en perfil de periodista, no borrar por fa
    @classmethod
    def get_last_published(cls, data):
        query = "SELECT * FROM news WHERE journalist_id = %(id)s ORDER BY created_at DESC LIMIT 1;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])

    ##TRAE NOTICIA MAS RECIENTE PUBLICADA POR PERIODISTA BY ID USADA EN INDEX POR EL CAMBIO AHORA<
    @classmethod
    def last_published(cls):
        query = "SELECT * FROM images LEFT JOIN news ON news.id = images.new_id ORDER BY news.created_at DESC LIMIT 5;"
        result = connectToMySQL(cls.data_name).query_db(query)
        print("AQUI------> last", result)
        news = []
        for new in result:
            news.append(cls(new))
        return news
    
    ## TRAE TODAS LAS NOTICIAS PARA TODOS LOS USUARIOS EN FORMA DESCENDE
    @classmethod
    def all_published(cls):
        query = "SELECT * FROM images LEFT JOIN news ON news.id = images.new_id ORDER BY news.created_at DESC;"
        result = connectToMySQL(cls.data_name).query_db(query)
        print("AQUI------> last", result)
        news = []
        for new in result:
            news.append(cls(new))
        return news

    ##Trae detalles de noticias escritas por un periodista 
    @classmethod
    def news_by_author(cls, data):
        query = "SELECT * FROM images LEFT JOIN news ON news.id = images.new_id"
        results = connectToMySQL(cls.data_name).query_db(query, data)
        news = []
        for new in results:
            news.append(cls(new))
        return news

##Muestra datos de noticia para plantilla individual
    @classmethod
    def individual_newsletter(cls, data):
        query = "SELECT * FROM images LEFT JOIN news ON news.id = images.new_id WHERE images.id = %(id)s"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        print(result)
        return cls(result[0])
    
    @classmethod 
    def news_by_category(cls, data):
        query = """SELECT * FROM images LEFT JOIN news ON news.id = images.new_id
                LEFT JOIN categories ON categories.id = news.category_id
                WHERE categories.id = %(id)s
                """
        result = connectToMySQL(cls.data_name).query_db(query, data)
        news = []
        for thing in result:
            print(thing)
            news.append(cls(thing))
        return news

    @staticmethod
    def validate_news(newsletter):
        is_valid = True
        if len(newsletter["title"]) < 3:
            flash("Debes poner al menos una palabra", "register")
            is_valid = False
        if len(newsletter["resume"]) < 10:
            flash("Debes poner al menos una frase que resuma la noticia", "register")
            is_valid = False
        if len(newsletter["content"]) < 10:
            flash("La noticia debe tener un enunciado informativo", "register")
            is_valid = False
        if len(newsletter["category_id"]) == "":
            flash("Debes seleccionar una categoría", "register")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_width_picture(cls):
        query = "SELECT * FROM images LEFT JOIN news ON news.id = images.new_id;"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        print("AQUI QUIERO VER 22222-->",results)
        all_data = []
        for data in results:
            data['name'] = ''
            all_data.append(cls(data))
            print("VER DATA--->", data)
            print("VER ALL_DATA--->", all_data)
        return all_data

