from flask_sqlalchemy import SQLAlchemy
from models import db

class UserPfDB(db.Model):
    __tablename__ = 'UserPf'

    Id_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(100), nullable=False)
    CNH = db.Column(db.String(20))
    CPF = db.Column(db.String(11), unique=True, nullable=False)
    Nome = db.Column(db.String(100), nullable=False)
    Telefone = db.Column(db.String(15))
    Data_Nascimento = db.Column(db.Date)
    CEP = db.Column(db.String(20))
    Logradouro = db.Column(db.String(100))
    Numero = db.Column(db.String(10))
    Complemento = db.Column(db.String(50))
    Bairro = db.Column(db.String(50))
    Estado = db.Column(db.String(50))
    Cidade = db.Column(db.String(50))
    Senha = db.Column(db.String(255), nullable=False)
