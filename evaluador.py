# -*- coding: utf-8 -*-
"""
Created on Sun May 30 20:51:56 2021

@author: user
"""

from app import create_app, db#, cli
from app.models import User, Consultas, Sii

app = create_app()
#cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Consultas' :Consultas, 'Sii': Sii}