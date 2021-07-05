# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 11:12:33 2021

@author: user
"""

import csv, sqlite3
#from pandas import to_sql



con = sqlite3.connect('C:\\Users\\user\\Desktop\\MTS\\app.db') # change to 'sqlite:///your_filename.db'
#from sqlalchemy import create_engine
import pandas as pd

#engine = sqlalchemy.create_engine('sqlite:app.db)
df = pd.read_csv('C:\\Users\\user\\Desktop\\Suspendidos.csv')#, columns=['rut','tramoventas','trabajadores','inicio','rubro','comuna'])
df.to_sql('suspendidos',con=con, if_exists="append",index =True, index_label = 'id'  )