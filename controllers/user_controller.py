from flask import Flask, Blueprint, session, render_template, make_response, redirect, url_for, request, abort
from models.UserPj import UserPjDB
from models.UserPf import UserPfDB
from models.Reservas import Reservas
from models.Veiculo import Veiculos
from controllers.validacoes import validarSenha
from re import sub
from models import db
from sqlalchemy import or_

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/portaldoCliente')
def portaldoCliente():

    if session.get('usuario_logado') == None:
        abort(401)
    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado')) 

    reservas = Reservas.query.filter_by(Id_Cliente = user.Id_Cliente).all()
    veiculos = Veiculos.query.all()

    veiculos_dict = {veiculo.id: veiculo for veiculo in veiculos}
    if user:
        return render_template('portalCliente.html', user = user, reservas = reservas, veiculos = veiculos_dict)
  
    else:
        return render_template('index.html')
    

@user_bp.route('/minhasReservas', methods=['GET'])
def pgMinhasReservas():
    if session.get('usuario_logado') == None:
        abort(401)
    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado'))
    reservas = Reservas.query.filter_by(Id_Cliente = user.Id_Cliente).all()
    return render_template('portalCliente.html', reservas)

@user_bp.route('/login', methods=['GET'])
def pgLogin():
    return render_template('login.html')

@user_bp.route('/cadastro', methods=['GET'])
def pgCadastro():
    return render_template('cadastro.html')

@user_bp.route('/atualizarSenha', methods=['POST'])
def atualizarSenha():
    senha_atual = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')
    confirmar = request.form.get('confirmar_senha')

    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado'))
    erros = []
    if user.Senha != senha_atual:
        erros.append('Senha atual incorreta')
    if not validarSenha(nova_senha):
        erros.append('A nova senha deve conter letras maiúsculas e minúsculas e pelo menos 8 caracteres')
    if nova_senha != confirmar:
        erros.append('As senhas não coincidem')

    if erros:
        return render_template('portalCliente', erros = erros)
    
    if session.get('usuario_perfil') == 'pf':
        UserPfDB.query.filter_by(Id_Cliente=session.get('usuario_logado')).update({  #A senha não está atualizando, pode ser conflito com o js ou o problema é o comando no bd
            "Senha": nova_senha
        })
        db.session.commit() 

        return render_template('portalCliente.html')

@user_bp.route('/excluirConta', methods=['POST'])
def excluir():
    user = getUser(session.get('usuario_perfil'), session.get('usuario_logado')) #Mesmo problema das outras rotas, pd ser js ou comando sql
    db.session.delete(user) 
    db.session.commit()
    return redirect(url_for('logout'))

@user_bp.route('/logout', methods=['GET']) 
def logout():
    session.clear()
    resposta = make_response(redirect(url_for('index')))

    resposta.set_cookie('user', '', expires=0)
    resposta.set_cookie('perfil', '', expires=0)
    if request.cookies.get('cargo'):
        resposta.set_cookie('cargo', '', expires=0)
    return resposta

def getUser(perfil, id):
    if perfil == 'pf':
        user = UserPfDB.query.get(id)
        return user
    if perfil == 'pj':
        user = UserPjDB.query.get(id)
        return user