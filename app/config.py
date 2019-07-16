import os
# Add these stuff from Miguel Grinberg tutorial
from os import getenv

# from MG tutorial
# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

class Config:
	#SECRET_KEY = os.environ.get('SECRET_KEY')
	SECRET_KEY=getenv('SECRET_KEY', None)
	assert SECRET_KEY
	#SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_DATABASE_URI=getenv('SQLALCHEMY_DATABASE_URI', None)
	assert SQLALCHEMY_DATABASE_URI
	# Setting up email port and server so the application knows where to send
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
