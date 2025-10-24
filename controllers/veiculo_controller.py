from flask import Blueprint, render_template, abort
from models.Veiculo import VEICULOS, getVeiById, Veiculo

veiculo_bp = Blueprint('veiculo_bp', __name__)

@veiculo_bp.route('/frota/<int:veiculo_id>')
def detalheVeiculo(veiculo_id):
    veiculo = getVeiById(veiculo_id)
    if veiculo is None:
        abort(404)
    return render_template('detalhe_veiculo.html', veiculo=veiculo)