from ..models import User
from .fixture import test_client
from flask import request
import pytest
from app import bcrypt


# Create new user
@pytest.fixture(scope='module')
def new_user():
	user = User(username='bumble', email='bumbleblee@gmail.com', password='flask')
	return user


# Test New User
def test_register_user(test_client, new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated,
    """
    response = test_client.post('/register', data=dict(username=new_user.username, email=new_user.email, password=new_user.password),follow_redirects=True)
    assert new_user.email == 'bumbleblee@gmail.com'
    assert new_user.username == 'bumble'
    assert new_user.password == 'flask'
    user = User.query.filter_by(email='bumblebee@gmail.com').first()
    assert user.username == '<username - bumble>'
    assert response.status_code == 200
    #assert b'Your account has been created! You are now able to log in' in response.data
    assert b'Log In With Admin Account' in response.data

def test_incorrect_register(test_client):
	# If wrong email
	response = test_client.post('register/', data=dict(
		username='chicken', email='chicken',
		password='python', confirm='python'
	), follow_redirects=True)
	assert b'Invalid email address.' in response.data
	assert b'/register/' in request.url



def test_incorrect_login(test_client):
	response = test_client.post('/login', data=dict(username='wrong', password='wrong'), follow_redirects=True)
	expected_mes = 'Login Unsuccessful. Please check email and password'
	assert response.status_code == 200
	# assertTrue(re.search(expected_mes, response.get_data(as_text=True)))

def test_correct_login(test_client):
    response = test_client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    # response = login(test_client, 'admin', 'admin')
    assert b'Account' in response.data