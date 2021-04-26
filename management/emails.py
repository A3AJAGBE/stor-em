from management import mail, app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from threading import Thread


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_SALT'])


def confirm_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_SALT'],
        max_age=expiration
    )
    return email


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    msg = Message(
        subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=recipients,
        body=text_body,
        html=html_body,
    )
    Thread(target=send_async_email, args=(app, msg)).start()


def email_confirmation(user_email, text_body, html_body):
    send_email("[A3AJAGBE STOR'EM] Email Confirmation",
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)


def email_confirmation_resend(user_email, text_body, html_body):
    send_email("[A3AJAGBE STOR'EM] New Email Confirmation",
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)


def email_password_reset(user_email, text_body, html_body):
    send_email("[A3AJAGBE STOR'EM] Reset Password",
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)


def email_password_change(user_email, text_body, html_body):
    send_email("[A3AJAGBE STOR'EM] Password Change",
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)
