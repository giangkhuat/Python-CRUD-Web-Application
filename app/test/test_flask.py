from app import create_app, db
from test.test_basic import TestConfig
from app.models import User
import pytest


# Initialzie application, run before every test
@pytest.fixture(scope="module")
def test_client():
	flask_app = create_app(TestConfig)
	testing_client = flask_app.test_client()

	context = flask_app.app_context()
	context.push()

	yield testing_client

	context.pop()


@pytest.fixture(scope='module')
def init_database():
	# Create the database and the database table
	db.create_all()

	# Insert user data
	user1 = User(email='abc@gmail.com', plaintext_password='FlaskIsAwesome')
	user2 = User(email='bumbleebee@gmail.com', plaintext_password='PaSsWoRd')
	db.session.add(user1)
	db.session.add(user2)

	# Commit the changes for the users
	db.session.commit()

	yield db  # this is where the testing happens!

	db.drop_all()


#@pytest.fixture(scope='module')
#def login(test_client, username, password):
#	return test_client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

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

# Test Main Page load correctly
def test_main_page(test_client):
		response = test_client.get('/', follow_redirects=True)
		assert response.status_code == 200


# Test login page loads correctly
def test_login_page_load(test_client):
	response = test_client.get('/login', content_type='html/text')
	assert response.status_code == 200
	assert b'Log In With Admin Account' in response.data


def test_incorrect_login(test_client):
	response = test_client.post('/login', data=dict(username='wrong', password='wrong'), follow_redirects=True)
	expected_mes = 'Login Unsuccessful. Please check email and password'
	assert response.status_code == 200
	# assertTrue(re.search(expected_mes, response.get_data(as_text=True)))

def test_correct_login(test_client):
    response = test_client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    # response = login(test_client, 'admin', 'admin')
    assert b'Account' in response.data