# 🎓 Smart College ERP System

A full-stack **Student ERP (Enterprise Resource Planning) System** designed to manage academic and administrative activities within a college.
The system supports **role-based access** for Admin, Faculty, and Students with modules like grievances, notifications, admissions, and events.

---

## 🚀 Features

### 👨‍💼 Admin Panel

* Manage student & faculty data
* View and resolve grievances
* Send notifications to users
* Manage events & notices
* Access college calendar

### 👩‍🎓 Student Panel

* Login securely
* Submit grievances
* View grievance status & admin replies
* Receive notifications
* Access academic information

### 👨‍🏫 Faculty Panel

* Login system
* Manage student-related data
* Interact with grievances (if applicable)

### 📌 Core Modules

* 🔐 Role-based Authentication (Admin / Student / Faculty)
* 📝 Grievance Management System
* 🔔 Notification System
* 📅 College Calendar
* 📢 Events & Notices
* 🎓 Admission Module

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python (Flask)

### Database

* SQLite3

### Tools & Libraries

* Jinja2 (Templating)
* Werkzeug (Authentication & Security)
* Flask Sessions

---

## 📂 Project Structure

```
student_erp/
│
├── static/              # CSS, images, uploads
│   ├── css/
│   └── uploads/
│
├── templates/           # HTML Templates (Jinja2)
│   ├── admin/
│   ├── student/
│   ├── faculty/
│
├── app.py               # Main Flask application
├── database.db          # SQLite database
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/smart-college-erp-system.git
cd smart-college-erp-system
```

### 2️⃣ Create Virtual Environment (optional but recommended)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```
pip install flask
pip install werkzeug
```

### 4️⃣ Run the Application

```
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔐 Default Roles (Example)

| Role    | Access                 |
| ------- | ---------------------- |
| Admin   | Full control           |
| Student | Submit/view grievances |
| Faculty | Academic interaction   |

---

## 📸 Screenshots (Add your UI images here)

* Landing Page
* Login Page
* Admin Dashboard
* Grievance Module

---

## 🎯 Future Improvements

* 📊 Dashboard analytics & charts
* 📧 Email notifications
* 📱 Responsive mobile design
* ⚛️ Upgrade to React frontend
* ☁️ Deployment (AWS / Render / Railway)

---

## 🤝 Contribution

Contributions are welcome!
Feel free to fork this repository and submit a pull request.

---

## 📄 License

This project is for educational purposes.

---

## 👩‍💻 Author

**Sakshi Sinha**
B.Tech CSE Student

---

⭐ If you like this project, don’t forget to star the repo!
