from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


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


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')

	# User can update their accounts and nothing changes
	# But we need to check that they enter correct username and password
	# when they update
	# So import current_user from flask_login
	# run validation rules if they fail to verify
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already existed. Please choose another username')

	def validate_email(self, email):
		# check if email already exists
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already existed')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		# check if email already exists
		user = User.query.filter_by(email=email.data).first()
		# If user doesnt exist
		if user is None:
			raise ValidationError('No account associated with the email. Please register first')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Reset Password')
