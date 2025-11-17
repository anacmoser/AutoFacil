from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from models import db

class Reservas(db.Model):
    __tablename__ = 'Reservas'

    Id_Reserva = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Cliente = db.Column(db.Integer, nullable=False)
    Id_Veiculo = db.Column(db.Integer, nullable=False)
    Data_Retirada = db.Column(db.Date, nullable=False)
    Data_Devolucao = db.Column(db.Date, nullable=False)
    Valor_Total = db.Column(db.DECIMAL(10, 2), nullable=False)
    Status = db.Column(db.Enum('pendente', 'confirmada', 'cancelada', name='status_reserva'), nullable=False)
    local_retirada = db.Column(db.String(255), nullable=False)
    local_devolucao = db.Column(db.String(255), nullable = False)
    perfil = db.Column(db.String(2), nullable = False)

