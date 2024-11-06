import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
DROP TABLE projectdetails;
""")

connie.commit()
connie.close()
