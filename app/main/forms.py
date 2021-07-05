from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User
from flask import request

style_boton={'style': 'width: 100%; margin: 5px auto; font-weight:bold; font-size: 20px; height:60px; grid-column: 1 / 3;'}
style_boton_click={"onclick": "document.getElementById('formulario-final').style.opacity=0.3 , document.getElementById('loading_oculto').style.visibility='visible'", 'style': 'width: 100%; margin: 5px auto; font-weight:bold; font-size: 20px; height:60px; grid-column: 1 / 3;'}
style_relleno={'style': 'color:black; background-color: white;'}
style_relleno_numero={"onkeyup": "this.value=addcommas(this.value);", 'style': 'color:black; background-color: white;'}





class RegistrationForm(FlaskForm):
    name =StringField(_l('Nombre'), validators=[DataRequired()], render_kw=style_relleno)
    lastname = StringField(_l('Apellido'), validators=[DataRequired()], render_kw=style_relleno)
    username = StringField(_l('Usuario'), validators=[DataRequired()], render_kw=style_relleno)
    email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw=style_relleno)
    submit = SubmitField(_l('Registrar'), render_kw=style_boton)

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Por favor usa un Usuario diferente.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Por favor usa un Email diferente.'))


#### PRUEBA


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, EqualTo, Length, Email
from werkzeug.utils import secure_filename

class InicioForm(FlaskForm):
    Evaluador = SubmitField('Evaluar Cliente', render_kw=style_boton)
    Historial = SubmitField('Historial de Consultas', render_kw=style_boton)

class EmpresaForm(FlaskForm):
    Evaluador = SubmitField('Evaluar Cliente', render_kw=style_boton)
    Historial = SubmitField('Historial de Consultas', render_kw=style_boton)
    Seguimiento = SubmitField('Seguimiento Empresa', render_kw=style_boton)
    Gestion = SubmitField('Gestionar Usuarios', render_kw=style_boton)

class EvaluadorForm(FlaskForm):
    # StringField <input type='text' name='name' required>
    # PasswordField <input type='password' name='password' required>
    rut = StringField(
                 label = "Rut a evaluar",
                 # Verificación: el nombre de usuario no puede estar vacío
        validators=[DataRequired() ], render_kw=style_relleno
    )
    name = StringField(
                 label = "Cliente",
                 # Verificación: el nombre de usuario no puede estar vacío
        validators=[DataRequired() ], render_kw=style_relleno
    )
    
        
    bancarizado = SelectField(
                        label = "El cliente se encuentra bancarizado?",
            #coerce=int,
                        choices = [("Si", "Si"), ("No", "No")],
                        render_kw=style_relleno
            
    )
    
    cmf = FileField(
                 label = "Deudas CMF",
                 # Verificación: el nombre de usuario no puede estar vacío
        validators=[DataRequired(), FileAllowed (['pdf'], 'El archivo debe ser PDF!')]
    )
    
    carpeta = FileField(
                 label = "Carpeta Tributaria",
                 # Verificación: el nombre de usuario no puede estar vacío
        validators=[DataRequired(), FileAllowed (['pdf'], 'El archivo debe ser PDF!')]
    )
    
    
    enviar = SubmitField (label = "Evaluar", render_kw = style_boton)
        

class Evaluador2Form(FlaskForm):

    solicitudes = SelectField(
                         label = "Cuantas veces en el ultimo año ha pedido aumento de cupo de la linea de credito en los bancos?",
            #coerce=int,
                         choices = [("0", "0"), ("1", "1")
                                    , ("2", "2") , ("3", "3") , 
                                    ("Mas de 3", "Mas de 3") ],
                         render_kw=style_relleno
    )
    aprobados = SelectField(
                         label = "Cuantas veces los bancos le han otorgado el aumento de cupo solicitado?",
            #coerce=int,
                         choices = [("0", "0"), ("1", "1")
                                    , ("2", "2") , ("3", "3") , 
                                    ("Mas de 3", "Mas de 3") ],
                         render_kw=style_relleno
    )

    hipotecario = StringField(
                         label = "Tienes hipotecario y por que monto? (aproximado)",
                         validators=[DataRequired() ],  render_kw=style_relleno_numero
    )
    
    enviar = SubmitField (label = "Evaluar", id="mybutton",render_kw = style_boton)


class Evaluador3Form(FlaskForm):

    antiguedad = SelectField(
                         label = "Cual es la antiguedad del cliente con la empresa?",
                         choices = [("Cliente nuevo", "Cliente nuevo"), ("Entre 1 y 2 años", "Entre 1 y 2 años")
                                    , ("Entre 2 y 4 años", "Entre 2 y 4 años") , ("Mas de 4 años", "Mas de 4 años")],
                        render_kw=style_relleno
            
    )
    
    empleados = StringField(
                         label = "Cuantos empleados tiene? (aproximado)",
                         validators=[DataRequired() ],  render_kw=style_relleno
    )
    
    montolinea = StringField(
                         label = "Cual es el monto de la linea de credito aprobado actualmente? (con la empresa)",
                      validators=[DataRequired() ],  render_kw=style_relleno_numero
    )
            
    
    
    adicional = StringField(
                         label = "Que monto adicional de linea de credito necesita? (con la empresa)",
                         validators=[DataRequired() ], render_kw=style_relleno_numero
    )
    
    cupoAprobado = SelectField(
                         label = "En el ultimo año el cliente ha:",
                         choices = [("Aumentado su cupo", "Aumentado su cupo"), ("Mantenido su cupo", "Mantenido su cupo")
                                    , ("Disminuido su cupo", "Disminuido su cupo")],
                        render_kw=style_relleno
            
    )
    plazoPago = SelectField(
                 label = "Al momento de pagar el cliente presenta:",
                 choices = [("Pago al dia", "Pago al dia"), ("Atrasos normales (hasta 30 dias)", "Atrasos normales (hasta 30 dias)")
                                    , ("Atrasos excesivos (entre 30 y 90 dias)", "Atrasos excesivos (entre 30 y 90 dias)"), ("Es incobrable (mas de 90 dias)", "Es incobrable (mas de 90 dias)")],
                        render_kw=style_relleno
            
    )
    
    frecuencia = SelectField(
                 label = "El cliente presenta compras:",
                 choices = [("Mensuales", "Mensuales"), ("Cada 2 a 3 meses", "Cada 2 a 3 meses")
                                    , ("Cada 4 a 6 meses", "Cada 4 a 6 meses"), ("Cada 6 a 12 meses", "Cada 6 a 12 meses")],
                        render_kw=style_relleno
            
    )

    enviar = SubmitField (label = "Evaluar", id="mybutton",render_kw = style_boton_click)


class SearchForm(FlaskForm):
    q = StringField(_l('Consultar Rut sin puntos y con guion'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class GestionForm(FlaskForm):
    Gestionar = SubmitField('Gestionar Ejecutivos', render_kw=style_boton)
    Crear = SubmitField('Crear nueva cuenta', render_kw=style_boton)

class administrarForm(FlaskForm):
    Ejecutivo = SelectField('Seleccionar Ejecutivo', choices=[], render_kw=style_relleno)
    Accion  = SelectField(
                 label = "Accion:",
                 choices = [("Hacer Administrador", "Hacer Administrador"), ("Quitar permisos de administrador", "Quitar permisos de administrador")
                                    , ("Dar cuenta de baja", "Dar cuenta de baja")],
                        render_kw=style_relleno)
    enviar = SubmitField (label = "Actualizar usuario", id="mybutton",render_kw = style_boton)

