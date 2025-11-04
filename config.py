import os


class Config:
	SECRET_KEY = os.environ.get('FLASK_SECRET', 'dev-secret')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///seloedu.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'localhost'
	MAIL_PORT = 1025
	MAIL_USE_TLS = False
	MAIL_USERNAME = ""
	MAIL_PASSWORD = ""
	MAIL_DEFAULT_SENDER = "reset_password@seloedu"