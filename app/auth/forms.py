from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l



style_relleno={'style': 'color:black;'}
style_boton={'style': 'width: 100%; margin: 5px auto; font-weight:bold; font-size: 20px'}

class LoginForm(FlaskForm):
    username = StringField(_l('Usuario'), validators=[DataRequired()], render_kw=style_relleno)
    password = PasswordField(_l('Contraseña'), validators=[DataRequired()], render_kw=style_relleno)
    remember_me = BooleanField(_l('Recuerdame'))
    submit = SubmitField(_l('Ingresar'), render_kw=style_boton)


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw=style_relleno)
    submit = SubmitField(_l('Restablecer contraseña'), render_kw=style_boton)


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Contraseña'), validators=[DataRequired()], render_kw=style_relleno)
    password2 = PasswordField(
        _l('Repetir Contraseña'), validators=[DataRequired(),
                                           EqualTo('password')], render_kw=style_relleno)
    submit = SubmitField(_l('Restablecer Contraseña'), render_kw=style_boton)








