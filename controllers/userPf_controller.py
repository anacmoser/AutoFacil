#PESSOA FÍSICA

#Verificar se os campos estão vazios

#Função de cadastro
#função de login

from flask import Blueprint, render_template, request, session, make_response, redirect, url_for
from controllers.validacoes import validarEmail, validarCpf
from models.UserPf import USERSpf
import re
user_pf_bp = Blueprint('user_pf_bp', __name__)

id_counter_Pf = 2  

@user_pf_bp.route('/cadastrarPf', methods=['POST'])
def cadastro():
    global id_counter_Pf  
    
    # Obter dados do formulário
    nome = request.form.get('nome', '').strip()
    nascimento = request.form.get('nascimento', '')
    cpf = request.form.get('cpf', '')
    cpf = re.sub(r'[^0-9]', '', cpf) 
    celular = request.form.get('celular', '')
    celular = re.sub(r'[^0-9]', '', celular)
    email = request.form.get('email', '').strip()
    cep = request.form.get('cep', '')
    logradouro = request.form.get('logradouro', '').strip()
    numero = request.form.get('numero', '').strip()
    complemento = request.form.get('complemento', '').strip()
    bairro = request.form.get('bairro', '').strip()
    estado = request.form.get('estado', '').strip()
    cidade = request.form.get('cidade', '').strip()
    senha = request.form.get('senha', '')
    confirmar_senha = request.form.get('confirmar', '')
    termos = request.form.get('termos')
    
    # Verificar se todos os campos obrigatórios foram preenchidos
    campos_obrigatorios = [nome, nascimento, cpf, celular, email, cep, logradouro, bairro, estado, cidade, senha, confirmar_senha]
    for campo in campos_obrigatorios:
        if not campo:
            return render_template('cadastro.html', erros='Todos os campos obrigatórios devem ser preenchidos')

    if not termos:
        return render_template('cadastro.html', erros='Você deve aceitar os Termos de Uso.')
    try:
        novoUser = UserPf(id_counter_Pf, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, confirmar_senha, logradouro, numero, complemento)
        adicao = addUser(novoUser) #Verificar por nome também (já existe por email e cpf)
        if adicao == True: #Se não for true será a lista de erros
            id_counter_Pf += 1
            return redirect(url_for('login'))
        else:
            return render_template('cadastro.html', erros=adicao)
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
        
        return render_template('cadastro.html', erros=erros)

@user_pf_bp.route('/logarPf', methods=['GET', 'POST']) #Modularizar as verificações
def login():
    if request.method == 'POST':
        user = request.form.get('user', '')
        senha = request.form.get('password', '')
        remember = request.form.get('lembrar')

        if not user:
            return render_template('login.html', erro = 'Email obrigatório')
        if not senha:
            return render_template('login.html', erro = 'Senha obrigatória')
        
        if '@' in user:
            if not validarEmail(user):
                return render_template('login.html', erro = 'E-mail inválido')
            for usuario in USERSpf:
                if usuario.email == user :
                    if usuario.senha == senha:
                        session['usuario_logado'] = usuario.nome
                        if remember:
                            response = make_response(redirect(url_for('index')))
                            response.set_cookie('user', usuario.id, max_age=60*60*72)
                            return response
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')
        else: 
            cpf = re.sub(r'[^0-9]', '', user)
            if not validarCpf(cpf):
                return render_template('login.html', erro = 'Digite e-mail ou CPF inválidos')
            for usuario in USERSpf:
                if usuario.cpf == cpf:
                    if usuario.senha == senha:
                        session['usuario_logado'] = usuario.nome
                        if remember:
                            response = make_response(redirect(url_for('index')))
                            response.set_cookie('user', usuario.id, max_age=60*60*72)
                            return response
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')        
    
    return render_template('login.html')