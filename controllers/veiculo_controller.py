from flask import Blueprint, render_template, abort, request, redirect, url_for
from models.Veiculo import VEICULOS, getVeiById, Veiculo

veiculo_bp = Blueprint('veiculo_bp', __name__)
id = 21

@veiculo_bp.route('/frota/<int:veiculo_id>')
def detalheVeiculo(veiculo_id):
    veiculo = getVeiById(veiculo_id)
    if veiculo is None:
        abort(404)
    return render_template('detalhe_veiculo.html', veiculo=veiculo)

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