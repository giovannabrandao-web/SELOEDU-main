from flask import render_template, request, redirect, url_for, flash, current_app
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
        
            # Ensure uploads directory exists
            uploads_rel_dir = os.path.join('static', 'uploads')
            uploads_abs_dir = os.path.join(current_app.root_path, uploads_rel_dir)
            os.makedirs(uploads_abs_dir, exist_ok=True)

            # Sanitize filename and save using absolute path, store relative path in DB
            safe_name = secure_filename(f"{current_user.id}_{foto.filename}")
            save_abs_path = os.path.join(uploads_abs_dir, safe_name)
            foto.save(save_abs_path)

            # store path relative to the `static` folder so templates can do url_for('static', filename=...)
            profile.foto = os.path.join('uploads', safe_name).replace('\\', '/')
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('users/profile.html', profile=profile)
