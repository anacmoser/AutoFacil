from flask import Flask, Blueprint, session, render_template
from models.UserPj import USERSpj

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/portalCliente', methods=['GET'])
def portalCliente():
    user_id = session.get('usuario_logado')
    user_perfil = session.get('usuario_perfil')
    if user_perfil == 'pj':
        for user in USERSpj:
            if user.id == user_id:
                return render_template('portalCliente.html', user = user)
    #if user_perfil == 'pf':
        #Lógica com o banco de dados
    return render_template('index.html')

@user_bp.route('/login', methods=['GET'])
def pgLogin():
    return render_template('login.html')

@user_bp.route('/cadastro', methods=['GET'])
def pgCadastro():
    return render_template('cadastro.html')