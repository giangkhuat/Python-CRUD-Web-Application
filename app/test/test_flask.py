import pytest
from .fixture import test_client


# Test Main Page load correctly
def test_main_page(test_client):
		response = test_client.get('/', follow_redirects=True)
		assert response.status_code == 200


# Test login page loads correctly
def test_login_page_load(test_client):
	response = test_client.get('/login', content_type='html/text')
	assert response.status_code == 200
	assert b'Log In With Admin Account' in response.data


# Test Home Page loads correctly
def test_home_page(test_client):
	response = test_client.get('/home', follow_redirects=True)
	assert response.status_code == 200

# Test About Page loads correctly
def test_about_page(test_client):
	response = test_client.get('/about', follow_redirects=True)
	assert response.status_code == 200

# Test Register Page loads
def test_register_page(test_client):
	response = test_client.post('/register', follow_redirects=True)
	assert response.status_code == 200
	assert b'Register Form' in response.data
	assert b'Login' in response.data
	assert b'Log Out' not in response.data