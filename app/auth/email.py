from flask import render_template
from app import mail

from flask import current_app
from flask_babel import _
from app.email import send_email


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[RDFSPA] Reset Your Password'),
               sender=current_app._get_current_object().config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_password_set_email(user):
    token = user.get_reset_password_token()
    send_email(_('[RDFSPA] Establecer contrasena'),
               sender=current_app._get_current_object().config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/set_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/set_password.html',
                                         user=user, token=token))



