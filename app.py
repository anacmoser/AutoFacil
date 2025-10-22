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

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
import re
from models.UserPf import UserPf, USERSpf, addUser, delUser, getUserByCpf, getUserByEmail, verificarDuplicidade
from models.UserPj import UserPj, USERSpj, addUserPj
from models.Veiculo import Veiculo, VEICULOS, addVeiculo, removerVeiculo, getVeiById
from controllers.veiculo_controller import veiculo_bp
from controllers.userPf_controller import user_pf_bp
from controllers.userPj_controller import user_pj_bp

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'
app.register_blueprint(veiculo_bp)
app.register_blueprint(user_pf_bp)
app.register_blueprint(user_pj_bp)


def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_cpf(cpf):
    cpf_limpo = ''.join(filter(str.isdecimal, str(cpf))) 
    return len(cpf_limpo) == 11 and cpf_limpo != cpf_limpo[0] * 11

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def pgCadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def pgLogin():
    return render_template('login.html')

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

@app.route('/frota', methods=['GET'])  #Modularizar esta frota criando funções
def pgFrota():  #adicionar o filtro de preço menor para maior

    #Entender este código, aplicar os filtros no html
    categoria = request.args.get('categoria', '')
    marca = request.args.get('marca', '')
    modelo = request.args.get('modelo', '')
    transmissao = request.args.get('transmissao', '')
    combustivel = request.args.get('combustivel', '')
    preco_maximo = request.args.get('preco_maximo', '')
    malas_min = request.args.get('malas_min', '')
    passageiros_min = request.args.get('passageiros_min', '')
    portas_min = request.args.get('portas_min', '')
    
    # Filtrar veículos
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
    
    # Formatar os dados para o template
    veiculos_formatados = []
    for veiculo in veiculos_filtrados:
        veiculos_formatados.append({
            'id': veiculo.id,
            'categoria': veiculo.categoria,
            'marca': veiculo.marca,
            'modelo': veiculo.modelo,
            'transmissao': veiculo.transmissao,
            'preco': f"{veiculo.preco:.2f}",
            'nome': veiculo.nome,
            'imagem': veiculo.imagem,
            'malas': veiculo.malas,
            'passageiros': veiculo.passageiros,
            'portas': veiculo.portas,
            'combustivel': veiculo.combustivel,
            'status': veiculo.status
        })
    
    return render_template('frota.html', veiculos=veiculos_formatados)


 


@app.route('/api/filtrar', methods=['POST']) #refazer
def api_filtrar():
    try:
        # Obter dados do JSON
        data = request.get_json()
        
        categoria = data.get('categoria', '')
        marca = data.get('marca', '')
        modelo = data.get('modelo', '')
        transmissao = data.get('transmissao', '')
        combustivel = data.get('combustivel', '')
        preco_maximo = data.get('preco_maximo', '')
        malas_min = data.get('malas_min', '')
        passageiros_min = data.get('passageiros_min', '')
        portas_min = data.get('portas_min', '')
        
        # Filtrar veículos
        veiculos_filtrados = VEICULOS.copy()
        
        # Aplicar filtros
        if categoria and categoria != 'todos':
            veiculos_filtrados = [v for v in veiculos_filtrados if v['categoria'].lower() == categoria.lower()]
        
        if marca:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['marca'].lower() == marca.lower()]
        
        if modelo:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['modelo'].lower() == modelo.lower()]
        
        if transmissao:
            veiculos_filtrados = [v for v in veiculos_filtrados if v['transmissao'].lower() == transmissao.lower()]
        
        if combustivel:
            veiculos_filtrados = [v for v in veiculos_filtrados if v.get('combustivel', '').lower() == combustivel.lower()]
        
        if preco_maximo:
            try:
                preco = float(preco_maximo)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['preco_diario'] <= preco]
            except ValueError:
                pass
        
        if malas_min:
            try:
                min_malas = int(malas_min)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_malas'] >= min_malas]
            except ValueError:
                pass
        
        if passageiros_min:
            try:
                min_passageiros = int(passageiros_min)
                # Ordenar por proximidade ao número solicitado (exato primeiro)
                veiculos_filtrados = sorted(
                    [v for v in veiculos_filtrados if v['numero_passageiros'] >= min_passageiros],
                    key=lambda x: (x['numero_passageiros'] == min_passageiros, x['numero_passageiros']),
                    reverse=True
                )
            except ValueError:
                pass
        
        if portas_min:
            try:
                min_portas = int(portas_min)
                veiculos_filtrados = [v for v in veiculos_filtrados if v['numero_portas'] >= min_portas]
            except ValueError:
                pass
        
        # Formatar resposta
        resposta = []
        for veiculo in veiculos_filtrados:
            resposta.append({
                'id': veiculo.get('id', 0),
                'categoria': veiculo['categoria'],
                'marca': veiculo['marca'],
                'modelo': veiculo['modelo'],
                'transmissao': veiculo['transmissao'],
                'preco': f"{veiculo['preco_diario']:.2f}",
                'nome': veiculo['nome'],
                'imagem': veiculo['imagem'],
                'malas': veiculo['numero_malas'],
                'passageiros': veiculo['numero_passageiros'],
                'portas': veiculo['numero_portas'],
                'combustivel': veiculo.get('combustivel', 'Flex'),
                'status': veiculo['status']
            })
        
        return jsonify(resposta)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/colaborador', methods=['GET'])
def pgColaborador():
    return render_template('colaboradores/login_colaborador.html')

@app.route('/alterCadastro', methods=['GET']) #Fazer igual a páginade detalhes e passar o id ou buscar o id pela session
def pgAlterCadastro():
    return render_template('alterCadastro.html', )

@app.route('/logout', methods=['GET']) 
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

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


