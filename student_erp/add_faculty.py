import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO faculty (name,email,password,department)
VALUES (?,?,?,?)
""",("Dr Sharma","sharma@erp.com","1234","Computer Science"))

conn.commit()
conn.close()

print("Faculty Added Successfully ✅")