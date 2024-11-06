import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
connie.execute("PRAGMA foreign_keys = 1;")
c=connie.cursor()

c.execute("""
CREATE TABLE projectdetails
(	pro_id VARCHAR(10),
	p_des TEXT,
	p_rat TEXT,
	gd_id VARCHAR(15),
	dom_id VARCHAR(10),
	foreign key (pro_id) references tprojects (p_id),
	foreign key (gd_id) references tguide (g_id),
	foreign key (dom_id) references tdomain (d_id)
)
""")

connie.commit()
connie.close()
