from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from tkinter import messagebox
import sqlite3

app = Flask(__name__)
app.secret_key = 'spd'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dbSql*1777'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)
db_locale='projectdatabase.db'

@app.route('/')
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
	# Output message if something goes wrong...
	msg = ''
	# Check if "username" and "password" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
		# Fetch one record and return result
		account = cursor.fetchone()
		# If account exists in accounts table in out database
		if account:
			# Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			# Redirect to home page
			msg = 'Logged in successfully!'
			projDetails=queryproject()
			print(projDetails)
			return render_template('home.html',projDetails=projDetails)
		else:
			# Account doesnt exist or username/password incorrect
			msg = 'Incorrect username/password!'
	# Show the login form with message (if any)
	return render_template('index.html', msg=msg)

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
	# Output message if something goes wrong...
	msg = ''
	# Check if "username", "password" and "email" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
		account = cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			msg = 'Account already exists!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address!'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers!'
		elif not username or not password or not email:
			msg = 'Please fill out the form!'
		else:
			# Account doesnt exists and the form data is valid, now insert new account into accounts table
			cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
			mysql.connection.commit()
			msg = 'You have successfully registered!'
	elif request.method == 'POST':
		# Form is empty... (no POST data)
		msg = 'Please fill out the form!'
	# Show registration form with message (if any)
	return render_template('register.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
	# Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/home')
def home():
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	if 'loggedin' in session:
		projDetails=queryproject()
		print(projDetails)
		return render_template('home.html',projDetails=projDetails)
	else:
		projDetails=queryproject()
		print(projDetails)
		return render_template('home_stu.html',projDetails=projDetails)

@app.route('/addproject',methods=['GET','POST'])
def addproject():
	if request.method=="GET":
		return render_template('addprojects.html')
	else:
		user_p=(
			request.form['ipid'],
			request.form['ititle'],
			request.form['idoneBy'],
			request.form['ibatch'],
			request.form['iusn']
			)
		user_s=(
			request.form['iusn'],
			request.form['isname'],
			request.form['isemail']
			)
		user_d=(
			request.form['idid'],
			request.form['idname']
			)
		user_g=(
			request.form['igid'],
			request.form['igname'],
			request.form['igexp']
			)
		user_pd=(
			request.form['ipid'],
			request.form['ipdes'],
			request.form['iprat'],
			request.form['idid'],
			request.form['igid']
			)
		insertproject(user_p,user_s,user_d,user_g,user_pd)
		return render_template('addsuccess.html')
		
def insertproject(user_p,user_s,user_d,user_g,user_pd):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='INSERT INTO tprojects (p_id,title,doneBy,batch,std_usn) VALUES (?,?,?,?,?)';
		c.execute(sql_execute_string,user_p)
		connie.commit()
		connie.close()
		print(user_p)
		insertpro_stu(user_s,user_d,user_g,user_pd)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def insertpro_stu(user_s,user_d,user_g,user_pd):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='INSERT INTO s_contact (s_usn,s_name,s_mail) VALUES (?,?,?)';
		c.execute(sql_execute_string,user_s)
		connie.commit()
		connie.close()
		print(user_s)
		insertpro_dom(user_d,user_g,user_pd)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def insertpro_dom(user_d,user_g,user_pd):
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	sql_execute_string='INSERT OR IGNORE INTO tdomain (d_id,d_name) VALUES (?,?)'
	c.execute(sql_execute_string,user_d)
	connie.commit()
	connie.close()
	print(user_d)
	insertpro_guide(user_g,user_pd)

def insertpro_guide(user_g,user_pd):
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	sql_execute_string='INSERT OR IGNORE INTO tguide (g_id,g_name,g_expertise) VALUES (?,?,?)';
	c.execute(sql_execute_string,user_g)
	connie.commit()
	connie.close()
	print(user_g)
	insertpro_details(user_pd)

def insertpro_details(user_pd):
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	sql_execute_string='INSERT OR IGNORE INTO projectdetails (pro_id,p_des,p_rat,dom_id,gd_id) VALUES (?,?,?,?,?)';
	c.execute(sql_execute_string,user_pd)
	connie.commit()
	connie.close()
	print(user_pd)

def queryproject():
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute('SELECT * FROM tprojects	ORDER BY p_id')
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")


@app.route('/delproject',methods=['GET','POST'])
def delproject():
	if request.method=="GET":
		return render_template('delprojects.html')
	else:
		user_projectt = request.form['did']
		user_projectu = request.form['usn']
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute('DELETE FROM s_contact WHERE s_usn=?',(user_projectu,))
		connie.commit()
		c.execute('DELETE FROM tprojects WHERE p_id=?',(user_projectt,))
		connie.commit()
		c.execute('DELETE FROM projectdetails WHERE pro_id=?',(user_projectt,))
		connie.commit()
		# altertproject()
		connie.close()
		return render_template('delsuccess.html')

def deleteproject(user_projectd):
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	sql_execute_string='DELETE '
	c.execute(sql_execute_string, (user_projectd,))
	connie.commit()
	# altertproject()
	connie.close()

@app.route('/studentcontact')
def studentcontact():
	try:
		studContact=querystudent()
		print(studContact)
		return render_template('studcont.html',studContact=studContact)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def querystudent():
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute("""
			SELECT * FROM s_contact

			""")
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/teachdetails')
def teachdetails():
	if 'loggedin' in session:
		try:
			teachDetails=queryteacher()
			print(teachDetails)
			return render_template('teach_details.html',teachDetails=teachDetails)
		except:
			messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")
	else :
		try:
			teacherList=queryteacher()
			print(teacherList)
			return render_template('teacherlist.html',teacherList=teacherList)
		except:
			messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def queryteacher():
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute("""
			SELECT * FROM tcontact

			""")
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/addteacher',methods=['GET','POST'])
def addteacher():
	try:
		if request.method=="GET":
			return render_template('addteachers.html')
		else:
			# user_guide=(
			# 	request.form['itid']
			# )
			user_teacher=(
				request.form['itid'],
				request.form['itname'],
				request.form['itmail']
			)
			insertteacher(user_teacher)
			# insertguide(user_guide)
			return render_template('addsuccess.html')
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def insertteacher(user_teacher):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='INSERT INTO tcontact (t_id,t_name,t_mail) VALUES (?,?,?)';
		c.execute(sql_execute_string,user_teacher)
		connie.commit()
		connie.close()
		print(user_teacher)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/openproject',methods=['GET','POST'])
def openproject():
	if 'loggedin' in session:
		try:
			if request.method=="GET":
				return render_template('openprojects.html')
			else:
				user_openpro=(
					request.form['ipid']
					)
				projOpen=openprojdetails(user_openpro)
				return render_template('openprojdetails.html',projOpen=projOpen)
		except:
			messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")
	else:
		try:
			if request.method=="GET":
				return render_template('openprojects.html')
			else:
				user_stuopenpro=(
					request.form['ipid']
					)
				projectOpen=openprojdetails(user_stuopenpro)
				return render_template('openprojdetails_stu.html',projectOpen=projectOpen)
		except:
			messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def openprojdetails(user_openpro):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='SELECT P.pro_id,T.title,P.p_des,P.p_rat,S.s_name,G.g_id,G.g_name,P.dom_id,D.d_name FROM projectdetails P,tguide G,tdomain D,tprojects T, s_contact S WHERE P.pro_id=? AND P.pro_id=T.p_id AND P.gd_id=G.g_id AND P.dom_id=D.d_id AND S.s_usn=T.std_usn';
		c.execute(sql_execute_string, (user_openpro,))
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/domaindetails')
def domaindetails():
	try:
		domDetails=querydomain()
		print(domDetails)
		return render_template('dominfo.html',domDetails=domDetails)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def querydomain():
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute("""
			SELECT * FROM tdomain

			""")
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/searchproject',methods=['GET','POST'])
def searchproject():
	try:
		if request.method=="GET":
			return render_template('home.html')
		else:
			user_searchpro=(
				request.form['psearch']
				)
			projSearch=srchproj(user_searchpro)
			return render_template('searchproject.html',projSearch=projSearch)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def srchproj(user_searchpro):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='SELECT * FROM tprojects WHERE title=?';
		c.execute(sql_execute_string, (user_searchpro,))
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/sortprojects',methods=['GET','POST'])
def sortprojects():
	try:
		if request.method=="GET":
			return render_template('sortby.html')
		else:
			user_sortpro=(
				request.form['isortby']
				)
			user_sortorder=(
				request.form['isortorder']
				)
			projSort=sortproj(user_sortpro,user_sortorder)
			return render_template('sortbyres.html',projSort=projSort)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def sortproj(user_sortpro,user_sortorder):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		if (user_sortorder=='Ascending'):
			if (user_sortpro=='Project ID'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY p_id ASC
				""")
			elif (user_sortpro=='Project Title'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY title ASC
				""")
			elif (user_sortpro=='Group Name'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY doneBy ASC
				""")
			elif (user_sortpro=='Batch'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY batch ASC
				""")
			elif (user_sortpro=='USN'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY std_usn ASC
				""")
		elif (user_sortorder=='Descending'):
			if (user_sortpro=='Project ID'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY p_id DESC
				""")
			elif (user_sortpro=='Project Title'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY title DESC
				""")
			elif (user_sortpro=='Group Name'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY doneBy DESC
				""")
			elif (user_sortpro=='Batch'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY batch DESC
				""")
			elif (user_sortpro=='USN'):
				c.execute("""
					SELECT * FROM tprojects ORDER BY std_usn DESC
				""")
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/delteacher',methods=['GET','POST'])
def delteacher():
	if request.method=="GET":
		return render_template('delteacher.html')
	else:
		user_delteach=(
			request.form['tname']
			)
		deleteteacher(user_delteach)
		return render_template('delsuccess.html')

def deleteteacher(user_delteach):
	connie=sqlite3.connect(db_locale)
	c=connie.cursor()
	sql_execute_string='DELETE FROM tcontact WHERE t_name=?';
	c.execute(sql_execute_string, (user_delteach,))
	connie.commit()
	# altertproject()
	connie.close()
	print(user_delteach)

@app.route('/guidedetails')
def guidedetails():
	try:
		guideDetails=queryguide()
		print(guideDetails)
		return render_template('guide_details.html',guideDetails=guideDetails)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def queryguide():
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		c.execute("""
			SELECT * FROM tguide

			""")
		projdata=c.fetchall()
		return projdata
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

@app.route('/updateproform',methods=['GET','POST'])
def updateproform():
	try:
		if request.method=="GET":
			return render_template('updateproform.html')
		else:
			# user_guide=(
			# 	request.form['itid']
			# )
			user_pro_form=(
				request.form['updes'],
				request.form['upID'],
				request.form['upTitle']
			)
			updateprodes(user_pro_form)
			# insertguide(user_guide)
			return render_template('upsuccess.html')
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")

def updateprodes(user_pro_form):
	try:
		connie=sqlite3.connect(db_locale)
		c=connie.cursor()
		sql_execute_string='UPDATE projectdetails SET p_des = ? WHERE pro_id = ? OR (SELECT title FROM tprojects)=?';
		c.execute(sql_execute_string,user_pro_form)
		connie.commit()
		connie.close()
		print(user_pro_form)
	except:
		messagebox.showerror("UNIQUE CONSTRAINT VIOLATION !","PLEASE ENTER DIFFERENT DATA")


if __name__ == '__main__':
	app.secret_key = 'spd'
	app.run(debug=True)
	root = Tk()
	root.mainloop()
# projects=[
# {
# 	'title': 'My Project',
# 	'done_by': 'Arcot Prashanth'
# },

# {
# 	'title': 'My First Project',
# 	'done_by': 'Kishan Bhat'
# }

# ]

# def altertproject():
# 	connie=sqlite3.connect(db_locale)
# 	c=connie.cursor()
# 	c.execute("""
# 		ALTER TABLE tprojects AUTO_INCREMENT = 1;
# 		""")
# 	connie.commit()
# 	connie.close()


# def insertguide(user_guide):
# 	connie=sqlite3.connect(db_locale)
# 	c=connie.cursor()
# 	sql_execute_string='INSERT OR REPLACE INTO tguide(tch_id) VALUES (?)';
# 	c.execute(sql_execute_string,(user_guide,))
# 	connie.commit()
# 	connie.close()
# 	print(user_guide)