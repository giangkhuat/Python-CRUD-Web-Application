from app import db, login_manager
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

