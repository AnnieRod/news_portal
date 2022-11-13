from flask_base.config.mysqlconnection import connectToMySQL
from flask import flash

## Clase de usuario para poder heredar en las otras tablas
class User:
    data_name = "portal_noticias"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.user = data['user']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password, user, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(user)s, NOW(), NOW());"
        user = connectToMySQL(cls.data_name).query_db(query, data)
        return user