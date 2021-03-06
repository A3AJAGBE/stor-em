from management import login_manager
from management.models import *
from management.forms import *
from management.emails import *
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from phonenumbers import NumberParseException, is_possible_number, parse, is_valid_number


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/<name>')
@login_required
def profile(name):
    return render_template('profile.html')


"""Merchants Related Functions"""


@app.route('/merchant', methods=['GET', 'POST'])
@login_required
def merchant():
    merchants = Merchants.query.filter_by(user_id=current_user.id)
    form = MerchantForm()
    if form.validate_on_submit():
        merchant_name = form.merchant_name.data.title()
        contact_name = form.contact_name.data.title()
        email = form.email.data
        phone_number = form.phone_number.data

        try:
            number = parse(phone_number)
            if not is_possible_number(number):
                flash("Check the phone number again", "danger")
                return redirect(request.referrer)
            elif not is_valid_number(number):
                flash("Invalid phone number", "danger")
                return redirect(request.referrer)
        except NumberParseException:
            flash("Add the country code to phone number, eg. +353", "danger")
            return redirect(request.referrer)
        else:
            # check that merchant does not exist
            if Merchants.query.filter_by(merchant_name=merchant_name).first():
                flash("That merchant already exist in the database", "danger")
                return redirect(request.referrer)
            elif Merchants.query.filter_by(phone_number=phone_number).first():
                flash("That number exists in the database, use another", "danger")
                return redirect(request.referrer)
            else:
                new_merchant = Merchants(
                    merchant_name=merchant_name,
                    contact_name=contact_name,
                    email=email,
                    phone_number=phone_number,
                    user_id=current_user.id
                )
                db.session.add(new_merchant)
                db.session.commit()
                flash(f'"{merchant_name}" merchant info added successfully', "success")
                return redirect(request.referrer)
    return render_template('merchant.html', form=form, merchants=merchants)


@app.route('/edit merchant/<int:merchant_id>', methods=['GET', 'POST'])
@login_required
def edit_merch(merchant_id):
    edit_merchant = Merchants.query.get(merchant_id)
    editMerchant = MerchantForm(
        merchant_name=edit_merchant.merchant_name,
        contact_name=edit_merchant.contact_name,
        email=edit_merchant.email,
        phone_number=edit_merchant.phone_number,
    )
    if editMerchant.validate_on_submit():

        try:
            number = parse(editMerchant.phone_number.data)
            if not is_possible_number(number):
                flash("Check the phone number again", "danger")
                return redirect(request.referrer)
            elif not is_valid_number(number):
                flash("Invalid phone number", "danger")
                return redirect(request.referrer)
        except NumberParseException:
            flash("Add the country code to phone number, eg. +353", "danger")
            return redirect(request.referrer)
        else:
            edit_merchant.merchant_name = editMerchant.merchant_name.data.title()
            edit_merchant.contact_name = editMerchant.contact_name.data.title()
            edit_merchant.email = editMerchant.email.data
            edit_merchant.phone_number = editMerchant.phone_number.data
            db.session.commit()
            flash(f'"{edit_merchant.merchant_name}" merchant information updated successfully', "success")
            return redirect(url_for('merchant'))
    return render_template('edit_merchant.html', form=editMerchant)


@app.route("/delete merchant/<int:merchant_id>")
def delete_merch(merchant_id):
    delete_med = Merchants.query.get(merchant_id)
    db.session.delete(delete_med)
    db.session.commit()
    flash("Merchant deleted successfully", "success")
    return redirect(request.referrer)


"""Customers Related Functions"""


@app.route('/customer', methods=['GET', 'POST'])
@login_required
def customer():
    customers = Customers.query.filter_by(user_id=current_user.id)
    form = CustomerForm()
    if form.validate_on_submit():
        customer_name = form.customer_name.data.title()
        email = form.email.data
        phone_number = form.phone_number.data

        try:
            number = parse(phone_number)
            if not is_possible_number(number):
                flash("Check the phone number again", "danger")
                return redirect(request.referrer)
            elif not is_valid_number(number):
                flash("Invalid phone number", "danger")
                return redirect(request.referrer)
        except NumberParseException:
            flash("Add the country code to phone number, eg. +353", "danger")
            return redirect(request.referrer)
        else:
            # check that customer does not exist
            if Customers.query.filter_by(customer_name=customer_name).first():
                flash("That customer already exist in the database", "danger")
                return redirect(request.referrer)
            elif Customers.query.filter_by(phone_number=phone_number).first():
                flash("That number exists in the database, use another", "danger")
                return redirect(request.referrer)
            else:
                new_customer = Customers(
                    customer_name=customer_name,
                    email=email,
                    phone_number=phone_number,
                    user_id=current_user.id
                )
                db.session.add(new_customer)
                db.session.commit()
                flash(f'"{customer_name}" customer info added successfully', "success")
                return redirect(request.referrer)
    return render_template('customer.html', form=form, customers=customers)


@app.route('/edit customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    edit_cust = Customers.query.get(customer_id)
    form = CustomerForm(
        customer_name=edit_cust.customer_name,
        email=edit_cust.email,
        phone_number=edit_cust.phone_number,
    )
    if form.validate_on_submit():

        try:
            number = parse(form.phone_number.data)
            if not is_possible_number(number):
                flash("Check the phone number again", "danger")
                return redirect(request.referrer)
            elif not is_valid_number(number):
                flash("Invalid phone number", "danger")
                return redirect(request.referrer)
        except NumberParseException:
            flash("Add the country code to phone number, eg. +353", "danger")
            return redirect(request.referrer)
        else:
            edit_cust.customer_name = form.customer_name.data.title()
            edit_cust.email = form.email.data
            edit_cust.phone_number = form.phone_number.data
            db.session.commit()
            flash(f'"{edit_cust.customer_name}" customer information updated successfully', "success")
            return redirect(url_for('customer'))
    return render_template('edit_customer.html', form=form)


@app.route("/delete customer/<int:customer_id>")
def delete_customer(customer_id):
    delete_cust = Customers.query.get(customer_id)
    db.session.delete(delete_cust)
    db.session.commit()
    flash("Customer deleted successfully", "success")
    return redirect(request.referrer)


"""Auth Related Functions"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "warning")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        business_name = form.business_name.data.title()
        email = form.email.data
        password = form.password.data

        # Check if the email is unique
        if Users.query.filter_by(email=email).first():
            flash("That email already exists, try another", "danger")
            return redirect(request.referrer)
        elif Users.query.filter_by(business_name=business_name).first():
            flash("That business name exists, use another", "danger")
            return redirect(request.referrer)
        else:
            encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            new_user = Users(
                business_name=business_name,
                email=email,
                password=encrypt_password,
            )
            db.session.add(new_user)
            db.session.commit()

            token = generate_token(email)
            user_email = email
            confirm_email_url = url_for('confirm_email', token=token, _external=True)
            text_body = render_template('emails/email_confirmation.txt', confirm_email_url=confirm_email_url,
                                        name=business_name)
            html_body = render_template('emails/email_confirmation.html', confirm_email_url=confirm_email_url,
                                        name=business_name)
            email_confirmation(user_email, text_body, html_body)

            flash(f'Registration successful "{business_name}", check for email confirmation in your inbox',
                  "success")
            return redirect(url_for('index'))
    return render_template('auth/register.html', form=form)


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash('That confirmation link is Invalid or has expired', 'danger')
        return redirect(url_for('email_unconfirmed'))
    else:
        user = Users.query.filter_by(email=email).first_or_404()

        if user.email_confirmed:
            flash(f'"{user.business_name}", you have confirmed that email.', 'warning')
            return redirect(url_for('login'))
        else:
            user.email_confirmed = True
            user.email_confirmed_at = datetime.utcnow()
            user.is_active = True
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f'Email confirmation successful {user.business_name}, you are now logged in.', 'success')
            return redirect(url_for('profile', name=user.business_name))


@app.route('/unconfirmed', methods=['GET', 'POST'])
def email_unconfirmed():
    if current_user.is_authenticated and current_user.email_confirmed:
        flash("You are unable to view that page because you are verified user.", "warning")
        return redirect(url_for('index'))
    form = NewEmailConfirmationRequestForm()
    if form.validate_on_submit():
        email = form.email.data

        user = Users.query.filter_by(email=email).first()

        if not user:
            flash('That is not a registered email address.', 'danger')
            return redirect(request.referrer)
        elif user.email_confirmed:
            flash('That email address has already been confirmed.', 'danger')
            return redirect(request.referrer)
        else:
            token = generate_token(email)
            user_email = email
            confirm_email_url = url_for('confirm_email', token=token, _external=True)
            text_body = render_template('emails/resend_confirmation.txt', confirm_email_url=confirm_email_url,
                                        name=user.business_name)
            html_body = render_template('emails/resend_confirmation.html', confirm_email_url=confirm_email_url,
                                        first_name=user.business_name)
            email_confirmation_resend(user_email, text_body, html_body)
            flash(f'A new email confirmation has been sent "{user.business_name}".', 'success')
            return redirect(request.referrer)
    return render_template('auth/unconfirmed_email.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "warning")
        return redirect(url_for('profile', name=current_user.business_name))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Find the user by email
        user = Users.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email address, try again.", "danger")
            return redirect(request.referrer)
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, try again.', "danger")
            return redirect(request.referrer)
        else:
            if user.email_confirmed:
                login_user(user)
                flash('You are logged in successfully', "success")
                return redirect(url_for('profile', name=current_user.business_name))
            else:
                flash('You are yet to confirm your email address.', "danger")
                return redirect(url_for('email_unconfirmed'))
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully', "success")
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "warning")
        return redirect(url_for('profile', name=current_user.business_name))
    if form.validate_on_submit():
        email = form.email.data

        user = Users.query.filter_by(email=email).first()

        if not user:
            flash('That is not a registered email address.', 'danger')
            return redirect(request.referrer)
        elif not user.email_confirmed:
            flash('That email address is not confirmed.', 'danger')
            return redirect(request.referrer)
        else:
            token = generate_token(email)
            user_email = email
            reset_password_url = url_for('reset_password', token=token, _external=True)
            text_body = render_template('emails/password_reset.txt', reset_password_url=reset_password_url,
                                        name=user.business_name)
            html_body = render_template('emails/password_reset.html', reset_password_url=reset_password_url,
                                        name=user.business_name)
            email_password_reset(user_email, text_body, html_body)
            flash(f'An email has been sent "{user.business_name}", check it for further instructions.', 'success')
            return redirect(request.referrer)
    return render_template('auth/reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash('The password reset link is Invalid or has expired, request for another', 'danger')
        return redirect(url_for('reset_password_request'))
    else:
        user = Users.query.filter_by(email=email).first()

        if not user.email_confirmed:
            flash(f'"{user.business_name}", you have not confirmed that email. Kindly, confirm before proceeding.',
                  'warning')
            return redirect(url_for('email_unconfirmed'))

        if form.validate_on_submit():
            password = form.password.data
            encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            user.password = encrypt_password
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f'Password reset successful "{user.business_name}", you are now logged in.', 'success')
            return redirect(url_for('profile', name=user.business_name))
    return render_template('auth/password_reset.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data

        encrypt_new_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)

        user = Users.query.filter_by(email=current_user.email).first()

        if not check_password_hash(user.password, old_password):
            flash('Old password is incorrect, try again.', 'danger')
            return redirect(request.referrer)
        else:
            user.password = encrypt_new_password
            db.session.commit()
            user_email = user.email
            reset_password_request_url = url_for('reset_password_request', _external=True)
            text_body = render_template('emails/password_changed.txt',
                                        reset_password_request_url=reset_password_request_url,
                                        name=user.business_name)
            html_body = render_template('emails/password_changed.html',
                                        reset_password_request_url=reset_password_request_url,
                                        name=user.business_name)
            email_password_change(user_email, text_body, html_body)
            flash(f'Password successfully changed {user.business_name}.', 'success')
            return redirect(url_for('profile', name=user.business_name))
    return render_template('auth/change_password.html', form=form)
