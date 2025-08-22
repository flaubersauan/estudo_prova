from flask_login import UserMixin
from flask import session

class User(UserMixin):
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.id = nome  # o id do usuário é o próprio nome

    @staticmethod
    def get(user_id):
        # Recupera o usuário da sessão se existir
        
        usuarios = session.get('usuarios', {})
        if user_id in usuarios:
            return User(nome=user_id, senha=usuarios[user_id])
        return None

