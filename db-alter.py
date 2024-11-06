import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
ALTER TABLE tprojects
RENAME COLUMN id TO p_id;
""")

connie.commit()
connie.close()