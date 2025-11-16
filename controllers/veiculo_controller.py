from flask import Blueprint, render_template, abort, request, redirect, url_for
from datetime import datetime
import math
from models.Veiculo import Veiculos
from models import db
import cloudinary
import cloudinary.uploader

veiculo_bp = Blueprint('veiculo_bp', __name__)
id = 21

@veiculo_bp.route('/reserva', methods=['GET'])
def pgReserva():
    return render_template('reserva.html')

@veiculo_bp.route('/frota', methods=['GET', 'POST'])  #Modularizar esta frota criando funções
def pgFrota():  #adicionar o filtro de preço menor para maior
    veiculos_filtrados = Veiculos.query
    # Aplicar filtros apenas se os valores não estiverem vazios

    page = request.args.get('page', 1, type=int)
    per_page = 12

    paginacao = veiculos_filtrados.paginate(page=page, per_page=per_page)
    veiculos_da_pagina = paginacao.items
    total_pages = paginacao.pages

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
    malas_min = request.form.get('nMalas', '')
    passageiros_min = request.form.get('nPassageiros', '')
    portas_min = request.form.get('nPortas', '')

    veiculos_filtrados = Veiculos.query
    
    # Aplicar filtros apenas se os valores não estiverem vazios
    if categoria and categoria != "todos":
        veiculos_filtrados = veiculos_filtrados.filter_by(categoria=categoria)
    
    if marca:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.marca.ilike(marca))
    
    if modelo:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.modelo.ilike(modelo))
    
    if transmissao:
        veiculos_filtrados = veiculos_filtrados.filter_by(transmissao=transmissao)

    if combustivel:
        veiculos_filtrados = veiculos_filtrados.filter_by(combustivel=combustivel)
    
    if preco_maximo:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.precoDiario <= float(preco_maximo))
    
    if malas_min:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.nMalas >= int(malas_min))
    
    if passageiros_min:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.nPassageiros >= int(passageiros_min))
    
    if portas_min:
        veiculos_filtrados = veiculos_filtrados.filter(Veiculos.nPortas >= int(portas_min))

    page = request.args.get('page', 1, type=int)
    per_page = 12

    paginacao = veiculos_filtrados.paginate(page=page, per_page=per_page)
    veiculos_da_pagina = paginacao.items
    total_pages = paginacao.pages

    
    return render_template('frota.html', 
                           veiculos=veiculos_da_pagina, 
                           page=page, 
                           total_pages=total_pages,
                           filtros_limpos = False)

@veiculo_bp.route('/frota/<int:veiculo_id>')
def detalheVeiculo(veiculo_id):
    veiculo = Veiculos.query.get(veiculo_id)
    similares = []

    if veiculo is None:
        abort(404)
    
    similares = Veiculos.query.filter_by(categoria=veiculo.categoria).all()
        
    return render_template('detalhe_veiculo.html', veiculo=veiculo, veiculos_similares = similares)

@veiculo_bp.route('/reserva/<int:veiculo_id>', methods=['POST'])
def reserva(veiculo_id):
    formato='%Y-%m-%d'
    data_ret = datetime.strptime(request.form.get('dataRetirada'), formato).date()
    data_dev = datetime.strptime(request.form.get('dataDev'), formato).date()

    dias = (data_dev - data_ret).days

    local = request.form.get('localRetirada')

    for veiculo in Veiculos.query:
        if veiculo.id == veiculo_id:
            if veiculo.status == 'disponível':
                #Verifica se há este carro nesse local
                #Verifica se esse carro deste local está reservado entre as data_ret e data_dev
                #Se sim, veiculo.status = 'indiponível'
                #return redirect(url_for('pgPagamento', veiculo=veiculo))
                #valorTotal = veiculo.precoDiario * dias * local.porcentagem
                valorTotal = veiculo.precoDiario * dias
                return render_template('pagamento.html', veiculo = veiculo, valorTotal = valorTotal)
        #return render_template('detalhe_veiculo.html', status = 'Veículo indiponível nesta data', veiculo=veiculo)
    
@veiculo_bp.route('/upload/<int:veiculo_id>', methods=['POST'])
def upload_imagem(veiculo_id):
    imagem = request.files['imagem']
    result = cloudinary.uploader.upload(imagem)

    veiculo = Veiculos.query.get(veiculo_id)
    veiculo.imagem = result["secure_url"]

    db.session.commit()
    return result["secure_url"]

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