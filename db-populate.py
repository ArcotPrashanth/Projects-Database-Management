import sqlite3
db_locale='projects.db'

connie = sqlite3.connect(db_locale)
c=connie.cursor()

c.execute("""
INSERT INTO tprojects (title,doneBy,batch,usn) VALUES
('My Project','Prashanth','2018-22','1DT18IS009'),
('My First Project','Kishan','2018-22','1DT18IS042')
""")

connie.commit()
connie.close()
