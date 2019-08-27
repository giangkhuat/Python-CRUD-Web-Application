import os
import unittest
from app.config import Config
from app.config import basedir
from app.models import User
from app import create_app, db
from flask import current_app
import re

class TestConfig(Config):
	# Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
	BCRYPT_LOG_ROUNDS = 4

	# Enable the TESTING flag to disable the error catching during request handling
	# so that you get better error reports when performing test requests against the application.
	TESTING = True

	# Disable CSRF tokens in the Forms (only valid for testing purposes!)
	WTF_CSRF_ENABLED = False

class BasicTests(unittest.TestCase):

	############################
	#### setup and teardown ####
	############################

	def setUp(cls):
		cls.app = create_app(TestConfig)
		cls.app.config.testing = True
		cls.app.config['WTF_CSRF_ENABLED'] = False
		cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

	# executed prior to each test
	def setUpConfig(self):
		with self.app.app_context():
			# If we comment the three lines below it works
			#self.app = app.test_client()
			#self.client = self.app.test_client()
			#tester = self.app.test_client()
			#self.client = self.app.test_client()
			db.create_all()

	# executed after each test
	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

	###############
	#### tests ####
	###############

	def test_main_page(self):
		# test client to mock the functionality of current_app
		self.client = self.app.test_client()
		response = self.client.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

    # Test login page loads correctly
	def test_login_page_load(self):
		self.client = self.app.test_client()
		response = self.client.get('/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'Log In With Admin Account' in response.data)

	def test_incorrect_login(self):
		tester = self.app.test_client()
		response = tester.post('/login', data=dict(username='wrong', password='wrong'), follow_redirects=True)
		expected_mes = 'Login Unsuccessful. Please check email and password'
		self.assertEqual(response.status_code, 200, response.data)
		self.assertTrue(re.search(expected_mes, response.get_data(as_text=True)))

	# Test login behaves correctly given correct credential
	def test_correct_login(self):
	    tester = self.app.test_client()
	    response = tester.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
	    self.assertIn(b'Account', response.data)

if __name__ == '__main__':
	unittest.main()