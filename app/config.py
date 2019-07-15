

class Config:
	SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
	SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/Giang/PycharmProjects/databaseProj/app/site.db'
	# Setting up email port and server so the application knows where to send
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
