from flask import Blueprint, render_template, abort, request, redirect, url_for
import math
from models.Veiculo import VEICULOS, getVeiById, Veiculo

veiculo_bp = Blueprint('veiculo_bp', __name__)
id = 21

@veiculo_bp.route('/reserva', methods=['GET'])
def pgReserva():
    return render_template('reserva.html')

@veiculo_bp.route('/frota', methods=['GET', 'POST'])  #Modularizar esta frota criando funções
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

@veiculo_bp.route('/filtrar', methods=['POST'])
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

@veiculo_bp.route('/frota/<int:veiculo_id>')
def detalheVeiculo(veiculo_id):
    veiculo = getVeiById(veiculo_id)
    similares = []

    if veiculo is None:
        abort(404)
    
    for i in VEICULOS:
        if i.categoria == veiculo.categoria:
            similares.append(i)
        
    return render_template('detalhe_veiculo.html', veiculo=veiculo, veiculos_similares = similares)

@veiculo_bp.route('/reserva/<int:veiculo_id>', methods=['POST'])
def reserva(veiculo_id):
    data_ret = request.form.get('dataRetirada')
    data_dev = request.form.get('dataDev')
    local = request.form.get('localRetirada')
    for veiculo in VEICULOS:
        if veiculo.id == veiculo_id:
            if veiculo.status == 'disponível':
                #Verifica se há este carro nesse local
                #Verifica se esse carro deste local está reservado entre as data_ret e data_dev
                #Se sim, veiculo.status = 'indiponível'
                #return redirect(url_for('pgPagamento', veiculo=veiculo))
                return render_template('pagamento.html', veiculo = veiculo)
        return render_template('detalhe_veiculo.html', status = 'Veículo indiponível nesta data', veiculo=veiculo)
    


'''@veiculo_bp.route('adicionarVeiculo', methods=['POST'])
def addVeiculo():
    global id
    tipo = request.form.get('tipo', '') 
    categoria= request.form.get('categoria', '') 
    marca = request.form.get('marca', '') 
    modelo = request.form.get('modelo', '') 
    transmissao = request.form.get('transmissao', '') 
    precoDiario = request.form.get('precoDiario', '') 
    nome = request.form.get('nome', '') 
    img = request.form.get('imagem', '') 
    nMala = request.form.get('nMalas', '')    
    nPassageiros = request.form.get('nPasageiros', '') 
    nPortas = request.form.get('nPortas', '') 
    combustivel = request.form.get('combustivel', '') 
    status = request.form.get('status', '')  

    campos = [tipo, categoria, marca, modelo, transmissao, precoDiario, nome, img, nMala, nPassageiros, nPortas, combustivel, status]
    for campo in campos:
        if not campo:
            return render_template('colaboradores/colaborador.html', erro = 'Preencha todos os campos')
        '''