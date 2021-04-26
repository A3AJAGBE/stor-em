from datetime import datetime

from management import app, login_manager
from management.models import *
from management.forms import *
from management.emails import *
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


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
            return redirect(request.referrer)
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
            flash(f'"{user.business_name}", you have confirmed that email. Kindly login.', 'warning')
            return redirect(url_for('login'))
        else:
            user.email_confirmed = True
            user.email_confirmed_at = datetime.utcnow()
            user.is_active = True
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f'Email confirmation successful {user.business_name}, you are now logged in.', 'success')
            return redirect(url_for('index'))


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
        elif user.email_confirmed:
            flash('That email address has already been confirmed.', 'danger')
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
        return redirect(url_for('index'))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Find the user by email
        user = Users.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email address, try again.", "danger")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, try again.', "danger")
        else:
            if user.email_confirmed:
                login_user(user)
                flash('You are logged in successfully', "success")
                return redirect(url_for('index'))
            else:
                flash('You are yet to confirm your email address.', "danger")
                return redirect(url_for('email_unconfirmed'))
    return render_template('auth/login.html', form=form)


