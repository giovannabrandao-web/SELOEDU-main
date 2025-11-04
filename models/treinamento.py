from extensions import db
from datetime import datetime

class Treinamento(db.Model):
    __tablename__ = 'treinamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    carga_horaria = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='ativo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('treinamentos', lazy=True))