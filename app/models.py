from app import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


# function return an user by user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    donors = db.relationship('Donor', backref='admin', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # pass in user ID to serialize an object (convert to a byte stream)
        # return the token
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    # If token is verified, function return user with user_id
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        # try loading the token
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    contact_email = db.Column(db.String(120), unique=True)
    donation_amount = db.Column(db.Integer, nullable=False)
    donate_event = db.Column(db.String(50), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Donor('{self.name}', '{self.contact_email}')"

