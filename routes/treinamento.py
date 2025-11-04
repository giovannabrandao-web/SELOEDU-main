from flask import Blueprint
from views.treinamento_view import (
    listar_treinamentos,
    novo_treinamento
)
from flask_login import login_required

treinamento_bp = Blueprint('treinamento', __name__)

@treinamento_bp.route('/listar', methods=['GET'])
@login_required
def listar():
    return listar_treinamentos()

@treinamento_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    return novo_treinamento()
