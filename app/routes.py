from flask import render_template, url_for, flash, redirect, request, abort
from app.forms import RegistrationForm, LoginForm, InsertForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Donor
from flask_mail import Message

# Link to home page

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# About page

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Register page

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # import login_user function
            login_user(user, remember=form.remember.data)
            # check if next page exists, get reurns none if next does not exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route user account home page, allowing user to update account right at home page

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
   # image_file = url_for('static', filename='profile-pics/' + current_user.image_file)
   form = UpdateAccountForm()
   if form.validate_on_submit():
       current_user.username = form.username.data
       current_user.email = form.email.data
       db.session.commit()
       flash('Your account has been updated!', 'success')
       return redirect(url_for('account'))
   elif request.method == 'GET':
       form.username.data = current_user.username
       form.email.data = current_user.email
   return render_template('account1.html', title='Account', form=form)


@app.route("/account/viewall", methods=['GET', 'POST'])
@login_required
def viewall():
    user_id = current_user.id
    page = request.args.get('page', 1, type=int)
    # Query donors of current user (filter_by) and order alphabetically
    # Number them into pages
    donors = Donor.query.filter_by(admin_id=user_id).order_by(Donor.name).paginate(page=page, per_page=3)
    # donors = Donor.query.filter(db.users.id == user_id)
    return render_template('viewall.html', title='Account', donors=donors)

@app.route("/account/update", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account1.html', title='Account', form=form)


# Since we posting data back into this route, the route
# needs to have get and post method
@app.route("/account/add",  methods=['GET', 'POST'])
@login_required
def insert_donor():
    form = InsertForm()
    # If form is valid, post it and return the updated table
    # on account page
    if form.validate_on_submit():
        # add donor to database
        donor = Donor(name=form.name.data, contact_email=form.contact_email.data,
                      donation_amount=form.donation_amount.data, donate_event=form.donate_event.data, admin=current_user)
        db.session.add(donor)
        db.session.commit()
        flash(' A new person data was added', 'success')
        return redirect(url_for('account'))
    return render_template('insert_donor.html', form=form, title=' Add Donor', legend='Add Donor')


# function to display a donor's information

@app.route("/account/<int:donor_id>")
def return_donor(donor_id):
    # get_or_404 is a function returning donor's id if exists, else 404 error
    # Consider show all donations the donor made
    # page = request.args.get('page', 1, type=int)
    # donor = Donor.query.filter_by(id=donor_id).first_or_404()
    # [donation_history]= Donation_history.query.filter_by(donor=donor).order_by(Donor.amount.desc()).paginate(page=page, per_page=5)
    donor = Donor.query.get_or_404(donor_id)
    return render_template('donor.html', title=donor.name, donor=donor)


# function to edit the donor's information
# Design idea: Admin needs to choose a specific donor to edit info

@app.route("/account/<int:donor_id>/update",  methods=['GET', 'POST'])
@login_required
def update_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    # if admin is not current user, give error
    if donor.admin != current_user:
        abort(403)
    form = InsertForm()
    # If form is valid, change only contact email or donation amount
    # if method is get, we want to the form to be filled ahead
    if form.validate_on_submit():
        donor.contact_email = form.contact_email.data
        donor.donation_amount = form.donation_amount.data
        donor.donate_event = form.donate_event.data
        db.session.commit()
        flash('Information has been updated!', 'success')
        return redirect(url_for('return_donor', donor_id=donor.id))
    elif request.method == 'GET':
        # Get data for name and contact email only
        form.name.data = donor.name
        form.contact_email.data = donor.contact_email
    return render_template('insert_donor.html', title='Update Donor',
                           form=form, legend='Update Donor')


@app.route("/account/<int:donor_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    # verify that user is current user
    if donor.admin != current_user:
        flash('Wrong admin', 'success')
        abort(403)
    db.session.delete(donor)
    db.session.commit()
    flash('One donor information was deleted!', 'success')
    return redirect(url_for('account'))
    return render_template('account1.html', title="Account")


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    
    If you did not make this request, please ignore this email
    '''
    mail.send(msg)

# Link to request reset password

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    # create form
    form = RequestResetForm()
    # if form is submitted, get the user with that email
    # Send them an email to reset password
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Request', form=form)

# Route to reset password

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    user = User.verify_reset_token(token)
    # if function does not return an user, flash an error message
    # redirect to reset request again
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
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
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset password', form=form)
