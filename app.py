"""
TAREFAS:
    * Arquitetura / organização MVC                      COMPLETO: view, models
    * Páginas de erro (404, 403, 401)
        *Definir a quais páginas o user tem acesso sem estar logado
    * Arquivo para APIs (Para diminuir a quantidade de html)
    * Api de CEP para pré-preenchimento do formulário
    * Lógica da página específica igual ao do exercício do agostinho (PRODUTOS)
    * Paginação
    * Blueprint
    * Arquivo de validações e verificações em comum para UserPj e UserPf

    * Para guardar os dados no BD, deve formatar num padrão
"""

from flask import Flask, render_template, request, redirect, url_for, session, make_response, abort
import math
from models.Veiculo import VEICULOS
from models.UserPj import USERSpj
from controllers.veiculo_controller import veiculo_bp
from controllers.userPf_controller import user_pf_bp
from controllers.userPj_controller import user_pj_bp
from controllers.colaborador_controller import colaborador_bp
from flask import Flask, render_template, request
from models import db
from dotenv import load_dotenv
import os
from models.UserPf import UserPfDB

load_dotenv()  # carrega o arquivo .env

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

    
app.secret_key = 'chave_secreta_autofacil'
app.register_blueprint(veiculo_bp)
app.register_blueprint(user_pf_bp)
app.register_blueprint(user_pj_bp)
app.register_blueprint(colaborador_bp)

# Rotas
@app.route('/')
def index():
    if 'usuario_logado' not in session:
        user = request.cookies.get('user', '')
        perfil = request.cookies.get('perfil')
        if user:
            session['usuario_logado'] = user
            session['usuario_perfil'] = perfil
            if perfil == 'colab':
                session['colab_cargo'] = request.cookies.get('cargo')
                return redirect(url_for('pgColaborador'))
    
    if 'usuario_logado' in session:
        if session.get('usuario_perfil') == 'colab':
            return redirect(url_for('pgColaborador'))

    return render_template('index.html')

@app.route('/login', methods=['GET'])
def pgLogin():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET'])
def pgCadastro():
    return render_template('cadastro.html')

@app.route('/loginColaborador', methods=['GET'])
def loginColaborador():
    return render_template('colaboradores/login_colaborador.html')

@app.route('/reserva', methods=['GET'])
def pgReserva():
    return render_template('reserva.html')

@app.route('/aluguelMensal', methods=['GET'])
def pgAluguelMensal():
    return render_template('aluguelmensal.html')

@app.route('/empresas', methods=['GET'])
def pgEmpresas():
    return render_template('empresas.html')

@app.route('/minhasReservas', methods=['GET'])
def pgMinhasReservas():
    if session.get('usuario_logado') == None:
        abort(401)
    return render_template('minhas_reservas.html')

@app.route('/portalCliente', methods=['GET'])
def portalCliente():
    user_id = session.get('user')
    user_perfil = session.get('usuario_perfil')
    if user_perfil == 'pj':
        for user in USERSpj:
            if user.id == user_id:
                return render_template('portalCliente.html', user = user)
    #if user_perfil == 'pf':
        #Lógica com o banco de dados
    return render_template('index.html')

@app.route('/colaborador', methods=['GET'])
def pgColaborador():
    if session.get('usuario_perfil') == None:
        return render_template('colaboradores/login_colaborador.html')
    elif 'colab_cargo' in session:
        return render_template('colaboradores/colaborador.html', cargo = session.get('colab_cargo'),
        nome = session.get('colab.nome'))
    abort(403)


@app.route('/pagamento/<veiculo>', methods=['GET'])
def pgPagamento(veiculo):
    return render_template('pagamento.html', veiculo = veiculo)


@app.route('/frota', methods=['GET', 'POST'])  #Modularizar esta frota criando funções
def pgFrota():  #adicionar o filtro de preço menor para maior


    veiculos_filtrados = VEICULOS.copy()
    
    # Aplicar filtros apenas se os valores não estiverem vazios

    page = request.args.get('page', 1, type=int)
    per_page = 12

    start = (page-1)*per_page
    end = start + per_page
    total_pages = math.ceil(len(veiculos_filtrados)/per_page)

    veiculos_da_pagina = veiculos_filtrados[start:end]
    
    return render_template('frota.html', 
                           veiculos=veiculos_da_pagina, 
                           page=page, 
                           total_pages=total_pages,
                           filtros_limpos = True)

@app.route('/filtrar', methods=['POST'])
def filtrar():
    modelo = request.form.get('modelo', '')
    categoria = request.form.get('categoria', '')
    marca = request.form.get('marca', '')
    transmissao = request.form.get('transmissao', '')
    combustivel = request.form.get('combustivel', '')
    preco_maximo = request.form.get('preco', '')
    malas_min = request.form.get('malas', '')
    passageiros_min = request.form.get('passageiros', '')
    portas_min = request.form.get('portas', '')

    veiculos_filtrados = VEICULOS.copy()
    
    # Aplicar filtros apenas se os valores não estiverem vazios
    if categoria and categoria != 'todos':
        veiculos_filtrados = [v for v in veiculos_filtrados if v.categoria.lower() == categoria.lower()]
    
    if marca:
        veiculos_filtrados = [v for v in veiculos_filtrados if v.marca.lower() == marca.lower()]
    
    if modelo:
        veiculos_filtrados = [v for v in veiculos_filtrados if v.modelo.lower() == modelo.lower()]
    
    if transmissao:
        veiculos_filtrados = [v for v in veiculos_filtrados if v.transmissao.lower() == transmissao.lower()]
    
    if combustivel:
        veiculos_filtrados = [v for v in veiculos_filtrados if v.combustivel.lower() == combustivel.lower()]
    
    if preco_maximo:
        try:
            preco = float(preco_maximo)
            veiculos_filtrados = [v for v in veiculos_filtrados if v.preco <= preco]
        except ValueError:
            pass
    
    if malas_min:
        try:
            min_malas = int(malas_min)
            veiculos_filtrados = [v for v in veiculos_filtrados if v.malas >= min_malas]
        except ValueError:
            pass
    
    if passageiros_min:
        try:
            min_passageiros = int(passageiros_min)
            # Ordenar por proximidade ao número solicitado (exato primeiro)
            veiculos_filtrados = sorted(
                [v for v in veiculos_filtrados if v.passageiros >= min_passageiros],
                key=lambda x: (x.passageiros == min_passageiros, x.passageiros),
                reverse=True
            )
        except ValueError:
            pass
    
    if portas_min:
        try:
            min_portas = int(portas_min)
            veiculos_filtrados = [v for v in veiculos_filtrados if v.portas >= min_portas]
        except ValueError:
            pass

    page = request.args.get('page', 1, type=int)
    per_page = 12

    start = (page-1)*per_page
    end = start + per_page
    total_pages = math.ceil(len(veiculos_filtrados)/per_page)

    veiculos_da_pagina = veiculos_filtrados[start:end]
    
    return render_template('frota.html', 
                           veiculos=veiculos_da_pagina, 
                           page=page, 
                           total_pages=total_pages,
                           filtros_limpos = False)

@app.route('/logout', methods=['GET']) 
def logout():
    session.clear()
    resposta = make_response(redirect(url_for('index')))

    resposta.set_cookie('user', '', expires=0)
    resposta.set_cookie('perfil', '', expires=0)
    if request.cookies.get('cargo'):
        resposta.set_cookie('cargo', '', expires=0)
    return resposta

@app.errorhandler(401)
def nao_autorizado(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def acesso_proibido(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def erro_interno_servidor(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'