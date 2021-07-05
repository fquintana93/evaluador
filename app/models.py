from datetime import datetime
import time
from datetime import date
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(-cls.id), total #####
            #db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    consultas = db.relationship('Consultas', backref='ejecutivo', lazy='dynamic') ## consultas
    es_admin = db.Column(db.Boolean)
    empresa = db.Column(db.String(120))
    estado = db.Column(db.String(64))
    followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))

    def __repr__(self):
        return 'Ejecutivo: {} {} '.format(self.name, self.lastname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')#.decode('utf-8')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_consultas(self):
        todas = Consultas.query.filter_by(empresa_ejecutivo=self.empresa)
        # followed = Consultas.query.join(
        #     followers, (followers.c.followed_id == Consultas.user_id)).filter(
        #         followers.c.follower_id == self.id)
        # own = Consultas.query.filter_by(user_id=self.id)
        return todas.order_by(Consultas.id.desc())
        #return followed.union(own).order_by(Consultas.fecha_ev.desc())
    
    def followed_users(self):
        todas = User.query.filter_by(empresa=self.empresa)
        return todas.order_by(User.username.desc())

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
### PRUEBA


class Consultas(SearchableMixin, db.Model):
    __searchable__ = ['rut']
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), index=True)
    cliente = db.Column(db.String(20), index=True)
    fecha_ev = db.Column(db.DateTime, index=True, default=datetime.now().replace(microsecond=0))
    monto_linea = db.Column(db.String(50))
    adicional = db.Column(db.String(50))
    solicitudes = db.Column(db.String(10))
    aprobados = db.Column(db.String(10))
    empleados = db.Column(db.String(30))
    hipotecario = db.Column(db.String(50))
    cmf_deuda = db.Column(db.Integer)
    cmf_cupo = db.Column(db.Integer)
    cmf_mora = db.Column(db.Integer)
    cmf_instituciones = db.Column(db.Integer)
    cmf_cupo_ctge = db.Column(db.Integer)
    iva_fecha_ini_act_str = db.Column(db.String(50))
    iva_total_ventas_ano_1 = db.Column(db.Integer)
    iva_meses_venta_ano_1 = db.Column(db.Integer)
    iva_total_imp_renta_trab_ano_1 = db.Column(db.Integer)
    iva_meses_imp_renta_trab_ano_1 = db.Column(db.Integer)
    iva_total_compras_ano_1 = db.Column(db.Integer)
    iva_meses_compras_ano_1 = db.Column(db.Integer)
    iva_meses_sin_declaracion_ano_1 = db.Column(db.Integer)
    iva_total_ventas_ano_2 = db.Column(db.Integer)
    iva_meses_venta_ano_2 = db.Column(db.Integer)
    iva_total_imp_renta_trab_ano_2 = db.Column(db.Integer)
    iva_meses_imp_renta_trab_ano_2 = db.Column(db.Integer)
    iva_total_compras_ano_2 = db.Column(db.Integer)
    iva_meses_compras_ano_2 = db.Column(db.Integer)
    iva_meses_sin_declaracion_ano_2 = db.Column(db.Integer)
    sii_empleados = db.Column(db.Integer)
    sii_tramo_ventas = db.Column(db.String(50))
    sii_inicio_act = db.Column(db.String(50))
    sii_rubro = db.Column(db.String(200))
    sii_comuna = db.Column(db.String(50))
    trabajadoresSuspendidos = db.Column(db.Integer)
    antiguedad_cli = db.Column(db.String(100))
    cupoAprobado =  db.Column(db.String(50))
    plazoPago =  db.Column(db.String(50))
    frecuencia =  db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    empresa_ejecutivo = db.Column(db.String(120))
    correlativo = db.Column(db.Integer, index=True)
    CMF_OK = db.Column(db.String(2))
    CARPETA_OK = db.Column(db.String(2))
    score_externo = db.Column(db.Integer)
    score_rdf = db.Column(db.Integer)
    score_final = db.Column(db.Integer)
    
    # empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))

    def __repr__(self):
        #return '<Consultas {}>'.format(self.cliente)
        return 'Fecha evaluacion: {}, Rut: {}, Cliente: {}, Score Final: {}'.format(self.fecha_ev, self.rut, self.cliente,  self.score_final)

    #     return 'ID Evaluacion: {}, Rut: {}, Cliente: {}, Fecha evaluacion: {}, Monto Linea: {}, Adicional: {}, Solicitudes: {}, Aprobados: {}, Empleados: {}, Hipotecario: {}, Score: {}, Deuda CMF: {}, Cupo CMF: {}, Mora CMF: {}, Instituciones CMF: {}, Total Ventas: {}, Impuesto Renta: {}, Total Compras: {}, Empleados SII: {}, Tramo Ventas SII: {}, Inicio Actividades: {}, Rubro SII: {}, Comuna SII: {}'\
    # .format(self.id, self.rut, self.cliente, self.fecha_ev, self.monto_linea, self.adicional, self.solicitudes, self.aprobados, self.empleados , self.hipotecario, self.score, self.cmf_deuda, self.cmf_cupo, self.cmf_mora, self.cmf_instituciones, self.iva_total_ventas_ano_1, self.iva_total_imp_renta_trab_ano_1, self.iva_total_compras_ano_1, self.sii_empleados, self.sii_tramo_ventas, self.sii_inicio_act, self.sii_rubro, self.sii_comuna)


class Sii(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20))
    tramoventas = db.Column(db.Integer)
    trabajadores = db.Column(db.Integer)
    inicio = db.Column(db.String(20))
    rubro = db.Column(db.String(200))
    comuna = db.Column(db.String(200))
    

    def __repr__(self):
        return 'RUT: {}, Tramo Ventas: {}, Trabajadores: {}, Fecha inicio actividades: {}, Rubro: {}, Comuna: {}'\
    .format(self.rut, self.tramoventas, self.trabajadores, self.inicio, self.rubro, self.comuna)
    
class Suspendidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20))
    razon = db.Column(db.String(200))
    autoridad = db.Column(db.Integer)
    suspension = db.Column(db.Integer)
    total = db.Column(db.Integer)    

    def __repr__(self):
        return 'RUT: {}, razon: {}, autoridad: {}, suspension: {}, total: {}'\
    .format(self.rut, self.razon, self.autoridad, self.suspension, self.total)