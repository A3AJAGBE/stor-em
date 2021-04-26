from management import app, login_manager
from management.models import *
from management.forms import *
from management.emails import *
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        pass
    return render_template('auth/login.html', form=form)


