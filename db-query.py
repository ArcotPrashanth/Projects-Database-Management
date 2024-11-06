from flask import Flask, render_template, request
from tkinter import messagebox
import sqlite3
db_locale='projectdatabase.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()
c.execute('PRAGMA foreign_keys = ON;')
c.execute('DELETE FROM s_contact')
connie.commit()
connie.close()

	#return render_template('addprojects.html')
