from controllers.validacoes import validacaoGeralColab
from controllers.validacoes import validarNome, validarEmail, validarSenha, validarCpf
from models import db
class ColaboradorDB(db.Model):
    __tablename__ = 'Colaborador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(20), default='colab')
    cargo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    
class Colaborador:
    def __init__(self, id, nome, perfil, cargo, email, senha, verificador, cpf):
        if validacaoGeralColab(nome, perfil, senha, verificador, cpf, email):
            self._id = id
            self._nome = nome
            self._perfil = 'colab'
            self._cargo = cargo
            self._email = email
            self._senha = senha
            self._cpf = cpf

    @property
    def id(self):
        return self._id
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def perfil(self):
        return self._perfil
    
    @property
    def cargo(self):
        return self._cargo
    
    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha    
    
    @property
    def cpf(self): 
        return self._cpf    

    def updateAttr(self, campo, valor):
        setattr(self, campo, valor)