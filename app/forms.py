from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User
# Syntax for subclass
# class DerivedClassName(BaseClassName):
#     pass


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

	def validate_username(self, username):
		# check if username already exists
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already existed. Please choose another username')

	def validate_email(self, email):
		# check if email already exists
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already existed')


class LoginForm(FlaskForm):
	# username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	# confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Log in')
	remember = BooleanField('Remember me')


class InsertForm(FlaskForm):
	# every insert action has to include donor's name
	name = StringField('Name', validators=[DataRequired()])
	contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
	donation_amount = IntegerField('Donation Amount ($)', validators=[DataRequired(), NumberRange(min=0)])
	donate_event = StringField('Donate Event')
	submit = SubmitField('Insert')
