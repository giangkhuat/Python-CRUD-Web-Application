from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from flask_migrate import Migrate


# We don't move extensions inside function create_app()
# because we want them to be created outside function
# but initialized inside function
# so one extension object can be used on multiple app

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# require user to log in access certain sites
# pass in function name of login route
login_manager.login_view = 'users.login'
# beautify flash message
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	# Initialize extensions
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	migrate.init_app(app, db)

	# import users, an instance of Blueprint class
	from app.users.routes import users
	from app.donors.routes import donors
	from app.main.routes import main
	from app.errors.handlers import errors
	# register that blueprint
	app.register_blueprint(users)
	app.register_blueprint(donors)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app


