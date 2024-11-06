import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
CREATE TABLE s_contact
(	s_usn VARCHAR(10) PRIMARY KEY,
	s_name varchar(255),
	s_mail varchar(255)
)
""")

connie.commit()
connie.close()
