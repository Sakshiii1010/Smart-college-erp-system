import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    title TEXT,
    pdf_file TEXT,
    ppt_file TEXT,
    uploaded_by TEXT
)
""")

# sample materials
cursor.execute("""
INSERT INTO materials (subject, title, pdf_file, ppt_file, uploaded_by)
VALUES
('Python','Python Basics','python_basics.pdf','python_slides.ppt','Prof Sharma'),
('DBMS','DBMS Introduction','dbms_notes.pdf','dbms_slides.ppt','Prof Singh')
""")

conn.commit()
conn.close()

print("Materials table ready ✅")