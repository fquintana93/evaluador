import time
from datetime import date

from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app.main import bp
from app import db, documents
from app.main.forms import RegistrationForm
from app.models import User#, Empresa
from app.auth.email import send_password_set_email
import cmf
from cmf import lecturacmf, lecturacarpeta, consulta_sii, iniciaLecturaCmf,iniciaLecturaIvas, consulta_suspendidos
from functools import wraps
from flask import abort, current_app
from app.main.forms import EvaluadorForm, InicioForm, EmpresaForm,  Evaluador2Form, Evaluador3Form, GestionForm, administrarForm
from app.models import Consultas
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone
import controles, consultas
from controles import controlescarpeta, controlescmf
from consultas import ultimaconsulta, actualizaconsultaCMF, actualizaconsultaComportamiento, gestionUsuarios,actualizarUsuarios, consultarut
from consultas import addlabels, graficoconsulta, graficoSeguimiento, lecturasOK, ejecutivosEmpresa, graficoEjecutivos
import concurrent.futures
from Modelo import Modelo, infoEva


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


@bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, lastname=form.lastname.data, empresa=current_user.empresa, es_admin = False)
        db.session.add(user)
        current_user.unfollow(user)
        current_user.follow(user) 
        user.unfollow(current_user)
        user.follow(current_user)
        db.session.commit()
        flash(_('El usuario ha sido registrado!, revisar email y seguir las instrucciones para establecer la contrasena'))
        send_password_set_email(user)
        return redirect(url_for('main.empresa'))
    return render_template('register.html', title=_('Registro'), form=form)


@bp.route('/evaluador/documentos', methods=['GET', 'POST'])
@login_required
def evaluador():
    form = EvaluadorForm()
    if form.validate_on_submit():
        documento_cmf = form.cmf.data
        filename_documento_cmf = 'CMF-rut' + form.rut.data.replace('−', '') + 'fecha' + str(date.today()).replace('-', '') +'.pdf'
        documento_cmf.save(os.path.join(current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'], filename_documento_cmf))
        documento_ivas = form.carpeta.data
        filename_documento_ivas = 'IVAS-rut' + form.rut.data.replace('−', '') + 'fecha' + str(date.today()).replace('-', '') +'.pdf'
        documento_ivas.save(os.path.join(current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'], filename_documento_ivas))
        
        control_cmf = controlescmf(os.path.join(current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'], filename_documento_cmf))
        control_carpeta = controlescarpeta(os.path.join(current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'], filename_documento_ivas))
        
        rut_cliente_sii, resultado_fecha_sii = control_carpeta
        resultado_sello_cmf, resultado_fecha_cmf, rut_cliente_cmf = control_cmf
        
        carpeta_rut = (rut_cliente_sii  == form.rut.data.lower())
        carpeta_fecha = (resultado_fecha_sii == 'Fecha carpeta tributaria OK')
        control_carpeta_ok =  carpeta_rut and carpeta_fecha
        
        control_cmf_rut = (rut_cliente_cmf == form.rut.data.lower())
        control_cmf_sello = (resultado_sello_cmf == 'Sello certificado OK')
        control_cmf_fecha = (resultado_fecha_cmf == 'Fecha certificado OK')
        control_cmf_ok = (control_cmf_rut and control_cmf_sello and control_cmf_fecha)
        
        control_global = control_carpeta_ok and control_cmf_ok
        from random import choice ################# LUEGO BORRAR
        if form.validate_on_submit() and control_global:
            consulta = Consultas(rut=form.rut.data.lower(), cliente=form.name.data, 
                                  empresa_ejecutivo = current_user.empresa,
                                  user_id = current_user.id,
                                  score_final = choice([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]) ################ RANDOM
                                  )
            db.session.add(consulta)
            db.session.commit()
            base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
            datosultimaconsulta = ultimaconsulta(current_user.id)
            consulta_sii(datosultimaconsulta[1], datosultimaconsulta[0], base = 'C:\\Users\\user\\Desktop\\MTS\\app.db')
            consulta_suspendidos(datosultimaconsulta[1], datosultimaconsulta[0], base = 'C:\\Users\\user\\Desktop\\MTS\\app.db')
            archivocmf = (current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'] + datosultimaconsulta[2])
            archivoivas = (current_app._get_current_object().config['UPLOADED_DOCUMENTS_DEST'] + datosultimaconsulta[3])
            iniciaLecturaCmf(archivocmf, datosultimaconsulta[1], datosultimaconsulta[0],base)
            iniciaLecturaIvas(archivoivas, datosultimaconsulta[1], datosultimaconsulta[0],base)
            flash(_('Documentos validados!'))
            if form.bancarizado.data == 'Si':
                return redirect(url_for('main.evaluador2', username=current_user.username)) ## ver como poner historial
            else:
                return redirect(url_for('main.evaluador3', username=current_user.username))
        
        
        elif control_cmf_ok == False and control_carpeta_ok == True:
            if control_cmf_rut == False:
                flash(_('Documento CMF no valido, el rut no coincide!'))
                return redirect(url_for('main.evaluador'))
            elif control_cmf_sello == True and control_cmf_fecha == False:
                flash(_('Documento CMF no valido, favor verificar informacion! La fecha del documento supera la antiguedad permitida'))
                return redirect(url_for('main.evaluador'))
            elif control_cmf_sello == False and control_cmf_fecha == True:
                flash(_('Documento CMF no valido, favor verificar informacion! El sello del documento no coincide'))
                return redirect(url_for('main.evaluador'))
            else:
                flash(_('Documento CMF no valido, favor verificar informacion! El sello no coincide y la fecha del documento supera la antiguedad permitida'))
                return redirect(url_for('main.evaluador'))  
            flash(_('Documento CMF no valido, favor verificar informacion!'))
            return redirect(url_for('main.evaluador'))  
        
        
        elif (not control_carpeta_ok) == True and control_cmf_ok == True:
            if carpeta_rut == False and carpeta_fecha == True:
                flash(_('Documento Carpeta Tributaria no valido, favor verificar informacion! El rut no coincide'))
                return redirect(url_for('main.evaluador'))
            elif carpeta_rut == True and carpeta_fecha == False:
                flash(_('Documento Carpeta Tributaria no valido, favor verificar informacion! La fecha del documento supera la antiguedad permitida'))
                return redirect(url_for('main.evaluador'))
            else:
                flash(_('Documento Carpeta Tributaria no valido, favor verificar informacion! El rut no coincide y la fecha del documento supera la antiguedad permitida'))
                return redirect(url_for('main.evaluador'))  
        elif control_carpeta_ok == False and control_cmf_ok == False:
            flash(_('Documento CMF y Carpeta Tributaria no validos, favor verificar informacion! (Rut y Fechas de los documentos)'))
            return redirect(url_for('main.evaluador'))
    return render_template('evaluador.html', title=_('Evaluador'), form=form)


@bp.route('/evaluador/CMF', methods=['GET', 'POST'])
@login_required
def evaluador2():
    base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
    form = Evaluador2Form()
    datosultimaconsulta = ultimaconsulta(current_user.id)
    if form.validate_on_submit():
        actualizaconsultaCMF(base, datosultimaconsulta[1], datosultimaconsulta[0], form.solicitudes.data, form.aprobados.data, 
                               form.hipotecario.data, current_user.empresa)
        #time.sleep(15) ### LOADING
        return redirect(url_for('main.evaluador3')) ## ver como poner historial
    return render_template('evaluador2.html', title=_('Evaluador'), form=form)

@bp.route('/evaluador/Comportamiento', methods=['GET', 'POST'])
@login_required
def evaluador3():
    base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
    form = Evaluador3Form()
    datosultimaconsulta = ultimaconsulta(current_user.id)
    if form.validate_on_submit():
        actualizaconsultaComportamiento(base, datosultimaconsulta[1], datosultimaconsulta[0],                                 
        form.antiguedad.data, form.empleados.data, form.montolinea.data, form.adicional.data,
        form.cupoAprobado.data, form.plazoPago.data, form.frecuencia.data)
        flash(_('La evaluacion ha sido registrada!'))    
        termino_procesos = lecturasOK(datosultimaconsulta[1],base)
        time.sleep(15)
        while termino_procesos == False:
            termino_procesos = lecturasOK(datosultimaconsulta[1],base)
            if termino_procesos == True:
                break
            else:
                print('Aun no termina de actualizar')
                time.sleep(5)
        print('Actualizacion completada.')
        Modelo(datosultimaconsulta[1],base)
        url_for('main.evaluacion', consultaid=datosultimaconsulta[1])
        return redirect(url_for('main.evaluacion', consultaid=datosultimaconsulta[1])) ## ver como poner historial
    return render_template('evaluador3.html', title=_('Evaluador'), form=form)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def inicioblank():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    elif current_user.es_admin:
        return redirect(url_for('main.empresa'))
    else:
        return redirect(url_for('main.inicio'))
    
@bp.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    form = InicioForm()
    if form.validate_on_submit():
        if form.Evaluador.data:
            return redirect(url_for('main.evaluador'))
        elif form.Historial.data:
            return redirect(url_for('main.historial')) ## ver como poner historial
    elif request.method == 'GET':
        return render_template('inicio.html',title=_('Inicio'), form=form)  

@bp.route('/empresa', methods=['GET', 'POST'])
@login_required
@admin_required
def empresa():
    form = EmpresaForm()
    if form.validate_on_submit():
        if form.Evaluador.data:
            return redirect(url_for('main.evaluador'))
        elif form.Historial.data:
            return redirect(url_for('main.historial')) ## ver como poner historial
        elif form.Seguimiento.data:
            return redirect(url_for('main.seguimiento'))
        elif form.Gestion.data:
            return redirect(url_for('main.gestion'))
    elif request.method == 'GET':
        return render_template('empresa.html',title=_('Inicio'), form=form)  

@bp.route('/historial')
@login_required
def historial():
    #user = User.query.filter_by(username=current_user.username).first_or_404()
    page = request.args.get('page', 1, type=int)
    consultas = current_user.followed_consultas().paginate(
        page, current_app._get_current_object().config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.historial', page=consultas.next_num) \
        if consultas.has_next else None
    prev_url = url_for('main.historial', page=consultas.prev_num) \
        if consultas.has_prev else None
    #form = EmptyForm()
    return render_template('historial.html',title=_('Historial Consultas'), consultas=consultas.items,
                            next_url=next_url, prev_url=prev_url)#, form=form)


@bp.route('/seguimiento')
@login_required
def seguimiento():
    #user = User.query.filter_by(username=current_user.username).first_or_404()
    base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
    ejecutivos = ejecutivosEmpresa(current_user.empresa, base)
    ruta_grafico = "C:\\Users\\user\\Desktop\\MTS\\app\\static\\graficos\\"
    graficoEjecutivos(ejecutivos, base, ruta_grafico)
    page = request.args.get('page', 1, type=int)
    consultas = Consultas
    user = current_user.followed_users().paginate(
        page, current_app._get_current_object().config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.seguimiento', page=user.next_num) \
        if user.has_next else None
    prev_url = url_for('main.seguimiento', page=user.prev_num) \
        if user.has_prev else None
    #form = EmptyForm()
    return render_template('seguimiento.html',title=_('Seguimiento'), user=user.items, consultas = consultas,
                            next_url=next_url, prev_url=prev_url)#, form=form)

from flask import g
from app.main.forms import SearchForm

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        #current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.historial'))
    page = request.args.get('page', 1, type=int)
    consultas, total = Consultas.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE']) ###
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), consultas=consultas, rut = g.search_form.q.data,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/Consulta-<consultaid>', methods=['GET', 'POST'])
@login_required
def evaluacion(consultaid):
    base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
    consulta_rut = consultarut(consultaid, base)[0]
    ruta_grafico = "C:\\Users\\user\\Desktop\\MTS\\app\\static\\graficos\\"
    graficoSeguimiento(base, consultaid, consulta_rut, current_user.empresa, ruta_grafico)
    dir_imagen = "../static/graficos/"+str(consulta_rut)+".png"
    datos = infoEva(consultaid, base)
    return render_template('evaluacion.html', title=_('Resumen Evaluacion'), consultaid = consultaid, dir_imagen=dir_imagen, datos = datos)


@bp.route('/gestion', methods=['GET', 'POST'])
@login_required
@admin_required
def gestion():
    form = GestionForm()
    if form.validate_on_submit():
        if form.Gestionar.data:
            return redirect(url_for('main.ejecutivos'))
        elif form.Crear.data:
            return redirect(url_for('main.register')) ## ver como poner historial
    elif request.method == 'GET':
        return render_template('gestion.html',title=_('Gestion'), form=form)
    
    
    



@bp.route('/ejecutivos', methods=['GET', 'POST'])
@login_required
@admin_required
def ejecutivos():
    form = administrarForm()
    base = 'C:\\Users\\user\\Desktop\\MTS\\app.db'
    form.Ejecutivo.choices = []        
    for row in gestionUsuarios(base, current_user.id, current_user.empresa):
        _id = str(row[0])
        ejecutivo = str(row[1])
        form.Ejecutivo.choices += [(_id, ejecutivo)]
    if form.validate_on_submit():
        actualizarUsuarios(base, form.Ejecutivo.data, current_user.empresa, form.Accion.data)
        flash(_('Usuario actualizado!'))        
        return redirect(url_for('main.empresa')) ## ver como poner historial
    return render_template('ejecutivos.html', title=_('Administrar'), form=form)


    