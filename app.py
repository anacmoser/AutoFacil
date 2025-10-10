"""
TAREFAS:
    * Arquitetura / organização MVC
    * Páginas de erro (404, 403, 401)
    * Arquivo para APIs
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re
from models import User, Users, Veiculo, Veiculos

app = Flask(__name__)
app.secret_key = 'chave_secreta_autofacil'
id_counter = 2
users = Users([])
#UserTest == usuarios

userTest = User(1, 'teste', '2000-10-12', '12345678909', '11923471103', 'teste@gmail.com', '12345678', 'teste Bairro', 'teste Estado', 'teste Cidade', '12345678', '12345678','teste logradouro', '2222', 'teste Complemento')

users.adicionar(userTest)

v1 = Veiculo(1, "econômico", "Econômico", "Fiat", "Mobi", "manual", 95.00, "Fiat Mobi", "https://production.autoforce.com/uploads/version/profile_image/10921/model_main_webp_comprar-like-1-0_9eee82ebb4.png.webp", 2, 5, 4, "Flex", "disponível")
v2 = Veiculo(2, "econômico", "Econômico","Renault", "Kwid", "manual", 100.00,"Renault Kwid","https://www.webmotors.com.br/imagens/prod/348031/RENAULT_KWID_1.0_12V_SCE_FLEX_OUTSIDER_MANUAL_34803110315083122.webp", 2, 5, 4, "Flex","disponível")
v3 = Veiculo(3, "econômico", "Econômico", "Hyundai", "HB20", "manual", 110.00, "Hyundai HB20", "/static/img/hb20.webp", 3, 5, 4, "Flex", "disponível")
v4 = Veiculo(4, "econômico", "Econômico", "Chevrolet", "Onix", "manual", 115.00, "Chevrolet Onix", "/static/img/onix.png", 3, 5, 4, "Flex", "disponível")
v5 = Veiculo(5, "econômico", "Econômico", "Volkswagen", "Gol", "manual", 105.00, "Volkswagen Gol", "https://cdn.motor1.com/images/mgl/YAAopq/s3/volkswagen-gol-1.0-2023.jpg", 2, 5, 4, "Flex", "disponível")
v6 = Veiculo(6, "sedan", "Sedan", "Toyota", "Corolla", "automático", 180.00, "Toyota Corolla", "/static/img/corolla.png", 3, 5, 4, "Gasolina", "disponível")
v7 = Veiculo(7, "sedan", "Sedan", "Honda", "Civic", "automático", 185.00, "Honda Civic", "https://di-uploads-pod33.dealerinspire.com/hendrickhondacharlotte/uploads/2021/03/mlp-img-top-2021-civic.png", 3, 5, 4, "Gasolina", "disponível")
v8 = Veiculo(8, "sedan", "Sedan", "Nissan", "Sentra", "automático", 170.00, "Nissan Sentra", "https://www.nissan-cdn.net/content/dam/Nissan/br/site/veiculos/sentra-my25/thumbs/sentra_exclusive_int_premium.png", 3, 5, 4, "Flex", "disponível")
v9 = Veiculo(9, "sedan", "Sedan", "Chevrolet", "Cruze", "automático", 175.00, "Chevrolet Cruze", "https://revistacarro.com.br/wp-content/uploads/2018/05/chevrolet_cruze_sport6_ltz.png", 3, 5, 4, "Flex", "disponível")
v10 = Veiculo(10, "sedan", "Sedan", "Volkswagen", "Virtus", "automático", 165.00, "Volkswagen Virtus", "https://cadastro.motorleads.co/public/images/20240130022136-v5.png", 3, 5, 4, "Flex", "disponível")
v11 = Veiculo(11, "suv", "SUV", "Jeep", "Compass", "automático", 220.00, "Jeep Compass", "https://www.webmotors.com.br/imagens/prod/348683/JEEP_COMPASS_1.3_T270_TURBO_FLEX_S_AT6_3486831606189095.webp?s=fill&w=170&h=125&t=true", 4, 5, 4, "Diesel", "disponível")
v12 = Veiculo(12, "suv", "SUV", "Hyundai", "Creta", "automático", 200.00, "Hyundai Creta", "https://www.webmotors.com.br/imagens/prod/348376/HYUNDAI_CRETA_1.6_16V_FLEX_ACTION_AUTOMATICO_34837618173811432.webp", 3, 5, 4, "Flex", "disponível")
v13 = Veiculo(13, "suv", "SUV", "Honda", "HR-V", "automático", 210.00, "Honda HR-V", "https://production.autoforce.com/uploads/version/profile_image/9408/comprar-exl-honda-sensing_f6ae5428c9.png", 3, 5, 4, "Gasolina", "disponível")
v14 = Veiculo(14, "suv", "SUV", "Nissan", "Kicks", "automático", 195.00, "Nissan Kicks", "https://www.nissan.com.br/content/dam/Nissan/br/site/veiculos/kicks-play/360/advance/branco-diamond/01.png.ximg.c1h.360.png", 3, 5, 4, "Flex", "disponível")
v15 = Veiculo(15, "suv", "SUV", "Chevrolet", "Tracker", "automático", 205.00, "Chevrolet Tracker", "https://www.autoclachevrolet.com.br/content/dam/chevrolet/sa/br/pt/master/home/suvs/tracker/tracker-myr-2026/2-colorizer/lt-at-turbo/chevrolet-tracker-lt-preto-ouro-negro.jpg?imwidth=1920", 3, 5, 4, "Flex", "disponível")
v16 = Veiculo(16, "luxo", "Luxo", "BMW", "Série 3", "automático", 450.00, "BMW Série 3", "https://www.bmw.com.br/content/dam/bmw/common/all-models/3-series/sedan/2024/navigation/bmw-3-series-ice-lci-modelfinder.png", 4, 5, 4, "Gasolina", "disponível")
v17 = Veiculo(17, "luxo", "Luxo", "Audi", "A4", "automático", 460.00, "Audi A4", "https://www.webmotors.com.br/imagens/prod/379665/AUDI_A4_2.0_TFSI_MHEV_S_LINE_QUATTRO_S_TRONIC_37966510582707039.webp", 4, 5, 4, "Gasolina", "disponível")
v18 = Veiculo(18, "luxo", "Luxo", "Mercedes-Benz", "C180", "automático", 480.00, "Mercedes-Benz C180", "https://www.webmotors.com.br/imagens/prod/347940/MERCEDESBENZ_C_180_1.6_CGI_GASOLINA_SPORT_COUPE_9GTRONIC_34794009590838032.webp", 4, 5, 4, "Gasolina", "disponível")
v19 = Veiculo(19, "luxo", "Luxo", "Volvo", "XC60", "automático", 500.00, "Volvo XC60", "https://www.webmotors.com.br/imagens/prod/348860/VOLVO_XC60_2.0_T8_RECHARGE_POLESTAR_ENGINEERED_AWD_GEARTRONIC_34886011041803311.webp", 4, 5, 4, "Híbrido", "disponível")
v20 = Veiculo(20, "luxo", "Luxo", "Jaguar", "XE", "automático", 520.00, "Jaguar XE", "https://www.webmotors.com.br/imagens/prod/348195/JAGUAR_XE_2.0_16V_INGENIUM_P250_GASOLINA_RDYNAMIC_S_4P_AUTOMATICO_34819510562480227.webp", 4, 5, 4, "Gasolina", "disponível")

veiculos_objetos = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20]
veiculos = Veiculos()

for veiculo in veiculos_objetos:
    veiculos.adicionar(veiculo)

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
def mudarFrota():
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
    veiculos_filtrados = veiculos_locacao.copy()
    
    # Aplicar filtros apenas se os valores não estiverem vazios
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
    
    # Formatar os dados para o template
    veiculos_formatados = []
    for veiculo in veiculos_filtrados:
        veiculos_formatados.append({
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
    
    return render_template('frota.html', veiculos=veiculos_formatados)

@app.route('/cadastrar', methods=['POST'])
def cadastro():
    global id_counter  # Usar a variável global
    
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
        novoUser = User(id_counter, nome, nascimento, cpf, celular, email, cep, bairro, estado, cidade, senha, confirmar_senha, logradouro, numero, complemento)
        try: 
            users.adicionar(novoUser) #Verificar por nome também (já existe por email e cpf)
            id_counter += 1
            return redirect(url_for('login'))
        except:
            return render_template('cadastro.html', erros=['CPF e/ou email já estão em uso'])
    except:
        return render_template('cadastro.html', erros=['Campo(s) inválido(s)'])
 
    


@app.route('/logar', methods=['GET', 'POST']) #Modularizar as verificações
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('password')

        if '@' in user:
            #verificação por email
            if not validar_email(user):
                return render_template('login.html', erro = 'E-mail inválido')
            for usuario in users.getUsers():
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
            for usuario in users.getUsers():
                if usuario.getUserDados('cpf') == cpf:
                    if usuario.verificarSenha(usuario.senha, senha):
                        session['usuario_logado'] = usuario
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
        veiculos_filtrados = veiculos.copy()
        
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


