from sqlalchemy import Column, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from .base import Base, db

class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(200))
    perfil = Column(String(20), default='usuario')  # admin, usuario, etc.
    foto_perfil = Column(String(200), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def senha(self):
        raise AttributeError('senha não é um atributo legível')
        
    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def is_admin(self):
        return self.perfil == 'admin'
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
