from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from models.treinamento import Treinamento
from extensions import db
from functools import wraps
from datetime import datetime

def coordenador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.role == 'coordenador':
            flash('Acesso restrito a coordenadores.', 'error')
            return redirect(url_for('treinamento.listar'))
        return f(*args, **kwargs)
    return decorated_function

def listar_treinamentos():
    treinamentos = Treinamento.query.all()
    return render_template('treinamento/listar.html', treinamentos=treinamentos)

@coordenador_required
def novo_treinamento():
    if request.method == 'POST':
        
        try:
            titulo = request.form.get('titulo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            carga_horaria = int(request.form.get('carga_horaria', 0))

            # form date inputs are in 'YYYY-MM-DD' format; convert to datetime

            data_inicio = datetime.strptime(request.form.get('data_inicio', ''), '%Y-%m-%d')
            data_fim = datetime.strptime(request.form.get('data_fim', ''), '%Y-%m-%d')
        except ValueError as e:
            flash('Dados do formulário inválidos: ' + str(e), 'error')
            print('Erro de parsing do formulário:', str(e))
            return render_template('treinamento/novo.html')

        # Validações
        if not titulo:
            flash('Título é obrigatório.', 'error')
            return render_template('treinamento/novo.html')

        if carga_horaria <= 0:
            flash('Carga horária deve ser um número positivo.', 'error')
            return render_template('treinamento/novo.html')

        if data_fim < data_inicio:
            flash('Data de término não pode ser anterior à data de início.', 'error')
            return render_template('treinamento/novo.html')

        treinamento = Treinamento(
            titulo=titulo,
            descricao=descricao,
            carga_horaria=carga_horaria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            user_id=current_user.id
        )

        try:
            db.session.add(treinamento)
            db.session.commit()
            flash('Treinamento criado!', 'success')
            return redirect(url_for('treinamento.listar'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar treinamento.', 'error')
            #flash(f'Erro ao criar treinamento: {str(e)}', 'error')
            #print(f'Erro detalhado: {str(e)}') 
            return render_template('treinamento/novo.html')

    return render_template('treinamento/novo.html')
