from flask import Flask, Blueprint, session, render_template, make_response, redirect, url_for, request, abort
from models.UserPj import USERSpj
from models.UserPf import UserPfDB
from re import sub
from sqlalchemy import or_

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/portaldoCliente')
def portaldoCliente():
    user = session.get('usuario_logado')
    perfil = session.get('usuario_perfil')

    usuario_limpo = sub(r'[^0-9]', '', user)

    if perfil == 'pj':
        for userpj in USERSpj:
            if userpj.id == user:
                render_template('portalCliente.html', user = user)
    elif perfil == 'pf':
        userpf = UserPfDB.query.filter(or_(UserPfDB.Email == user,UserPfDB.CPF == usuario_limpo)
        ).first()
        if userpf:
            return render_template('portalCliente.html', user = user)
    else:
        return render_template('index.html')

@user_bp.route('/minhasReservas', methods=['GET'])
def pgMinhasReservas():
    if session.get('usuario_logado') == None:
        abort(401)
    return render_template('minhas_reservas.html')

@user_bp.route('/login', methods=['GET'])
def pgLogin():
    return render_template('login.html')

@user_bp.route('/cadastro', methods=['GET'])
def pgCadastro():
    return render_template('cadastro.html')

@user_bp.route('/logout', methods=['GET']) 
def logout():
    session.clear()
    resposta = make_response(redirect(url_for('index')))

    resposta.set_cookie('user', '', expires=0)
    resposta.set_cookie('perfil', '', expires=0)
    if request.cookies.get('cargo'):
        resposta.set_cookie('cargo', '', expires=0)
    return resposta