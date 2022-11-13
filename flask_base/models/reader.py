from flask_base.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_base.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Reader(User):
    data_name = "portal_noticias"
    def __init__(self, data):
        super().__init__(data)
        self.id = data['id']
        self.subscription = data['subscription']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] 


    ##Crea instancia de lector
    @classmethod
    def save_reader(cls, data):
        query = "INSERT INTO readers (subscription, created_at, updated_at, user_id) VALUES (%(subscription)s, NOW(), NOW(), %(user_id)s);"
        reader = connectToMySQL(cls.data_name).query_db(query, data)
        return reader

    ##Busca lector por su ID
    @classmethod
    def get_reader_profile(cls, data):
        query = "SELECT * FROM readers JOIN users ON users.id = readers.user_id WHERE readers.id = %(id)s;"
        result = connectToMySQL(cls.data_name).query_db(query, data)
        return cls(result[0])

    ## Trae a todos los lectores 
    @classmethod
    def get_all(cls): 
        query = "SELECT * FROM readers JOIN users ON users.id = readers.user_id;"
        results = connectToMySQL(cls.data_name).query_db(query)
        readers = []
        for reader in results:
            readers.append(cls(reader))
        return readers


    ##revisa si correo coincide para iniciar sesión y luego valida datos
    @classmethod
    def get_login(cls, data):
        query = "SELECT * FROM readers JOIN users ON users.id = readers.user_id WHERE email =%(email)s;"
        result = connectToMySQL(cls.data_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_reader(reader):
        is_valid = True
        if len(reader["first_name"]) < 2:  
            flash("Tu nombre debe tener al menos dos caracteres.", "register")
            is_valid = False
        if len(reader["last_name"]) < 2: 
            flash("Tu apellido debe tener al menos dos caracteres.", "register")
            is_valid = False
        ##Valida que el correo no este registrado ya
        query = "SELECT * FROM readers JOIN users ON users.id = readers.user_id WHERE email =%(email)s;"
        coincidence = connectToMySQL("portal_noticias").query_db(query, reader)
        if len(coincidence) >= 1:
            flash ("Email no valido, ya está registrado", "register")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(reader['email']):
            flash("Email no valido", "register")
            is_valid = False
        if len(reader["password"]) < 8: 
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        if reader["password"] != reader['confirm_password']:
            flash("Contraseñas no coinciden", "register")
            is_valid = False
        if len(reader["subscription"]) < 8: 
            flash("Tu codigo de suscripción debe tener minimo 8 caracteres", "register")
            is_valid = False  
        return is_valid