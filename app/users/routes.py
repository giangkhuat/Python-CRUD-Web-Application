from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Donor
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from app.users.util import send_reset_email

users = Blueprint('users', __name__)

# Register page

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # Check if form is valid
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Actually create an instance of user and add them to database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # import login_user function
            login_user(user, remember=form.remember.data)
            # check if next page exists, get reurns none if next does not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Route user account home page, allowing user to update account right at home page

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
   # image_file = url_for('static', filename='profile-pics/' + current_user.image_file)
   form = UpdateAccountForm()
   if form.validate_on_submit():
       current_user.username = form.username.data
       current_user.email = form.email.data
       db.session.commit()
       flash('Your account has been updated!', 'success')
       return redirect(url_for('users.account'))
   elif request.method == 'GET':
       form.username.data = current_user.username
       form.email.data = current_user.email
   return render_template('account1.html', title='Account', form=form)


@users.route("/account/viewall", methods=['GET', 'POST'])
@login_required
def viewall():
    user_id = current_user.id
    page = request.args.get('page', 1, type=int)
    # Query donors of current user (filter_by) and order alphabetically
    # Number them into pages
    donors = Donor.query.filter_by(admin_id=user_id).order_by(Donor.name).paginate(page=page, per_page=3)
    # donors = Donor.query.filter(db.users.id == user_id)
    return render_template('viewall.html', title='Account', donors=donors)

@users.route("/account/update", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account1.html', title='Account', form=form)

# Link to request reset password

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    # create form
    form = RequestResetForm()
    # if form is submitted, get the user with that email
    # Send them an email to reset password
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Request', form=form)

# Route to reset password

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    user = User.verify_reset_token(token)
    # if function does not return an user, flash an error message
    # redirect to reset request again
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    # Else if user is valid, present form to reset password
    form = ResetPasswordForm()
    # Handle if form is submitted
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        # Actually create an instance of user and add them to database
        db.session.commit()
        flash('Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset password', form=form)
