import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Giang/PycharmProjects/databaseProj/app/site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# require user to log in access certain sites
# pass in function name of login route
login_manager.login_view = 'login'

# beautify flash message
login_manager.login_message_category = 'info'

# Setting up email port and server so the application knows where to send
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

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