"""
TAREFAS:
    * Arquitetura / organização MVC                      COMPLETO: view, models
    * Páginas de erro (404, 403, 401)
        *Definir a quais páginas o user tem acesso sem estar logado
    * Arquivo para APIs (Para diminuir a quantidade de html)
    * Api de CEP para pré-preenchimento do formulário
    * Lógica da página específica igual ao do exercício do agostinho (PRODUTOS)
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re
from models.User import User, USERS, addUser, delUser, getUserByCpf, getUserByEmail, verificarDuplicidade
from models.Veiculo import Veiculo, VEICULOS, addVeiculo, removerVeiculo, getVeiById

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'
id_counter = 2
#users = USERS

userTest = User(1, 'teste da silva', '2000-10-12', '12345678909', '11923471103', 'teste@gmail.com', '12345678', 'teste Bairro', 'teste Estado', 'teste Cidade', '12345678', '12345678','teste logradouro', '2222', 'teste Complemento')

addUser(userTest)

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

@app.route('/frota', methods=['GET'])  #Modularizar esta frota criando funções
def mudarFrota():  #adicionar o filtro de preço menor para maior
    # Obter parâmetros de filtro da URL
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

@app.route('/cadastrar', methods=['POST'])
def cadastro():
    global id_counter  # Usar a variável global
    
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
        novoUser = User(id_counter, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, confirmar_senha, logradouro, numero, complemento)
        adicao = addUser(novoUser) #Verificar por nome também (já existe por email e cpf)
        if adicao == True: #Se não for true será a lista de erros
            id_counter += 1
            return redirect(url_for('login'))
        else:
            return render_template('cadastro.html', erros=adicao)
    except ValueError as e:
        if isinstance(e.args[0], list):
            erros = e.args[0]
        else:
            erros = [str(e)]
        
        return render_template('cadastro.html', erros=erros)
 
"""@app.route('/cadastrar-empresa', methods=['POST'])
def cadastroEmpresa():"""
    

@app.route('/logar', methods=['GET', 'POST']) #Modularizar as verificações
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('password')

        if '@' in user:
            #verificação por email
            if not validar_email(user):
                return render_template('login.html', erro = 'E-mail inválido')
            for usuario in USERS:
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
            for usuario in USERS:
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

if __name__ == '__main__':
    app.run(debug=True)


