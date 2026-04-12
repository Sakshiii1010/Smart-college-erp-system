from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle
from werkzeug.security import generate_password_hash
from flask import send_file
import io
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = "student_erp_secret"

UPLOAD_FOLDER = "static/uploads/id_photos"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def require_student():
    if "student_id" not in session:
        return redirect(url_for("login"))
    
# 🔹 Homepage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admissions')
def admissions():
    return render_template('admissions.html')

@app.route('/apply-admission', methods=['GET', 'POST'])
def apply_admission():

    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        message = request.form['message']

        conn.execute("""
            INSERT INTO admission_applications
            (name, email, phone, course, message)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, course, message))

        conn.commit()
        conn.close()

        return "Application Submitted Successfully ✅"

    conn.close()
    return render_template('apply_admission.html')

@app.route('/admin/admissions')
def admin_admissions():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    applications = conn.execute("""
        SELECT * FROM admission_applications
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return render_template('admin_admissions.html', applications=applications)

#------------EVENTS & NOTICES----------------
@app.route('/events-and-notices')
def events_and_notices():

    conn = get_db_connection()

    data = conn.execute("""
        SELECT * FROM events_and_notices
        ORDER BY date DESC
    """).fetchall()

    conn.close()

    return render_template("events_and_notices.html", data=data)

@app.route('/admin/add-events-and-notices', methods=["GET", "POST"])
def add_events_and_notices():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        type_ = request.form["type"]
        date = request.form["date"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO events_and_notices (title, description, type, date)
            VALUES (?, ?, ?, ?)
        """, (title, description, type_, date))

        conn.commit()
        conn.close()

        return redirect('/events-and-notices')

    return render_template("add_events_and_notices.html")

#-----------------ADMIN EVENTS & NOTICES----------------
@app.route('/admin/events-and-notices')
def admin_events_and_notices():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    data = conn.execute("""
        SELECT * FROM events_and_notices
        ORDER BY date DESC
    """).fetchall()

    conn.close()

    return render_template("admin_events_and_notices.html", data=data)

#-------------ADD EVENTS AND NOTICES-----------------
@app.route('/admin/add-events-and-notices', methods=["GET", "POST"])
def admin_add_events_and_notices():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        type_ = request.form["type"]
        date = request.form["date"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO events_and_notices (title, description, type, date)
            VALUES (?, ?, ?, ?)
        """, (title, description, type_, date))

        conn.commit()
        conn.close()

        return redirect('/admin/events-and-notices')

    return render_template("admin_add_events_and_notices.html")

#---------------------ADMIN EDIT EVENTS & NOTICES----------------
@app.route('/admin/edit-events-and-notices/<int:id>', methods=["GET", "POST"])
def edit_events_and_notices(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        type_ = request.form["type"]
        date = request.form["date"]

        conn.execute("""
            UPDATE events_and_notices
            SET title=?, description=?, type=?, date=?
            WHERE id=?
        """, (title, description, type_, date, id))

        conn.commit()
        conn.close()

        return redirect('/admin/events-and-notices')

    item = conn.execute(
        "SELECT * FROM events_and_notices WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("admin_edit_events_and_notices.html", item=item)

#------------------ ADMIN DELETE EVENTS & NOTICES ----------------
@app.route('/admin/delete-events-and-notices/<int:id>')
def delete_events_and_notices(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("DELETE FROM events_and_notices WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/admin/events-and-notices')

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        role = request.form["role"]
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()

        # ---------- STUDENT LOGIN ----------
        if role == "student":
            student = conn.execute(
                "SELECT * FROM students WHERE enrollment=?",
                (username,)
            ).fetchone()

            if student:
                stored_password = student["password"]

                try:
                    if check_password_hash(stored_password, password):
                        session.clear()
                        session["student_id"] = student["id"]
                        conn.close()
                        return redirect(url_for("student_dashboard"))
                except:
                    pass

                if stored_password == password:
                    session.clear()
                    session["student_id"] = student["id"]
                    conn.close()
                    return redirect(url_for("student_dashboard"))

        # ---------- FACULTY LOGIN ----------
        elif role == "faculty":
            faculty = conn.execute(
                "SELECT * FROM faculty WHERE faculty_id=?",
                (username,)
            ).fetchone()

            if faculty:
                stored_password = faculty["password"]

                try:
                    if check_password_hash(stored_password, password):
                        session.clear()
                        session["faculty_id"] = faculty["id"]
                        conn.close()
                        return redirect(url_for("faculty_dashboard"))
                except:
                    pass

                if stored_password == password:
                    session.clear()
                    session["faculty_id"] = faculty["id"]
                    conn.close()
                    return redirect(url_for("faculty_dashboard"))

        # ---------- ADMIN LOGIN ----------
        elif role == "admin":
            admin = conn.execute(
                "SELECT * FROM admin WHERE username=?",
                (username,)
            ).fetchone()

            if admin:
                stored_password = admin["password"]

                try:
                    if check_password_hash(stored_password, password):
                        session.clear()
                        session["admin_id"] = admin["id"]
                        conn.close()
                        return redirect(url_for("admin_dashboard"))
                except:
                    pass

                if stored_password == password:
                    session.clear()
                    session["admin_id"] = admin["id"]
                    conn.close()
                    return redirect(url_for("admin_dashboard"))

        conn.close()
        return "Invalid Credentials ❌"

    return render_template("login.html")

#------------ADMIN HELPER FUNCTION-------------
def admin_required():
    if "admin_id" not in session:
        return redirect(url_for("login"))
    return None

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    # Admin info
    admin = conn.execute(
        "SELECT * FROM admin WHERE id=?",
        (session["admin_id"],)
    ).fetchone()

    # 📊 COUNTS (like system overview)
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_faculty = conn.execute("SELECT COUNT(*) FROM faculty").fetchone()[0]

    # ⚠️ Only if table exists (else remove for now)
    try:
        total_grievances = conn.execute("SELECT COUNT(*) FROM grievances").fetchone()[0]
    except:
        total_grievances = 0

    try:
        total_notifications = conn.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
    except:
        total_notifications = 0

    # 🕒 Recent students (for activity feel)
    recent_students = conn.execute("""
        SELECT name, enrollment FROM students
        ORDER BY id DESC LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        total_students=total_students,
        total_faculty=total_faculty,
        total_grievances=total_grievances,
        total_notifications=total_notifications,
        recent_students=recent_students
    )
    
# ---------------- ADMIN: VIEW STUDENTS ----------------
@app.route('/admin/students')
def admin_students():
    check = admin_required()
    if check:
        return check

    search = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR enrollment LIKE ?
        """, ('%' + search + '%', '%' + search + '%'))
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    conn.close()

    return render_template("admin_students.html", students=students, search=search)

# ---------------- DELETE STUDENT ----------------
@app.route("/admin/delete_student/<int:id>")
def delete_student(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect(url_for("admin_students"))

#-----------------ADD STUDENT--------------
#-------------- ADMIN ADD STUDENT ----------------
@app.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        enrollment = request.form.get('enrollment')
        password = request.form.get('password')
        course = request.form.get('course')
        semester = request.form.get('semester')
        year = request.form.get('year')

        conn = get_db_connection()

        conn.execute("""
        INSERT INTO students 
        (name, enrollment, password, course, semester, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, enrollment, password, course, semester, year))

        conn.commit()
        conn.close()

        return redirect('/admin/students')

    return render_template('add_student.html')
#---------------------EDIT STUDENT OPTION------------------------
@app.route('/admin/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    check = admin_required()
    if check:
        return check

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        enrollment = request.form['enrollment']
        branch = request.form['branch']
        year = request.form['year']

        cursor.execute("""
            UPDATE students
            SET name=?, enrollment=?, branch=?, year=?
            WHERE id=?
        """, (name, enrollment, branch, year, id))

        conn.commit()
        conn.close()

        return redirect('/admin/students')

    # GET request
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template('edit_student.html', student=student)

# ---------------- ADMIN: VIEW FACULTY ----------------
@app.route('/admin/faculty')
def admin_faculty():
    check = admin_required()
    if check:
        return check

    search = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM faculty
            WHERE name LIKE ? OR faculty_id LIKE ? OR department LIKE ?
        """, ('%' + search + '%', '%' + search + '%', '%' + search + '%'))
    else:
        cursor.execute("SELECT * FROM faculty")

    faculty = cursor.fetchall()
    conn.close()

    return render_template("admin_faculty.html", faculty=faculty, search=search)

# ---------------- ADMIN ADD FACULTY ----------------
@app.route('/admin/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    check = admin_required()
    if check:
        return check

    if request.method == 'POST':
        name = request.form['name']
        faculty_id = request.form['faculty_id']
        department = request.form['department']
        designation = request.form['designation']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO faculty 
            (faculty_id, name, department, designation, email, phone, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (faculty_id, name, department, designation, email, phone, password))

        conn.commit()
        conn.close()

        return redirect('/admin/faculty')

    return render_template('admin_add_faculty.html')

# ---------------- ADMIN EDIT FACULTY ----------------
@app.route('/admin/edit_faculty/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    check = admin_required()
    if check:
        return check

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        faculty_id = request.form['faculty_id']
        department = request.form['department']
        designation = request.form['designation']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute("""
            UPDATE faculty
            SET name=?, faculty_id=?, department=?, designation=?, email=?, phone=?
            WHERE id=?
        """, (name, faculty_id, department, designation, email, phone, id))

        conn.commit()
        conn.close()

        return redirect('/admin/faculty')

    cursor.execute("SELECT * FROM faculty WHERE id=?", (id,))
    faculty = cursor.fetchone()
    conn.close()

    return render_template('admin_edit_faculty.html', faculty=faculty)

# ---------------- ADMIN DELETE FACULTY ----------------
@app.route("/admin/delete_faculty/<int:id>")
def delete_faculty(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("DELETE FROM faculty WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect(url_for("admin_faculty"))

#--------------- ADMIN NOTIFICATIONS LIST ------------------
@app.route('/admin/notifications')
def admin_notifications():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    notifications = conn.execute(
        "SELECT * FROM notifications ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template('admin_notifications.html', notifications=notifications)


#---------------- ADMIN ADD NOTIFICATION -------------------
@app.route("/admin/add_notification", methods=["GET", "POST"])
def add_notification():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        target = request.form.get("target")

        conn.execute("""
            INSERT INTO notifications (title, message, target, student_id, faculty_id)
            VALUES (?, ?, ?, NULL, NULL)
        """, (title, message, target))

        conn.commit()
        conn.close()

        return redirect(url_for("admin_notifications"))

    conn.close()
    return render_template("admin_add_notification.html")


#---------------- ADMIN EDIT NOTIFICATION ------------------
@app.route('/admin/edit_notification/<int:id>', methods=['GET', 'POST'])
def edit_notification(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        target = request.form['target']

        conn.execute("""
            UPDATE notifications
            SET title=?, message=?, target=?
            WHERE id=?
        """, (title, message, target, id))

        conn.commit()
        conn.close()

        return redirect(url_for("admin_notifications"))

    notification = conn.execute(
        "SELECT * FROM notifications WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template('admin_edit_notification.html', notification=notification)


#-------------- ADMIN DELETE NOTIFICATION ------------------
@app.route("/admin/delete_notification/<int:id>")
def delete_notification(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM notifications WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_notifications"))

#----------------- ADMIN VIEW ALL GRIEVANCES ----------------
@app.route('/admin/grievances')
def admin_grievances():

    if "admin_id" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search")

    conn = get_db_connection()
    
    if search:
        grievances = conn.execute("""
            SELECT * FROM grievances
            WHERE subject LIKE ?
            ORDER BY created_at DESC
        """, ('%' + search + '%')).fetchall()
    else:
        grievances = conn.execute("""
            SELECT * FROM grievances 
            ORDER BY created_at DESC
        """).fetchall()

    conn.close()

    return render_template("admin_grievances.html", grievances=grievances)

#----------------- ADMIN VIEW + REPLY ----------------
@app.route('/admin/grievance/<int:id>', methods=['GET', 'POST'])
def view_grievance(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    # ✅ FETCH FIRST (VERY IMPORTANT)
    grievance = conn.execute(
        "SELECT * FROM grievances WHERE id=?",
        (id,)
    ).fetchone()

    if not grievance:
        conn.close()
        return "Grievance not found"

    if request.method == "POST":
        reply = request.form["reply"]
        status = request.form["status"]

        # ✅ UPDATE grievance
        conn.execute("""
            UPDATE grievances
            SET admin_reply=?, status=?
            WHERE id=?
        """, (reply, status, id))

        # 🔔 ADD NOTIFICATION (NOW grievance exists)
        conn.execute("""
            INSERT INTO notifications (student_id, title, message, target)
            VALUES (?, ?, ?, ?)
        """, (
            grievance["student_id"],
            "Grievance Update",
            f"Your grievance '{grievance['subject']}' has been {status}.",
            "student"
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("admin_grievances"))

    conn.close()
    return render_template("admin_view_grievance.html", grievance=grievance)

#------------------ ADMIN DELETE GRIEVANCE ----------------
@app.route('/admin/delete_grievance/<int:id>')
def delete_grievance(id):

    if "admin_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("DELETE FROM grievances WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_grievances"))

# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (session["student_id"],)
    ).fetchone()

    unread_count = conn.execute("""
        SELECT COUNT(*) FROM notifications
        WHERE (student_id=? OR student_id IS NULL)
        AND is_read=0
    """, (session["student_id"],)).fetchone()[0]

    conn.close()

    return render_template(
        "student_dashboard.html",
        student=student,
        unread_count=unread_count
    )
# ---------------- FACULTY DASHBOARD ----------------
@app.route("/faculty/dashboard")
def faculty_dashboard():

    if "faculty_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    faculty = conn.execute(
        "SELECT * FROM faculty WHERE id=?",
        (session["faculty_id"],)
    ).fetchone()

    conn.close()

    return render_template("faculty_dashboard.html", faculty=faculty)

# ---------------- FACULTY ----------------
# ---------------- FACULTY COURSES ----------------
@app.route("/faculty/courses")
def faculty_courses():

    if "faculty_id" not in session:
        return redirect(url_for("login"))

    faculty_id = session["faculty_id"]

    conn = get_db_connection()

    courses = conn.execute("""
        SELECT id, subject_name, course, semester
        FROM subjects
    """).fetchall()

    conn.close()

    return render_template(
        "faculty_courses.html",
        courses=courses
    )
    
# ---------------- FACULTY STUDENTS ----------------
@app.route("/faculty/students/<int:subject_id>")
def faculty_students(subject_id):

    if "faculty_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    subject = conn.execute(
        "SELECT * FROM subjects WHERE id=?",
        (subject_id,)
    ).fetchone()

    students = conn.execute("""
        SELECT * FROM students
        WHERE course=? AND semester=?
    """, (subject["course"], subject["semester"])).fetchall()

    conn.close()

    return render_template(
        "faculty_students.html",
        subject=subject,
        students=students
    )
    
# ---------------- FACULTY ATTENDANCE ----------------
@app.route("/faculty/attendance")
def faculty_attendance():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    subjects = conn.execute("""
        SELECT id, subject_name, course, semester
        FROM subjects
    """).fetchall()

    conn.close()

    return render_template(
        "faculty_attendance.html",
        subjects=subjects
    )
#---------------TAKE ATTENDANCE----------------------------------------
@app.route("/faculty/take_attendance/<int:subject_id>", methods=["GET","POST"])
def take_attendance(subject_id):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    subject = conn.execute("""
        SELECT * FROM subjects
        WHERE id = ?
    """,(subject_id,)).fetchone()

    students = conn.execute("""
        SELECT * FROM students
        WHERE course = ? AND semester = ?
    """,(subject["course"],subject["semester"])).fetchall()

    if request.method == "POST":

        date = request.form["date"]

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO attendance_sessions (subject_id,date)
        VALUES (?,?)
        """,(subject_id,date))

        session_id = cursor.lastrowid

        for student in students:

            status = request.form.get(f"status_{student['id']}")

            cursor.execute("""
            INSERT INTO attendance_records
            (session_id,student_id,status)
            VALUES (?,?,?)
            """,(session_id,student["id"],status))

        conn.commit()

        return redirect("/faculty/attendance")

    return render_template(
        "take_attendance.html",
        subject=subject,
        students=students
    )
    
# ---------------- FACULTY PAYMENTS ----------------
@app.route("/faculty/payments")
def faculty_payments():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    payments = conn.execute("""
        SELECT * FROM payments
        WHERE faculty_id = ?
    """, (faculty_id,)).fetchall()

    conn.close()

    return render_template(
        "faculty_payments.html",
        payments=payments
    )

# ---------------- FACULTY GRIEVANCE ----------------
@app.route("/faculty/grievance", methods=["GET", "POST"])
def faculty_grievance():

    if "faculty_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        subject = request.form["subject"]
        description = request.form["description"]

        conn.execute("""
            INSERT INTO grievances (faculty_id, subject, description, date, status)
            VALUES (?, ?, ?, datetime('now'), ?)
        """, (session["faculty_id"], subject, description, "Pending"))

        conn.commit()

    grievances = conn.execute("""
        SELECT * FROM grievances WHERE faculty_id=?
    """, (session["faculty_id"],)).fetchall()

    conn.close()

    return render_template("faculty_grievance.html", grievances=grievances)
    
# ---------------- FACULTY NOTICES ----------------
@app.route("/faculty/notices")
def faculty_notices():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    notices = conn.execute("""
        SELECT * FROM notices
        ORDER BY date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "faculty_notices.html",
        notices=notices
    )
    
# ---------------- FACULTY HELP ----------------
@app.route("/faculty/help", methods=["GET", "POST"])
def faculty_help():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    # 🔹 SUBMIT TICKET
    if request.method == "POST":

        issue_type = request.form["issue_type"]
        description = request.form["description"]

        conn.execute("""
            INSERT INTO support_tickets
            (faculty_id, issue_type, description, date, status)
            VALUES (?, ?, ?, DATE('now'), 'Pending')
        """, (faculty_id, issue_type, description))

        conn.commit()

    # 🔹 FETCH MY TICKETS
    tickets = conn.execute("""
        SELECT * FROM support_tickets
        WHERE faculty_id = ?
        ORDER BY date DESC
    """, (faculty_id,)).fetchall()

    conn.close()

    return render_template(
        "faculty_help.html",
        tickets=tickets
    )
    
# ---------------- FACULTY PROFILE ----------------
@app.route("/faculty/profile", methods=["GET", "POST"])
def faculty_profile():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    # 🔹 UPDATE PROFILE
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE faculty
            SET name = ?, phone = ?
            WHERE id = ?
        """, (name, phone, faculty_id))

        conn.commit()

    # 🔹 FETCH DATA
    faculty = conn.execute("""
        SELECT * FROM faculty WHERE id = ?
    """, (faculty_id,)).fetchone()

    conn.close()

    return render_template(
        "faculty_profile.html",
        faculty=faculty
    )
    
# ---------------- FACULTY DEPARTMENT ----------------
@app.route("/faculty/department")
def faculty_department():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    # 🔹 Get faculty details
    faculty = conn.execute("""
        SELECT * FROM faculty WHERE id = ?
    """, (faculty_id,)).fetchone()

    # 🔹 Get subjects (based on your existing table)
    subjects = conn.execute("""
        SELECT subject_name, course, semester
        FROM subjects
    """).fetchall()

    conn.close()

    return render_template(
        "faculty_department.html",
        faculty=faculty,
        subjects=subjects
    )
    
# ---------------- FACULTY ALL STUDENTS ----------------
@app.route("/faculty/students")
def faculty_all_students():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    # 🔹 Get filter values
    course = request.args.get("course")
    semester = request.args.get("semester")
    search = request.args.get("search")

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    # 🔍 Apply filters
    if course:
        query += " AND course = ?"
        params.append(course)

    if semester:
        query += " AND semester = ?"
        params.append(semester)

    if search:
        query += " AND (name LIKE ? OR enrollment LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    students = conn.execute(query, params).fetchall()

    conn.close()

    return render_template(
        "faculty_all_students.html",
        students=students
    )
    
# ---------------- FACULTY CONTACTS ----------------
@app.route("/faculty/contacts", methods=["GET", "POST"])
def faculty_contacts():

    if "faculty_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    faculty_id = session["faculty_id"]

    # 🔹 Handle message submit
    if request.method == "POST":
        message = request.form["message"]

        conn.execute("""
            INSERT INTO contact_messages (faculty_id, message, date)
            VALUES (?, ?, DATE('now'))
        """, (faculty_id, message))

        conn.commit()

    conn.close()

    return render_template("faculty_contacts.html")
# ---------------- STUDENT ----------------
# ---------------- ACADEMICS PAGE ----------------
@app.route("/student/academics")
def academics():
    if "student_id" not in session:
        return redirect(url_for("login"))

    
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (session["student_id"],)
    ).fetchone()

    subjects = conn.execute(
        "SELECT * FROM subjects WHERE student_id=?",
        (session["student_id"],)
    ).fetchall()

    conn.close()

    total_marks = 0
    total_subjects = len(subjects)
    subjects_with_grades = []

    for sub in subjects:
        marks = sub["internal_marks"]

        if marks >= 90:
            grade = "A+"
        elif marks >= 75:
            grade = "A"
        elif marks >= 60:
            grade = "B"
        elif marks >= 50:
            grade = "C"
        else:
            grade = "F"

        total_marks += marks

        subjects_with_grades.append({
            "name": sub["subject_name"],
            "marks": marks,
            "grade": grade
        })

    gpa = round(total_marks / total_subjects, 2) if total_subjects > 0 else 0
    status = "PASS" if all(s["grade"] != "F" for s in subjects_with_grades) else "FAIL"
    
    subject_names = [sub["name"] for sub in subjects_with_grades]
    subject_marks = [sub["marks"] for sub in subjects_with_grades]
    
    return render_template(
        "academics.html",
        student=student,
        subjects=subjects_with_grades,
        gpa=gpa,
        status=status,
        subject_names=subject_names,
        subject_marks=subject_marks
    )

# ---------------- RESULTS ----------------
@app.route("/student/results")
def student_results():
    
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (session["student_id"],)
    ).fetchone()

    subjects = conn.execute(
        "SELECT * FROM subjects WHERE student_id=?",
        (session["student_id"],)
    ).fetchall()

    conn.close()

    total_marks = 0
    total_subjects = len(subjects)
    subjects_with_results = []

    for sub in subjects:
        marks = sub["internal_marks"]

        # Grade Logic
        if marks >= 90:
            grade = "A+"
        elif marks >= 75:
            grade = "A"
        elif marks >= 60:
            grade = "B"
        elif marks >= 50:
            grade = "C"
        else:
            grade = "F"

        result = "PASS" if marks >= 50 else "FAIL"

        total_marks += marks

        subjects_with_results.append({
            "name": sub["subject_name"],
            "marks": marks,
            "grade": grade,
            "result": result
        })

    average = round(total_marks / total_subjects, 2) if total_subjects > 0 else 0

    overall_result = "PASS" if all(s["result"] == "PASS" for s in subjects_with_results) else "FAIL"

    # Division
    if average >= 75:
        division = "Distinction"
    elif average >= 60:
        division = "First Class"
    elif average >= 50:
        division = "Second Class"
    else:
        division = "Fail"

    return render_template(
        "results.html",
        student=student,
        subjects=subjects_with_results,
        average=average,
        overall_result=overall_result,
        division=division
    )
    
# ---------------- RESULT DOWNLOAD ---------------
@app.route("/download-result")
def download_result_pdf():
   
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (session["student_id"],)
    ).fetchone()

    subjects = conn.execute(
        "SELECT * FROM subjects WHERE student_id=?",
        (session["student_id"],)
    ).fetchall()

    conn.close()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("Student Result Card", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Name: {student['name']}", styles['Normal']))
    elements.append(Paragraph(f"Enrollment: {student['enrollment']}", styles['Normal']))
    elements.append(Paragraph(f"Course: {student['course']}", styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [["Subject", "Marks"]]

    for sub in subjects:
        data.append([sub["subject_name"], sub["internal_marks"]])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="result_card.pdf",
        mimetype='application/pdf'
    )
    
# ---------------- GRIEVANCE ----------------
@app.route("/student/grievance", methods=["GET", "POST"])
def student_grievance():

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        category = request.form.get("category")
        description = request.form.get("description")
        
        if not category or not description:
            return "Form error: Missing fields"

        conn.execute("""
            INSERT INTO grievances (student_id, subject, description, date, status)
            VALUES (?, ?, ?, datetime('now'), ?)
        """, (session["student_id"], category, description, "Pending"))

        conn.commit()

    grievances = conn.execute("""
        SELECT * FROM grievances WHERE student_id=?
    """, (session["student_id"],)).fetchall()

    conn.close()

    return render_template("student_grievance.html", grievances=grievances)

# ---------------- NOTIFICATIONS ----------------
@app.route("/student/notifications")
def student_notifications():

    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    notifications = conn.execute("""
        SELECT * FROM notifications
        WHERE student_id=? OR student_id IS NULL
        ORDER BY date DESC
    """, (session["student_id"],)).fetchall()

    conn.close()

    return render_template("notifications.html", notifications=notifications)
# ---------------- NOTIFICATIONS MARK READ ----------------
@app.route("/notification/read/<int:notif_id>")
def mark_notification_read(notif_id):
 
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    conn.execute("""
        UPDATE notifications
        SET is_read=1
        WHERE id=?
    """, (notif_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("student_notifications"))

# ---------------- UNIFORM ----------------
@app.route("/student/uniform", methods=["GET", "POST"])
def student_uniform():
    
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    # Submit new application
    if request.method == "POST":
        size = request.form["size"]
        quantity = request.form["quantity"]
        gender = request.form["gender"]
        remarks = request.form["remarks"]

        conn.execute("""
            INSERT INTO uniform_applications
            (student_id, size, quantity, gender, remarks, status, date)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (session["student_id"], size, quantity, gender, remarks, "Pending"))

        conn.commit()

    # Fetch all applications
    applications = conn.execute("""
    SELECT * FROM uniform_applications
    WHERE student_id=?
    ORDER BY date DESC
    """, (session["student_id"],)).fetchall()

    conn.close()

    return render_template("uniform.html", applications=applications)
# ----------------CANCEL UNIFORM ----------------
@app.route("/uniform/cancel/<int:app_id>")
def cancel_uniform(app_id):
   
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    # Only cancel if status is Pending
    conn.execute("""
        UPDATE uniform_applications
        SET status='Cancelled'
        WHERE id=? AND status='Pending'
    """, (app_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("student_uniform"))

# ---------------- APPLY ID CARD ----------------
@app.route("/student/apply-id-card", methods=["GET","POST"])
def apply_id_card():
    
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        full_name = request.form["full_name"]
        father_name = request.form["father_name"]
        dob = request.form["dob"]
        course = request.form["course"]
        address = request.form["address"]

        photo = request.files["photo"]

        filename = None

        if photo and photo.filename != "":
            upload_folder = "static/uploads/id_photos"
            os.makedirs(upload_folder, exist_ok=True)

            filename = photo.filename
            photo.save(os.path.join(upload_folder, filename))

        conn.execute("""
        INSERT INTO id_card_applications
        (student_id, full_name, father_name, dob, course, address, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (session["student_id"], full_name, father_name, dob, course, address, filename))

        conn.commit()

    applications = conn.execute("""
    SELECT * FROM id_card_applications
    WHERE student_id=?
    ORDER BY date DESC
    """, (session["student_id"],)).fetchall()

    conn.close()

    return render_template("apply_id_card.html", applications=applications)

# ---------------- CERTIFICATES PAGE ----------------
@app.route("/student/certificates", methods=["GET", "POST"])
def certificates():
    
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    if request.method == "POST":

        certificate_type = request.form["certificate_type"]
        purpose = request.form["purpose"]

        conn.execute("""
            INSERT INTO certificate_applications
            (student_id, certificate_type, purpose, status, date)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (session["student_id"], certificate_type, purpose, "Pending"))

        conn.commit()

    applications = conn.execute("""
        SELECT * FROM certificate_applications
        WHERE student_id = ?
        ORDER BY date DESC
    """, (session["student_id"],)).fetchall()

    conn.close()

    return render_template("certificates.html", applications=applications)
# ---------------- DOWNLOAD CERTIFICATE PDF ----------------
@app.route("/download-certificate/<int:app_id>")
def download_certificate(app_id):
    
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()

    app = conn.execute("""
        SELECT * FROM certificate_applications
        WHERE id=? AND student_id=?
    """, (app_id, session["student_id"])).fetchone()

    student = conn.execute("""
        SELECT * FROM students
        WHERE id=?
    """, (session["student_id"],)).fetchone()

    conn.close()

    if not app:
        return "Certificate not found"

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 800, "Kalinga University")

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(300, 770, f"{app['certificate_type']} Certificate")

    pdf.setFont("Helvetica", 12)

    text = f"""
This is to certify that {student['name']}
is a bonafide student of {student['course']}
in Semester {student['semester']}.

This certificate is issued for the purpose of:
{app['purpose']}

Date: {app['date']}
"""

    y = 700
    for line in text.split("\n"):
        pdf.drawString(100, y, line)
        y -= 20

    pdf.drawString(100, 550, "Authorized Signatory")
    pdf.drawString(100, 530, "Kalinga University")

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="certificate.pdf",
        mimetype="application/pdf"
    )
    
# ---------------- EDIT PROFILE ----------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    
    if "student_id" not in session:
        return redirect(url_for("login"))
    
    student_id = session["student_id"]
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        profile_pic = request.files.get("profile_pic")

        if profile_pic and profile_pic.filename != "":
            upload_folder = "static/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, profile_pic.filename)
            profile_pic.save(file_path)

            cursor.execute("""
                UPDATE students
                SET name=?, profile_pic=?
                WHERE id=?
            """, (name, profile_pic.filename, student_id))

        else:
            cursor.execute("""
                UPDATE students
                SET name=?
                WHERE id=?
            """, (name, student_id))

        conn.commit()
        conn.close()
        return redirect(url_for("student_dashboard"))

    student = cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()
    return render_template("edit_profile.html", student=student)


# ---------------- ADD SUBJECT MASTER ----------------
@app.route("/add-subject", methods=["GET","POST"])
def add_subject_master():

    if request.method == "POST":
        name = request.form["name"]
        code = request.form["code"]
        sem = request.form["semester"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO subjects (subject_name, subject_code, semester) VALUES (?, ?, ?)",
            (name, code, sem)
        )

        conn.commit()
        conn.close()

        return "Subject Added Successfully!"

    return render_template("add_subject.html")


# ---------------- ADMIN ADD SUBJECT MARKS ----------------
@app.route("/admin/add-subject", methods=["GET", "POST"])
def add_subject_admin():

    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":
        student_id = request.form["student_id"]
        subject_name = request.form["subject_name"]
        marks = request.form["marks"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO subjects (student_id, subject_name, internal_marks) VALUES (?, ?, ?)",
            (student_id, subject_name, marks)
        )
        conn.commit()
        conn.close()

        return "Marks Added Successfully ✅"

    return render_template("add_subject.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/admin/subjects")
        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")


# ---------------- ADMIN SUBJECT LIST ----------------
@app.route("/admin/subjects")
def admin_subjects():

    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()

    subjects = conn.execute("""
        SELECT subjects.*, students.name
        FROM subjects
        JOIN students ON subjects.student_id = students.id
    """).fetchall()

    conn.close()

    return render_template("admin_subjects.html", subjects=subjects)


# ---------------- EDIT SUBJECT ----------------
@app.route("/admin/edit-subject/<int:id>", methods=["GET","POST"])
def edit_subject(id):

    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["subject_name"]
        marks = request.form["marks"]

        conn.execute(
            "UPDATE subjects SET subject_name=?, internal_marks=? WHERE id=?",
            (name, marks, id)
        )
        conn.commit()
        conn.close()

        return redirect("/admin/subjects")

    subject = conn.execute(
        "SELECT * FROM subjects WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()
    return render_template("edit_subject.html", subject=subject)

# ---------------- SUBJECT PAGE ----------------
@app.route("/student/subjects")
def subjects_page():

    if "student_id" not in session:
        return redirect(url_for("login"))
    
    resp = require_student()
    if resp: return resp
    
    conn = get_db_connection()

    subjects = conn.execute(
        "SELECT * FROM subjects WHERE student_id=?",
        (session["student_id"],)
    ).fetchall()

    conn.close()

    return render_template("subjects.html", subjects=subjects)

# ---------------- FEES ----------------
@app.route("/student/fees")
def student_fees():

    if "student_id" not in session:
        return redirect(url_for("login"))
    
    resp = require_student()
    if resp: return resp
    
    conn = get_db_connection()

    fee = conn.execute(
        "SELECT * FROM fees WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    return render_template("fees.html", fee=fee)

# ---------------- DELETE SUBJECT ----------------
@app.route("/admin/delete-subject/<int:id>")
def delete_subject(id):

    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    conn.execute("DELETE FROM subjects WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin/subjects")

# ---------------- ADDITIONAL COURSES ----------------
@app.route("/courses")
def student_courses():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = get_db_connection()

    # available courses
    courses = conn.execute(
        "SELECT * FROM courses"
    ).fetchall()

    # enrolled courses
    enrolled_courses = conn.execute("""
        SELECT * FROM course_enrollments
        WHERE student_id = ?
    """, (student_id,)).fetchall()

    conn.close()

    return render_template(
        "courses.html",
        courses=courses,
        enrolled_courses=enrolled_courses
    )
# ---------------- ENROLL COURSE ----------------
@app.route("/course/enroll/<int:course_id>")
def enroll_course(course_id):

    if "student_id" not in session:
        return redirect(url_for("login"))
    
    student_id = session["student_id"]
    conn = get_db_connection()

    # check if already enrolled
    existing = conn.execute("""
        SELECT * FROM course_enrollments
        WHERE student_id=? AND course_id=?
    """, (student_id, course_id)).fetchone()

    if existing:
        conn.close()
        return redirect(url_for("student_courses"))

    conn.execute("""
        INSERT INTO course_enrollments (student_id, course_id, status)
        VALUES (?, ?, 'Enrolled')
    """, (student_id, course_id))
    
    conn.commit()
    conn.close()

    return redirect(url_for("student_courses"))
# ---------------- CANCEL COURSE ----------------
@app.route("/course/cancel/<int:course_id>")
def cancel_course(course_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM course_enrollments
        WHERE student_id=? AND course_id=?
    """, (session["student_id"], course_id))

    conn.commit()
    conn.close()

    return redirect(url_for("student_courses"))
# ---------------- DOWNLOAD CERTIFICATE ----------------
@app.route("/course/certificate/<int:course_id>")
def download_course_certificate(course_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    course = conn.execute("""
        SELECT courses.course_name, students.name
        FROM courses
        JOIN course_enrollments ON courses.id = course_enrollments.course_id
        JOIN students ON students.id = course_enrollments.student_id
        WHERE courses.id=? AND students.id=?
    """, (course_id, session["student_id"])).fetchone()

    conn.close()

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawCentredString(300, 700, "Certificate of Completion")

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(300, 650, f"This certifies that")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(300, 620, course["name"])

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(300, 590, f"has completed the course")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(300, 560, course["course_name"])

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="course_certificate.pdf",
        mimetype="application/pdf"
    )
    
# ---------------- HELP PAGE ----------------
@app.route("/student/help")
def student_help():

    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("help.html")

# ---------------- STUDENT MATERIAL ----------------

@app.route("/student/materials")
def student_materials():

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    materials = conn.execute(
        "SELECT * FROM study_materials"
    ).fetchall()

    conn.close()

    return render_template(
        "materials.html",
        materials=materials
    )
    
# ---------------- LIBRARY ----------------

@app.route("/student/library")
def student_library():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = get_db_connection()

    # available books
    books = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    # borrowed books
    borrowed_books = conn.execute("""
        SELECT book_issues.id, books.book_title, book_issues.issue_date,
               book_issues.due_date, book_issues.status
        FROM book_issues
        JOIN books ON book_issues.book_id = books.id
        WHERE book_issues.student_id = ?
    """,(student_id,)).fetchall()

    conn.close()

    return render_template(
        "library.html",
        books=books,
        borrowed_books=borrowed_books
    )
    
# ---------------- BORROW BOOK ----------------

@app.route("/borrow_book/<int:book_id>")
def borrow_book(book_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = get_db_connection()

    book = conn.execute(
        "SELECT available_copies FROM books WHERE id=?",
        (book_id,)
    ).fetchone()

    if book and book["available_copies"] > 0:

        conn.execute("""
        INSERT INTO book_issues (student_id, book_id, due_date)
        VALUES (?, ?, date('now','+7 day'))
        """,(student_id, book_id))

        conn.execute("""
        UPDATE books
        SET available_copies = available_copies - 1
        WHERE id=?
        """,(book_id,))

        conn.commit()

    conn.close()

    return redirect(url_for("student_library"))
    
# ---------------- RETURN BOOK ----------------

@app.route("/return_book/<int:issue_id>")
def return_book(issue_id):

    conn = get_db_connection()

    issue = conn.execute(
        "SELECT book_id FROM book_issues WHERE id=?",
        (issue_id,)
    ).fetchone()

    conn.execute("""
    UPDATE book_issues
    SET status='Returned'
    WHERE id=?
    """,(issue_id,))

    conn.execute("""
    UPDATE books
    SET available_copies = available_copies + 1
    WHERE id=?
    """,(issue["book_id"],))

    conn.commit()
    conn.close()

    return redirect(url_for("student_library"))

# ---------------- TEST ----------------
@app.route("/test")
def test():
    return "Flask is working"

# ---------------- CALENDAR ----------------

@app.route("/student/calendar")
def student_calendar():

    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    events = conn.execute(
        "SELECT * FROM calendar_events ORDER BY event_date"
    ).fetchall()

    conn.close()

    return render_template(
        "calendar.html",
        events=events
    )
    
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- TEST DB ----------------
@app.route("/test-db")
def test_db():
    conn = get_db_connection()

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    output = []

    for table in tables:
        table_name = table["name"]

        columns = conn.execute(
            f"PRAGMA table_info({table_name});"
        ).fetchall()

        col_names = [col["name"] for col in columns]

        output.append(f"{table_name} → {col_names}")

    conn.close()
    return "<br>".join(output)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)