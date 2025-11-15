from models import db

class Veiculos(db.Model):
    __tablename__ = "Veiculos"
     
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    transmissao = db.Column(db.String(50))
    precoDiario = db.Column(db.Float)
    nome = db.Column(db.String(100))
    imagem = db.Column(db.String(300))
    nMalas = db.Column(db.Integer)
    nPassageiros = db.Column(db.Integer)
    nPortas = db.Column(db.Integer)
    combustivel = db.Column(db.String(50))
    status = db.Column(db.String(20))
    
def getVeiById(id):
    return Veiculos.query.get(id)

