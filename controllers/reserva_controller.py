from flask import Flask, Blueprint, request, render_template, session, redirect, url_for
from datetime import datetime
from controllers.validacoes import validarCNH
from controllers.user_controller import getUser
from models.Veiculo import Veiculos
from models.Reservas import Reservas
from models.Locais import Locais
from models.UserPf import UserPfDB
from sqlalchemy import and_
from models import db

reserva_bp = Blueprint('reserva_bp', __name__)

@reserva_bp.route('/reserva/<int:veiculo_id>', methods=['POST'])
def reserva(veiculo_id):
    formato='%Y-%m-%d'
    data_ret = datetime.strptime(request.form.get('dataRetirada'), formato).date()
    data_dev = datetime.strptime(request.form.get('dataDev'), formato).date()
    dias = (data_dev - data_ret).days

    id_localDevolucao = request.form.get('localDevolucao')
    localDev = Locais.query.get(id_localDevolucao)
    id_localRetirada = request.form.get('localRetirada')
    localRet = Locais.query.get(id_localRetirada)

    for veiculo in Veiculos.query.all():
        if veiculo.id == veiculo_id:
            if veiculo.status == 'disponível':
                disponibilidade = verificar_disponibilidade(veiculo_id, data_ret, data_dev)
                if disponibilidade == True:
                    if dias >= 30 and dias < 90:
                        valorTotal = (veiculo.precoDiario * dias * (1 + localDev.Porcentagem) + 45) * 0.90
                    elif dias >= 90 and dias < 180:
                        valorTotal = (veiculo.precoDiario * dias * (1 + localDev.Porcentagem) + 45) * 0.70
                    elif dias >= 180:
                        valorTotal = (veiculo.precoDiario * dias * (1 + localDev.Porcentagem) + 45) * 0.55
                    else:
                        valorTotal = veiculo.precoDiario * dias * (1 + localDev.Porcentagem) + 45
                    try:
                        nova_reserva = Reservas(
                            Id_Cliente = session.get('usuario_logado'),  #Arrumar o login de userPf para passar seu login
                            Id_Veiculo = veiculo_id,
                            Data_Retirada = data_ret,
                            Data_Devolucao = data_dev,
                            Valor_Total = valorTotal,
                            Status = 'pendente',
                            local_retirada = localRet.Nome,
                            local_devolucao = localDev.Nome,
                            perfil = session.get('usuario_perfil')
                        )

                        db.session.add(nova_reserva)
                        db.session.commit()

                    except Exception as e:
                        db.session.rollback()
                        return redirect(url_for('reserva_bp.pgReserva', id_veiculo = veiculo.id))
                
                    reserva = getReserva(session.get('usuario_logado'), veiculo_id, data_ret, data_dev)
    
                    return redirect(url_for('reserva_bp.pgPagamento', id_reserva = reserva.Id_Reserva))
                elif disponibilidade == False:
                    return redirect(url_for('reserva_bp.pgReserva', id_veiculo = veiculo.id))
                else:
                    raise ValueError('Algo deu errado')

@reserva_bp.route('/confirmarReserva/<int:id_reserva>', methods=['POST'])  #Essa rota não está sendo chamada, provavelmente o js não está permitindo o acesso à rota
def confirmarReserva(id_reserva):
    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado'))
    reserva = Reservas.query.get(id_reserva)
    veiculo = Veiculos.query.get(reserva.Id_Veiculo)

    if session.get('usuario_perfil') == 'pf':
        if not user.CNH:
            cnh = request.form.get('cnh', '')
            if not validarCNH(cnh):          
                return render_template('pagamento.html', veiculo = veiculo, user = user, reserva = reserva, erro = 'CNH inválida')
            
            UserPfDB.query.filter_by(Id_Cliente=session.get('usuario_logado')).update({ #A cnh não está atualizando, pode ser conflito com o js ou o problema é o comando no bd
                "CNH": cnh
            })
            db.session.commit() 

    Reservas.query.filter_by(Id_Reserva=id_reserva).update({
        "Status": 'confirmada'  #O status também não está atualizando
    })
    db.session.commit() 
    return render_template('pagamento.html', veiculo = veiculo, user = user, reserva = reserva)
    
@reserva_bp.route('/pgPagamento/<int:id_reserva>')
def pgPagamento(id_reserva):
    reserva = Reservas.query.get(id_reserva)
    veiculo = Veiculos.query.get(reserva.Id_Veiculo)
    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado'))
    return render_template('pagamento.html', veiculo = veiculo, valorTotal = reserva.Valor_Total, user = user, reserva = reserva)

@reserva_bp.route('/pgReserva/<int:id_veiculo>')
def pgReserva(id_veiculo):
    veiculo = Veiculos.query.get(id_veiculo)
    locais = Locais.query.all()
    similares = Veiculos.query.filter_by(categoria=veiculo.categoria).all()
    
    return render_template('detalhe_veiculo.html', status='Veículo indisponível nessa data', veiculo=veiculo, veiculos_similares = similares, locais = locais)

def verificar_disponibilidade(veiculo_id, inicio, fim):
    conflito = (db.session.query(Reservas)
        .filter(
            Reservas.Id_Veiculo == veiculo_id,
            Reservas.Data_Retirada <= fim,
            Reservas.Data_Devolucao >= inicio
        )
        .first())

    if conflito:
        return False
    
    return True

def getReserva(id_cliente, id_carro, data_ret, data_dev):
    reserva = Reservas.query.filter(
        and_(
            Reservas.Id_Cliente == id_cliente,
            Reservas.Id_Veiculo == id_carro,
            Reservas.Data_Retirada == data_ret,
            Reservas.Data_Devolucao == data_dev
        )
    ).first()

    return reserva