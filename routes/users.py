from flask import Blueprint, request, render_template, flash
from flask_login import login_required, current_user
from extensions import db
from models.profile import Profile 
from views.users import (
    dashboard_view, list_users, create_user,
    show_user, edit_user, delete_user, render_perfil_page
)

users_bp = Blueprint("users", __name__)


@users_bp.route("/dashboard")
@login_required
def dashboard():
    return dashboard_view(current_user)

@users_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def atualizar_perfil():
    usuario = current_user
    perfil = usuario.perfil 

    if request.method == 'POST':
        telefone = request.form.get('telefone')
        instituicao = request.form.get('instituicao')
        cargo = request.form.get('cargo')
        bio = request.form.get('bio')
        
        if perfil is None:
            perfil = Profile(
                user_id=usuario.id,
                telefone=telefone,
                instituicao=instituicao,
                cargo=cargo,
                bio=bio
            )
            db.session.add(perfil)
        else:
            perfil.telefone = telefone
            perfil.instituicao = instituicao
            perfil.cargo = cargo
            perfil.bio = bio

        try:
            db.session.commit()
            flash('Seu perfil foi atualizado com sucesso!', 'success')
            return redirect(url_for('users.atualizar_perfil'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar o perfil: {e}', 'danger')
    
    return render_perfil_page(usuario, perfil)


@users_bp.route("/list", methods=["GET"])
@login_required
def index():
    return list_users()


@users_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        return create_user()
    return create_user()


@users_bp.route("/<int:id>", methods=["GET"])
@login_required
def show(id):
    return show_user(id)


@users_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    if request.method == "POST":
        return edit_user(id)
    return edit_user(id)


@users_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    return delete_user(id)
