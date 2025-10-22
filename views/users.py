from flask import render_template, request, redirect, url_for, flash
from models.users import db, User

def render_perfil_page(usuario, perfil):
    return render_template(
        'users/profile.html', 
        usuario=usuario, 
        perfil=perfil,
    )

def dashboard_view(current_user):
    return render_template("dashboard.html", user=current_user)


def list_users():
    users = User.query.all()
    return render_template("users/index.html", users=users)


def create_user():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "danger")
            return redirect(url_for("users.new"))
        user = User(nome=nome, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for("users.index"))
    return render_template("users/form.html")


def show_user(id):
    user = User.query.get_or_404(id)
    return render_template("users/show.html", user=user)


def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.nome = request.form.get("nome")
        user.email = request.form.get("email")
        password = request.form.get("password")
        if password:
            user.set_password(password)
        db.session.commit()
        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("users.show", id=user.id))
    return render_template("users/form.html", user=user)


def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuário excluído com sucesso.", "success")
    return redirect(url_for("users.index"))
