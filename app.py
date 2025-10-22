# app.py
from flask import Flask, render_template
from models.users import db, User
from extensions import login_manager, mail
from config import Config
from routes.auth import auth_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seloedu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # cria usuário master se não existir
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@seloedu.com").first():
            master = User(
                nome="Admin Master",
                email="admin@seloedu.com",
                role="master"
            )
            master.set_password("123456")
            db.session.add(master)
            db.session.commit()

    # rota principal
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)