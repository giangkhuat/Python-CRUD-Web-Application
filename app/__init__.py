from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Giang/PycharmProjects/databaseProj/app/site.db'


# Instantiate database

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# require user to log in access certain sites
# pass in function name of login route
login_manager.login_view = 'login'



# beautify flash message
login_manager.login_message_category = 'info'


from app import routes
