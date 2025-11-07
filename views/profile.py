from flask import render_template, request, redirect, url_for, flash, current_app
from utils.uploads import save_image, remove_file_safe
from flask_login import login_required, current_user
from models.profile import Profile
from extensions import db
import os
from werkzeug.utils import secure_filename

@login_required
def profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        telefone = request.form.get('telefone')
        instituicao = request.form.get('instituicao')
        cargo = request.form.get('cargo')
        bio = request.form.get('bio')
        foto = request.files.get('foto')
        
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
        profile.telefone = telefone
        profile.instituicao = instituicao
        profile.cargo = cargo
        profile.bio = bio

        if foto and foto.filename:
            remove_file_safe(profile.foto)
            remove_file_safe(profile.foto_thumb)

            filename, thumb_name = save_image(file_storage=foto, user_name=current_user.nome)
            profile.foto = filename
            profile.foto_thumb = thumb_name

        elif not profile.foto_thumb:
            _, thumb_name = save_image(user_name=current_user.nome)
            profile.foto_thumb = thumb_name

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('users/profile.html', profile=profile)