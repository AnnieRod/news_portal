import os

from flask_base.config.mysqlconnection import connectToMySQL
from flask_base.models.modelo_base import ModeloBase
from flask import flash

class Image(ModeloBase):
    
    modelo = 'images'
    campos = ['name','new_id']

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.recipe_id = data['new_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']