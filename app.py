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

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'
app.register_blueprint(veiculo_bp)

id_counter_Pf = 2     #vai pro cotroller
id_counter_pj = 2  #vai pro controller

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
def mudarCadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def mudarLogin():
    return render_template('login.html')

@app.route('/aluguelMensal', methods=['GET'])
def mudarAluguelMensal():
    return render_template('aluguelmensal.html')

@app.route('/empresas', methods=['GET'])
def mudarEmpresas():
    return render_template('empresas.html')

@app.route('/minhasReservas', methods=['GET'])
def mudarMinhasReservas():
    if session.get('usuario_logado') == None:
        abort(401)
    return render_template('minhas_reservas.html')

@app.route('/frota', methods=['GET'])  #Modularizar esta frota criando funções
def mudarFrota():  #adicionar o filtro de preço menor para maior

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

@app.route('/cadastrarPf', methods=['POST'])
def cadastro():
    global id_counter_Pf  # Usar a variável global
    
    # Obter dados do formulário
    nome = request.form.get('nome', '').strip()
    nascimento = request.form.get('nascimento', '')
    cpf = request.form.get('cpf', '')
    cpf = re.sub(r'[^0-9]', '', cpf) #Acho que não há necessidade, porque eu limpo o cpf na validação em User
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
 
@app.route('/cadastrarPj', methods=['POST'])
def cadastroEmpresa():
    global id_counter_pj
    tipo_conta = request.args.get('tipo_conta')

    rs = request.form.get('razao_social', '').strip()
    nf = request.form.get('nome_fantasia', '').strip()
    cnpj = request.form.get('cnpj', '')
    ie = request.form.get('inscricao_estadual', '').strip()
    ramo = request.form.get('ramo_atividade', '')
    tamanho = request.form.get('tamanho_empresa', '')
    nomeRep = request.form.get('nome_representante', '').strip()
    cpfRep = request.form.get('cpf_representante', '')
    cargoRep = request.form.get('cargo_representante', '').strip()
    phone = request.form.get('telefone_empresa', '')
    cell = request.form.get('celular_empresa', '')
    email = request.form.get('email_empresa', '').strip()
    cep = request.form.get('cep_empresa', '')
    logra = request.form.get('logradouro_empresa', '')
    num = request.form.get('numero_empresa', '')
    complemento = request.form.get('complemento_empresa', '')
    bairro = request.form.get('bairro_empresa', '').strip()
    estado = request.form.get('estado_empresa', '').strip()
    cidade = request.form.get('cidade_empresa', '').strip()
    senha = request.form.get('senha_empresa', '')
    confirmar = request.form.get('confirmar_empresa', '')
    termos = request.form.get('termos')
    autorizacao = request.form.get('autorizacao')

    campos_obrigatorios = [rs, nf, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, phone, email, cep, logra, num, bairro, estado, cidade, senha, confirmar]
    for campo in campos_obrigatorios:
        if not campo:
            return render_template('cadastro.html', erros='Todos os campos obrigatórios devem ser preenchidos')

    if not termos:
        return render_template('cadastro.html', erros='Você deve aceitar os Termos de Uso.')
    if not autorizacao:
        return render_template('cadastro.html', erros='Você deve aceitar a Autorização.')
    try:
        novoUser = UserPj(id_counter_pj, rs, nf, cnpj, ramo, tamanho, nomeRep, cpfRep, cargoRep, phone, email, cep, logra, num, bairro, estado, cidade, senha, confirmar, ie ,cell, complemento)
        adicao = addUserPj(novoUser) #Verificar por nome também (já existe por email e cpf)
        if adicao == True: #Se não for true será a lista de erros
            id_counter_pj += 1
            return redirect(url_for('login'))
        else:
            return render_template('cadastro.html', erros=adicao)
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
        
        return render_template('cadastro.html', erros=erros, tipo_conta=tipo_conta, tipo_conta_juridica=(tipo_conta == 'juridica'))


@app.route('/logar', methods=['GET', 'POST']) #Modularizar as verificações
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('password')

        if '@' in user:
            #verificação por email
            if not validar_email(user):
                return render_template('login.html', erro = 'E-mail inválido')
            for usuario in USERSpf:
                if usuario.getUserContato('email') == user :
                    if usuario.senha == senha:
                        session['usuario_logado'] = usuario.getUserDados('nome')
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')
        else: 
            #verificação por cpf
            cpf = re.sub(r'[^0-9]', '', user)
            if not validar_cpf(cpf):
                return render_template('login.html', erro = 'Digite e-mail ou CPF inválidos')
            for usuario in USERSpf:
                if usuario.cpf == cpf:
                    if usuario.senha == senha:
                        session['usuario_logado'] = usuario.getUserDados('nome')
                        return render_template('index.html')
                    return render_template('login.html', erro = 'Senha incorreta')
            return render_template('login.html', erro = 'Usuário não encontrado')        
    
    return render_template('login.html')

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

@app.route('/logout')
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


