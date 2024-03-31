from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re # import expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls, data):
        #encriptar mi contraseña
        query="INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_muroprivado').query_db(query, data)
        return result 
    
    @staticmethod
    def validate_user(data):
        # recibo mi data con todos los names y valores que el usuario ingresó
        is_valid = True
        #validar que el nombre tenga al menos dos caracteres
        if len(data["first_name"]) < 2:
            flash("Nombre debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        if len(data["last_name"]) < 2:
            flash("Apellido debe tener al menos 2 caracteres","register")
            is_valid = False

        # que el correo tenga el patron correcto
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email no válido", "register")
            is_valid = False
            
        # validar que el correo sea único
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_muroprivado').query_db(query,data)
        if len(results) >= 1:
            flash("Email registrado previamente", "register")
            is_valid = False
        
        # validar que la contraseña tengo al menos 6 caracteres
        if len(data["password"]) < 6:
            flash("El password debe tener al menos 6 caracteres", "register")
            is_valid = False

        if data["password"] != data["confirm"]:
            flash("Las contraseñas no coinciden! ", "register")
            is_valid = False

        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_muroprivado').query_db(query,data)
        if len(results) == 1:
            user = cls(results[0])
            return user
        else:
            return False
        
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_muroprivado').query_db(query, data)
        user = cls(result[0])
        return user
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ORDER BY first_name ASC "
        results = connectToMySQL('esquema_muroprivado').query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users
    