import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
CREATE TABLE tdomain
(	d_id varchar(10) PRIMARY KEY,
	d_name varchar(255)
)
""")

connie.commit()
connie.close()