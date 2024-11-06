import sqlite3
db_locale='projectdatabase.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS s_contact
(	s_usn VARCHAR(10) PRIMARY KEY NOT NULL,
	s_name varchar(255 ) NOT NULL,
	s_mail varchar(255) NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS tprojects
(	p_id VARCHAR(10) PRIMARY KEY NOT NULL,
	title TEXT NOT NULL,
	doneBy TEXT NOT NULL,
	batch VARCHAR(15) NOT NULL,
	std_usn references s_contact (s_usn) ON DELETE CASCADE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS tdomain
(	d_id varchar(10) PRIMARY KEY NOT NULL,
	d_name varchar(255) NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS tcontact
(	t_id varchar(10) PRIMARY KEY NOT NULL,
	t_name varchar(255) NOT NULL,
	t_mail varchar(255) NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS tguide
(	g_id varchar(10) PRIMARY KEY NOT NULL,
	g_name varchar(255) NOT NULL,
	g_expertise varchar(255) NOT NULL,
	tch_id references tcontact (t_id) ON DELETE CASCADE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS projectdetails
(	p_des TEXT NOT NULL,
	p_rat TEXT NOT NULL,
	pro_id references tprojects (p_id) ON DELETE CASCADE,
	gd_id references tguide (g_id) ON DELETE CASCADE,
	dom_id references tdomain (d_id) ON DELETE CASCADE
)
""")

connie.commit()
connie.close()
