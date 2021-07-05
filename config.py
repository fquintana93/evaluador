import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('la-mas-brigida-de-las-claves-ultrasecretas-nunca-sera-revelada') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #MAIL_SERVER=os.environ.get('smtp.googlemail.com')
    #MAIL_PORT=int(os.environ.get('587') or 25)
    #MAIL_USE_TLS=1
    #MAIL_USERNAME=os.environ.get('soporte.rdfspa@gmail.com')
    #MAIL_PASSWORD=os.environ.get('Rdfspa123456.')
    ADMINS=['soporte.rdfspa@gmail.com']
    POSTS_PER_PAGE = 8
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='soporte.rdfspa@gmail.com'
    MAIL_PASSWORD='Rdfspa123456.'
    LANGUAGES = ['en', 'es']
    UPLOADED_DOCUMENTS_DEST = 'C:\\Users\\user\\Desktop\\MTS\\uploads\\'
    ELASTICSEARCH_URL = 'http://localhost:9200'#os.environ.get('http://localhost:9200')
