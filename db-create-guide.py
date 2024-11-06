import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
CREATE TABLE tguide
(	g_id varchar(10) PRIMARY KEY,
	g_name varchar(255),
	g_expertise varchar(255),
	tch_id varchar(10),
	foreign key (tch_id) references tcontact (t_id)
)
""")

connie.commit()
connie.close()
