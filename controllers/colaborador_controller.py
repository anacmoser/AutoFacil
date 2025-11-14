from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, make_response
from models.Colaboradores import Colaborador, Lista_Colaboradores, adicionarColab, updateColab, deleteColab
from controllers.validacoes import validarEmail, validarSenha

colaborador_bp = Blueprint('colaborador_bp', __name__)
id = 5

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

@colaborador_bp.route('/cadastroColab', methods=['POST'])
def cadastrar():
    global id
    nome = request.form.get('nome', '')
    cargo = request.form.get('cargo', '')
    email = request.form.get('email', '')
    senha = request.form.get('senha', '')
    verificador = request.form.get('verificar', '')
    cpf = request.form.get('cpf', '')

    campos = [nome, cargo, email, senha, verificador, cpf]
    for campo in campos:
        if not campo:
            return render_template('colaboradores/colaborador.html', 
                                   errosCadastro = 'Todos os campos são obrigatórios',
                                    erroUpdate = '',
                                    errosDelete = '')
    
    try:
        novoColab = Colaborador(str(id), nome, cargo, email, senha, verificador, cpf)
        id += 1
        adicao = adicionarColab(novoColab)
        if adicao == True:
            return render_template('colaboradores/colaborador.html',
                                   errosCadastro = '', 
                                    errosUpdate = '',
                                    errosDelete = '')
        else:
            return render_template('colaboradores/colaborador.html', 
                                   errosCadastro = adicao,
                                    erroUpdate = '',
                                    errosDelete = '')
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
        
        return render_template('colaboradores/colaborador.html', 
                               errosCadastro = erros,
                                errosUpdate = '',
                                errosDelete = '')

@colaborador_bp.route('/updateColab', methods=['POST'])
def updateColab():
    cpf = request.form.get('cpf', '')
    campo = request.form.get('campo', '') #nome, email, cargo ou senha
    novoValor = request.form.get('novoValor', '')

    if not cpf or not campo or not novoValor:
        return render_template('colaboradores/colaborador.html', 
                               errosCadastro = '',
                               errosUpdate = 'Todos os campos devem ser preenchidos',
                               errosDelete = '')
    
    atualizacao = updateColab(cpf, campo, novoValor)
    if atualizacao != True:
        return render_template('volaboradores/colaborador.html', 
                               errosCadastro = '', 
                               errosUpdate = atualizacao,
                               errosDelete = '')
    return render_template('colaboradores/colaborador.html',
                            errosCadastro = '', 
                            errosUpdate = '',
                            errosDelete = '')

@colaborador_bp.route('/excluirColab', methods = ['POST'])
def excluirColab():
    cpf = request.form.get('cpf', '')
    exclusao = deleteColab(cpf)
    if exclusao == True:
        return render_template('colaboradores/colaborador.html',
                               errosCadastro = '', 
                               errosUpdate = '',
                               errosDelete = '')
    return render_template('colaboradores/colaborador.html',
                               errosCadastro = '', 
                               errosUpdate = '',
                               errosDelete = exclusao)

@colaborador_bp.route('/buscarColab', methods=['POST'])
def buscarColab():
    cpf = request.form.get('cpf', '')
    if not cpf: return render_template('colaboradores/colaborador.html', erro = 'Digite o CPF do colaborador')
    colab = buscarColab(cpf)
    if colab == False:
        return render_template('colaboradores/colaborador.html', erro = 'Colaborador não encontrado')
    if colab == 'CPF inválido':
        return render_template('colaboradores/colaborador.html', erro = 'CPF inválido')
    return render_template('colaboradores/colaborador.html', colaborador = colab)