from app import create_app, db
from app.config import Config
from app.models import User
import pytest

class TestConfig(Config):
	# Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
	BCRYPT_LOG_ROUNDS = 4

	# Enable the TESTING flag to disable the error catching during request handling
	# so that you get better error reports when performing test requests against the application.
	TESTING = True

	# Disable CSRF tokens in the Forms (only valid for testing purposes!)
	WTF_CSRF_ENABLED = False

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