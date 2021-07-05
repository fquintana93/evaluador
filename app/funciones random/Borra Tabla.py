# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 21:54:54 2021

@author: user
"""

import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('C:\\Users\\user\\Desktop\\MTS\\app.db') # change to 'sqlite:///your_filename.db'

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists
cursor.execute("DROP TABLE Sii")
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()