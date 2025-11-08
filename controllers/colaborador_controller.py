from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, make_response
from models.Colaboradores import Colaborador, Lista_Colaboradores
from controllers.validacoes import validarEmail, validarSenha

colaborador_bp = Blueprint('colaborador_bp', __name__)

@colaborador_bp.route('/loginColab', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('password', '')
        remember = request.form.get('lembrar', '')

        if not email:
            return render_template('colaboradores/login_colaborador.html', erro = 'Email obrigatório')
        if not senha:
            return render_template('colaboradores/login_colaborador.html', erro = 'Senha obrigatória')
        
        if not validarEmail(email):
            return render_template('colaboradores/login_colaborador.html', erro = 'Email inválido')
        if not validarSenha(senha):
            return render_template('colaboradores/login_colaborador.html', erro = 'Senha inválida')
        
        #BD verifica se o user existe
            #Se existir, verifica as senhas
                #Se as senhas forem iguais:
                    #session['usuario_logado'] = email
                    #session['usuario_perfil'] = 'colaborador'
                    #session['colab_cargo'] = busca no bd o cargo associado àquele email
                    #return render_template('colaboradores/colaborador.html', cargo = colab.cargo)
            
        for colab in Lista_Colaboradores:
            if colab.email == email and colab.senha == senha:
                session['usuario_logado'] = colab.email
                session['usuario_perfil'] = colab.perfil
                session['colab_cargo'] = colab.cargo
                if remember:
                    response = make_response(redirect(url_for('pgColaborador')))
                    response.set_cookie('user', str(colab.email), max_age=60*60*72)
                    response.set_cookie('perfil', 'colab', max_age=60*60*72)
                    response.set_cookie('cargo', str(colab.cargo), max_age=60*60*72)
                    return response
                return redirect(url_for('pgColaborador'))
            if colab.email == email and colab.senha != senha:
                return render_template('colaboradores/login_colaborador.html', erro = 'Senha incorreta')
        return render_template('colaboradores/login_colaborador.html', erro = 'Colaborador não encontrado')


#Mexer nos cookies remenber me
#API CEP