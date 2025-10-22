from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(11), nullable=True)
    instituicao = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    user = db.relationship(
        'User',
        back_populates='perfil', # Nome do atributo de relacionamento na classe User
        uselist=False
    )