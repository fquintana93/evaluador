from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app.auth import bp
from app import db
from app.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User#, Empresa
from app.auth.email import send_password_reset_email
from functools import wraps
from flask import abort



def superuser_required(f):
    @wraps(f)
    def superuser_function(*args, **kws):
        es_superuser = getattr(current_user, 'es_superuser', False)
        if not es_superuser:
            abort(401)
        return f(*args, **kws)
    return superuser_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        es_admin = getattr(current_user, 'es_admin', False)
        if not es_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/admin')
@login_required
@superuser_required
def admin():
    return redirect(url_for('admin'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.es_admin==False:
        return redirect(url_for('main.inicio'))
    elif current_user.is_authenticated and  current_user.es_admin==True:
        return redirect(url_for('main.empresa'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or user.estado != "Activo":
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if (not next_page or url_parse(next_page).netloc != '') and current_user.es_admin==False:
            next_page = url_for('main.inicio')
        elif (not next_page or url_parse(next_page).netloc != '') and current_user.es_admin ==True:
            next_page = url_for('main.empresa')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Ingreso'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated and current_user.es_admin==False:
        return redirect(url_for('main.inicio'))
    elif current_user.is_authenticated and  current_user.es_admin==True:
        return redirect(url_for('main.empresa'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Restablecer Contraseña'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    logout_user()
    if current_user.is_authenticated and current_user.es_admin==False:
        return redirect(url_for('main.inicio'))
    elif current_user.is_authenticated and  current_user.es_admin==True:
        return redirect(url_for('main.empresa'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.inicio'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
