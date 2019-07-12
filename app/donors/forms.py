from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


class InsertForm(FlaskForm):
	# every insert action has to include donor's name
	name = StringField('Name', validators=[DataRequired()])
	contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
	donation_amount = IntegerField('Donation Amount ($)', validators=[DataRequired(), NumberRange(min=0)])
	donate_event = StringField('Donate Event')
	submit = SubmitField('Insert')

