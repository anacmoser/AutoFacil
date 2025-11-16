from flask_sqlalchemy import SQLAlchemy
from models import db

class Locais(db.Model):
    __tablename__ = 'Local_RetiradaDevolucao'

    Id_Local = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Endereco = db.Column(db.String(100), nullable = False)
    Nome = db.Column(db.String(50), nullable = False)
    Porcentagem = db.Column(db.DECIMAL(10,3), nullable = False)
