from flask import (render_template, Blueprint, url_for, flash, redirect, request, abort)
from flask_login import current_user, login_required
from app import db
from app.models import Donor
from app.donors.forms import InsertForm

donors = Blueprint('donors', __name__)

# Since we posting data back into this route, the route
# needs to have get and post method
@donors.route("/account/add",  methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    return render_template('insert_donor.html', form=form, title=' Add Donor', legend='Add Donor')


# function to display a donor's information

@donors.route("/account/<int:donor_id>")
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

@donors.route("/account/<int:donor_id>/update",  methods=['GET', 'POST'])
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
        return redirect(url_for('donors.return_donor', donor_id=donor.id))
    elif request.method == 'GET':
        # Get data for name and contact email only
        form.name.data = donor.name
        form.contact_email.data = donor.contact_email
    return render_template('insert_donor.html', title='Update Donor',
                           form=form, legend='Update Donor')


@donors.route("/account/<int:donor_id>/delete", methods=['GET', 'POST'])
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
    return redirect(url_for('users.account'))

