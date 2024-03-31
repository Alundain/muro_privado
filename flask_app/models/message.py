from flask_app.config.mysqlconnection import connectToMySQL

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
    #atributo extra necesitamos el nombre del usuario que envio el mensaje
        self.sender_name = data['sender_name']
    
    @classmethod
    def save(cls,form):
        query="INSERT INTO messages (content, sender_id, receiver_id) VALUES(%(content)s, %(sender_id)s, %(receiver_id)s)"
        results = connectToMySQL('esquema_muroprivado').query_db(query, form)
        return results
    
    @classmethod
    def get_my_messages(cls, dicc):
        query = "SELECT messages.*, users.first_name as sender_name FROM messages JOIN users ON sender_id = users.id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('esquema_muroprivado').query_db(query, dicc) #lista de diccionarios se transforma en una lista de instancias
        messages = []
        for m in results:
            messages.append(cls(m))
        return messages
    
    @classmethod
    def delete_message(cls, form):
        query = "DELETE FROM messages WHERE id = %(id)s "
        results = connectToMySQL('esquema_muroprivado').query_db(query, form)
        return results
    
    #metodo para obtener cuantos mensajes se han obtenido
    @classmethod
    def sent_messages(cls, form):
        query= "SELECT COUNT(*) as cantidad FROM messages WHERE sender_id = %(id)s"
        results = connectToMySQL('esquema_muroprivado').query_db(query, form)
        return results[0]['cantidad']