import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
CREATE TABLE tcontact
(	t_id varchar(10) PRIMARY KEY,
	t_name varchar(255),
	t_mail varchar(255)
)
""")

connie.commit()
connie.close()