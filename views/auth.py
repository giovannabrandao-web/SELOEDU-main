from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.users import User
from extensions import db, mail
from utils.token_utils import generate_token, confirm_token
from flask_mail import Message

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('users.dashboard'))
        flash('Credenciais inválidas.', 'danger')
        return render_template('auth/login.html')

    return render_template('auth/login.html')


def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))


def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message(
                subject='Redefinição de senha',
                recipients=[email],
                body=f'Clique no link para redefinir sua senha: {reset_url}'
            )
            mail.send(msg)
            flash(f'Link de redefinição enviado para {email}.', 'info')
        else:
            flash('E-mail não encontrado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    return render_template('auth/forgot_password.html')


def reset_password(token=None):
    if not token:
        flash('Token ausente ou inválido.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    email = confirm_token(token)
    if not email:
        flash('Token expirado ou inválido.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            user.set_password(password)
            db.session.commit()
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Informe uma nova senha.', 'danger')
    return render_template('auth/reset_password.html')


class AuthViews:
    login = staticmethod(login)
    logout = staticmethod(logout)
    forgot_password = staticmethod(forgot_password)
    reset_password = staticmethod(reset_password)

auth = AuthViews
