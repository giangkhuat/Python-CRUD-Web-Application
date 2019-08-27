from app.models import User
import pytest


# Create new user
@pytest.fixture(scope='module')
def new_user():
	user = User(username='bumble',email='bumbleblee@gmail.com', password='Flask')
	return user

# Test New User
def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated,
    """
    assert new_user.email == 'bumbleblee@gmail.com'
    assert new_user.hashed_password != 'Flask'
    assert not new_user.authenticated


def test_incorrect_login(test_client):
	response = test_client.post('/login', data=dict(username='wrong', password='wrong'), follow_redirects=True)
	expected_mes = 'Login Unsuccessful. Please check email and password'
	assert response.status_code == 200
	# assertTrue(re.search(expected_mes, response.get_data(as_text=True)))

def test_correct_login(test_client):
    response = test_client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    # response = login(test_client, 'admin', 'admin')
    assert b'Account' in response.data