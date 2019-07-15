from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# require user to log in access certain sites
# pass in function name of login route
login_manager.login_view = 'users.login'

# beautify flash message
login_manager.login_message_category = 'info'


# Now we can initialize extension
mail = Mail(app)

# import users, an instance of Blueprint class
from app.users.routes import users
from app.donors.routes import donors
from app.main.routes import main
# register that blueprint

app.register_blueprint(users)
app.register_blueprint(donors)
app.register_blueprint(main)