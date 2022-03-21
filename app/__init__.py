from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

##all of the required functionality we instantiate them here
login_manager = LoginManager()
bootstrap = Bootstrap5()
mail = Mail()
moment = Moment()
pagedown = PageDown()
db = SQLAlchemy()

login_manager.login_view = "auth.login"
##create and initialize app
def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	##attach blueprint here
	from .auth import auth
	app.register_blueprint(auth)

	config[config_name].init_app(app)

	mail.init_app(app)
	login_manager.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	pagedown.init_app(app)
	db.init_app(app)

	return app

