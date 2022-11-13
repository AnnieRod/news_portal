from flask_base.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_base.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Journalist(User):
    data_name = "portal_noticias"
    def __init__(self, data):
        super().__init__(data)
        self.id = data['id']
        self.credential = data['credential']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] 
        self.news=['']

    ##Crea periodista
    @classmethod
    def save_journalist(cls, data):
        query = "INSERT INTO journalists(credential, created_at, updated_at, user_id) VALUES (%(credential)s, NOW(), NOW(), %(user_id)s);"
        journalist = connectToMySQL(cls.data_name).query_db(query, data)
        return journalist

    ##Recupera periodista por su ID para mostrar nombre en perfil de creador, no borrar porfa
    @classmethod
    def get_creator_profile(cls, data):
        query = "SELECT * FROM journalists JOIN users ON users.id = journalists.user_id WHERE journalists.id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])

    #Recupera periodista por su ID, se usa en index  ahora con el cambio  
    @classmethod
    def get_journalist(cls, data):
        query = "SELECT * FROM journalists JOIN users ON users.id = journalists.user_id JOIN news ON news.journalist_id = journalists.id JOIN images ON images.new_id = news.id;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        print("VER JOURNALIST--->", result)
        all_journalists_news = []
        for journalist in result:
            data = {
                'id' : journalist['news.id'],
                'title' : journalist['title'],
                'resume' : journalist['resume'],
                'content' : journalist['content'],
                'category_id' : journalist['category_id'],
                'journalist_id' : journalist['journalist_id'],
                'image' : journalist.get('name', ""),
                'created_at' : journalist['news.created_at'],
                'updated_at' : journalist['news.updated_at']
            }
            all_journalists_news.append(data)
            print("QUIERO VER JOURNALIST XXX--->", journalist)
        new_journalist= cls(result[0])
        new_journalist.news = all_journalists_news
        return new_journalist

    #Obtiene TODOS los periodistas
    @classmethod
    def get_all_journalists(cls): 
        query = "SELECT journalists.*,users.first_name, users.last_name, users.email, users.password FROM journalists JOIN users ON users.id = journalists.user_id;"
        results = connectToMySQL(cls.data_name).query_db(query)
        all_journalists = []
        for journalist in results:
            all_journalists.append(cls(journalist))
        return all_journalists

    ##revisa si correo coincide para iniciar sesión y luego valida datos
    @classmethod
    def get_login(cls, data):
        query = "SELECT * FROM journalists JOIN users ON users.id = journalists.user_id WHERE email =%(email)s;"
        result = connectToMySQL(cls.data_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_journalist(journalist): 
        is_valid = True
        if len(journalist["first_name"]) < 2:  
            flash("Tu nombre debe tener al menos dos caracteres.", "register")
            is_valid = False
        if len(journalist["last_name"]) < 2:  
            flash("Tu apellido debe tener al menos dos caracteres.", "register")
            is_valid = False
        ##Valida que el correo no este registrado ya
        query = "SELECT * FROM journalists JOIN users ON users.id = journalists.user_id WHERE email =%(email)s;"
        coincidence = connectToMySQL("portal_noticias").query_db(query, journalist)
        if len(coincidence) >= 1:
            flash ("Email no valido, ya está registrado", "register")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(journalist['email']):
            flash("Email no valido", "register")
            is_valid = False
        if len(journalist["password"]) < 8: 
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        if journalist["password"] != journalist['confirm_password']:
            flash("Las contraseñas no coinciden", "register")
            is_valid = False
        if len(journalist["credential"]) < 4: 
            flash("Tu registro profesional debe ser más largo", "register")
            is_valid = False
        return is_valid