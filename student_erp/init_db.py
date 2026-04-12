import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON")

# ---------------- CLEAN START ----------------
cursor.executescript("""
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS fees;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS faculty_courses;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS notices;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS attendance_sessions;
DROP TABLE IF EXISTS attendance_records;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS grievances;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS contact_messages;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS certificates;
DROP TABLE IF EXISTS library_books;
DROP TABLE IF EXISTS book_issues;
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admission_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    course TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

#---------------- EVENTS & NOTICES ----------------
cursor.execute("""
CREATE TABLE events_and_notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    type TEXT,          -- event OR notice
    date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- STUDENTS ----------------
cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    enrollment TEXT UNIQUE,
    password TEXT,
    course TEXT,
    semester TEXT,
    year TEXT
)
""")

cursor.execute("""
INSERT INTO students (name, enrollment, password, course, semester, year)
VALUES (?, ?, ?, ?, ?, ?)
""", ("Sakshi", "CS202401", generate_password_hash("12345"), "B.Tech CSE", "6", "2023-2027"))

# ---------------- SUBJECTS ----------------
cursor.execute("""
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_name TEXT,
    teacher_name TEXT,
    attendance INTEGER,
    internal_marks INTEGER,
    syllabus_file TEXT,
    course TEXT,
    semester TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

cursor.execute("""
INSERT INTO subjects (student_id, subject_name, teacher_name, attendance, internal_marks, course, semester)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (1, "Data Structures", "Mr. Sharma", 85, 78, "B.Tech CSE", "6"))

cursor.execute("""
INSERT INTO subjects (student_id, subject_name, teacher_name, attendance, internal_marks, course, semester)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (1, "Operating System", "Ms. Gupta", 90, 82, "B.Tech CSE", "6"))

# ---------------- FEES ----------------
cursor.execute("""
CREATE TABLE fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    total_fee INTEGER,
    paid_amount INTEGER,
    due_date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# ---------------- NOTIFICATIONS ----------------
cursor.execute("""
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    date TEXT,
    title TEXT,
    message TEXT,
    target TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

#-----------------STUDENT UNIFORM-----------------
cursor.execute("""
CREATE TABLE uniform_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    size TEXT,
    quantity INTEGER,
    gender TEXT,
    remarks TEXT,
    status TEXT DEFAULT 'Pending',
    date TEXT
)
""")

#----------------STUDENT ID CARD-------------
cursor.execute("""
CREATE TABLE id_card_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    father_name TEXT,
    student_id INTEGER,
    course TEXT,
    dob INTEGER,
    address TEXT,
    photo TEXT,
    status TEXT DEFAULT 'Pending',
    date TEXT
)
""")

#-----------STUDENT CERTIFICATE-------------
cursor.execute("""
CREATE TABLE certificate_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    certificate_type TEXT,
    purpose TEXT,
    status TEXT DEFAULT 'Pending',
    date TEXT
)
""")

#-----------STUDENT ADDITIONAL COURSE--------
cursor.execute("""
CREATE TABLE course_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_name TEXT,
    instructor TEXT,
    credits INTEGER,
    status TEXT DEFAULT 'Pending',
    date TEXT
)
""")

# ---------------- FACULTY ----------------
cursor.execute("""
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id TEXT,
    name TEXT,
    department TEXT,
    designation TEXT,
    email TEXT,
    phone TEXT,
    password TEXT,
    profile_pic TEXT
)
""")

# ---------------- ADMIN ----------------
cursor.execute("""
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
INSERT INTO admin (username, password)
VALUES (?, ?)
""", ("admin", generate_password_hash("admin123")))

# ---------------- COURSES ----------------
cursor.execute("""
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    description TEXT,
    duration TEXT
)
""")

# ---------------- ENROLLMENTS ----------------
cursor.execute("""
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

# ---------------- CERTIFICATES ----------------
cursor.execute("""
CREATE TABLE certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    file_path TEXT,
    issue_date TEXT
)
""")

# ---------------- LIBRARY ----------------
cursor.execute("""
CREATE TABLE library_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER
)
""")

cursor.execute("""
CREATE TABLE book_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    status TEXT
)
""")

# ---------------- ATTENDANCE ----------------
cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    date TEXT,
    status TEXT
)
""")

# ---------------- PAYMENTS ----------------
cursor.execute("""
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER,
    month TEXT,
    basic_salary INTEGER,
    allowances INTEGER,
    deductions INTEGER,
    net_salary INTEGER,
    status TEXT
)
""")

# ---------------- GRIEVANCES ----------------
cursor.execute("""
CREATE TABLE grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    subject TEXT,
    description TEXT,
    date TEXT,
    status TEXT
)
""")

# ---------------- SUPPORT ----------------
cursor.execute("""
CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    issue_type TEXT,
    description TEXT,
    date TEXT,
    status TEXT
)
""")

# ---------------- CONTACT ----------------
cursor.execute("""
CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    message TEXT,
    date TEXT
)
""")

# ---------------- NOTICES ----------------
cursor.execute("""
CREATE TABLE notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    message TEXT,
    date TEXT,
    posted_by TEXT
)
""")

#---------MISSING STUDENT TABLE FIELDS---------
cursor.execute("ALTER TABLE students ADD COLUMN branch TEXT")
#-----------ADMIN GRIEVANCE-----------------
cursor.execute("ALTER TABLE grievances ADD COLUMN admin_reply TEXT")
cursor.execute("ALTER TABLE grievances ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")


conn.commit()
conn.close()

print("✅ FULLY FIXED DATABASE READY")