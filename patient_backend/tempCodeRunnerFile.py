from flask import Flask, request, redirect, session, jsonify, flash
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import secrets
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
bcrypt = Bcrypt(app)

# -------------------------------------------------
# DATABASE CONNECTION WITH ERROR HANDLING
# -------------------------------------------------
def get_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jinay",
            database="patient_system",
            autocommit=False
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# -------------------------------------------------
# LOGIN REQUIRED DECORATOR
# -------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------
# HTML TEMPLATE WITH IMPROVED STYLING
# -------------------------------------------------
def render_page(title, body, show_nav=True):
    nav_html = ""
    if show_nav and 'user' in session:
        nav_html = """
        <div class="nav">
            <div class="nav-container">
                <b>🏥 Patient Healthcare System</b>
                <div class="nav-links">
                    <a href='/dashboard'>📊 Dashboard</a>
                    <a href='/history'>📋 Medical History</a>
                    <a href='/appointments'>📅 Appointments</a>
                    <a href='/profile'>👤 Profile</a>
                    <a href='/logout'>🚪 Logout</a>
                </div>
            </div>
        </div>
        """
    elif show_nav:
        nav_html = """
        <div class="nav">
            <div class="nav-container">
                <b>🏥 Patient Healthcare System</b>
            </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .nav {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .nav-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }}
            .nav-links {{
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }}
            .nav a {{
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}
            .nav a:hover {{
                background-color: rgba(255,255,255,0.2);
                transform: translateY(-2px);
            }}
            .container {{
                max-width: 1200px;
                margin: 30px auto;
                padding: 0 20px;
            }}
            .card {{
                background: white;
                padding: 30px;
                margin-bottom: 25px;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.15);
            }}
            .card h2, .card h3 {{
                color: #1e3c72;
                margin-bottom: 20px;
            }}
            input, textarea, select {{
                width: 100%;
                padding: 12px;
                margin-top: 8px;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }}
            input:focus, textarea:focus, select:focus {{
                outline: none;
                border-color: #667eea;
            }}
            button {{
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
            }}
            button:active {{
                transform: translateY(0);
            }}
            .error {{
                color: #dc2626;
                background-color: #fee2e2;
                padding: 10px;
                border-radius: 6px;
                margin-top: 10px;
            }}
            .success {{
                color: #059669;
                background-color: #d1fae5;
                padding: 10px;
                border-radius: 6px;
                margin-top: 10px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}
            .info-item {{
                padding: 15px;
                background-color: #f8fafc;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .info-item strong {{
                color: #1e3c72;
                display: block;
                margin-bottom: 5px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
            }}
            .stat-card h3 {{
                color: white;
                font-size: 32px;
                margin: 10px 0;
            }}
            .stat-card p {{
                opacity: 0.9;
            }}
            .btn-secondary {{
                background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            .form-group label {{
                display: block;
                color: #374151;
                font-weight: 600;
                margin-bottom: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}
            th {{
                background-color: #f8fafc;
                color: #1e3c72;
                font-weight: 600;
            }}
            tr:hover {{
                background-color: #f8fafc;
            }}
            @media (max-width: 768px) {{
                .nav-container {{
                    flex-direction: column;
                    gap: 15px;
                }}
                .nav-links {{
                    justify-content: center;
                }}
            }}
        </style>
    </head>
    <body>
        {nav_html}
        <div class="container">
            {body}
        </div>
    </body>
    </html>
    """

# -------------------------------------------------
# LOGIN & REGISTRATION
# -------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect("/dashboard")
    
    error = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            error = "Email and password are required"
        else:
            db = get_db()
            if db is None:
                error = "Database connection failed. Please try again later."
            else:
                try:
                    cur = db.cursor(dictionary=True)
                    cur.execute(
                        "SELECT * FROM patients WHERE email=%s",
                        (email,)
                    )
                    user = cur.fetchone()
                    
                    if user and bcrypt.check_password_hash(user['password'], password):
                        session.permanent = True
                        session["user"] = email
                        session["name"] = user['name']
                        return redirect("/dashboard")
                    else:
                        error = "Invalid email or password"
                except Error as e:
                    error = f"Login error: {str(e)}"
                finally:
                    cur.close()
                    db.close()

    return render_page("Login", f"""
        <div class="card" style="max-width: 500px; margin: 50px auto;">
            <h2>🔐 Patient Login</h2>
            <form method="post">
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" placeholder="Enter your email" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter your password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            {f'<p class="error">{error}</p>' if error else ''}
            <div style="margin-top: 20px; padding: 15px; background-color: #f0fdf4; border-radius: 8px;">
                <p><b>🔑 Demo Login:</b></p>
                <p>Email: amit@gmail.com</p>
                <p>Password: 1234</p>
            </div>
            <div style="margin-top: 15px; text-align: center;">
                <a href="/register" style="color: #667eea; text-decoration: none; font-weight: 600;">
                    Don't have an account? Register here
                </a>
            </div>
        </div>
    """, show_nav=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    success = ""
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "")
        phone = request.form.get("phone", "").strip()
        
        if not all([name, email, password, age, gender, phone]):
            error = "All fields are required"
        else:
            db = get_db()
            if db is None:
                error = "Database connection failed"
            else:
                try:
                    cur = db.cursor(dictionary=True)
                    cur.execute("SELECT * FROM patients WHERE email=%s", (email,))
                    if cur.fetchone():
                        error = "Email already registered"
                    else:
                        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                        cur.execute(
                            """INSERT INTO patients (name, email, password, age, gender, phone)
                               VALUES (%s, %s, %s, %s, %s, %s)""",
                            (name, email, hashed_password, age, gender, phone)
                        )
                        db.commit()
                        success = "Registration successful! Please login."
                except Error as e:
                    error = f"Registration error: {str(e)}"
                finally:
                    cur.close()
                    db.close()
    
    return render_page("Register", f"""
        <div class="card" style="max-width: 600px; margin: 50px auto;">
            <h2>📝 Patient Registration</h2>
            <form method="post">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" name="age" min="1" max="120" required>
                </div>
                <div class="form-group">
                    <label>Gender</label>
                    <select name="gender" required>
                        <option value="">Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="tel" name="phone" required>
                </div>
                <button type="submit">Register</button>
            </form>
            {f'<p class="error">{error}</p>' if error else ''}
            {f'<p class="success">{success}</p>' if success else ''}
            <div style="margin-top: 15px; text-align: center;">
                <a href="/" style="color: #667eea; text-decoration: none; font-weight: 600;">
                    Already have an account? Login here
                </a>
            </div>
        </div>
    """, show_nav=False)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    if db is None:
        return render_page("Error", '<div class="card"><p class="error">Database connection failed</p></div>')
    
    try:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM patients WHERE email=%s", (session["user"],))
        patient = cur.fetchone()
        
        if not patient:
            session.clear()
            return redirect("/")
        
        # Get statistics
        cur.execute("SELECT COUNT(*) as count FROM medical_history WHERE patient_email=%s", (session["user"],))
        history_count = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM appointments WHERE patient_email=%s", (session["user"],))
        appointment_count = cur.fetchone()['count']
        
        # Get recent medical records
        cur.execute(
            "SELECT * FROM medical_history WHERE patient_email=%s ORDER BY visit_date DESC LIMIT 3",
            (session["user"],)
        )
        recent_records = cur.fetchall()
        
        recent_html = ""
        for r in recent_records:
            recent_html += f"""
            <div class="info-item">
                <strong>📅 {r['visit_date']}</strong>
                <p><b>Doctor:</b> Dr. {r['doctor']}</p>
                <p><b>Diagnosis:</b> {r['diagnosis']}</p>
            </div>
            """
        
        return render_page("Dashboard", f"""
            <h2>Welcome, {patient['name']}! 👋</h2>
            
            <div class="stats">
                <div class="stat-card">
                    <p>Medical Records</p>
                    <h3>{history_count}</h3>
                </div>
                <div class="stat-card">
                    <p>Appointments</p>
                    <h3>{appointment_count}</h3>
                </div>
                <div class="stat-card">
                    <p>Account Age</p>
                    <h3>{patient['age']}</h3>
                </div>
            </div>
            
            <div class="card">
                <h3>👤 Your Profile</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Full Name</strong>
                        <p>{patient['name']}</p>
                    </div>
                    <div class="info-item">
                        <strong>Age</strong>
                        <p>{patient['age']} years</p>
                    </div>
                    <div class="info-item">
                        <strong>Gender</strong>
                        <p>{patient['gender']}</p>
                    </div>
                    <div class="info-item">
                        <strong>Phone</strong>
                        <p>{patient['phone']}</p>
                    </div>
                    <div class="info-item">
                        <strong>Email</strong>
                        <p>{patient['email']}</p>
                    </div>
                </div>
            </div>
            
            {f'''
            <div class="card">
                <h3>📋 Recent Medical Records</h3>
                <div class="info-grid">
                    {recent_html}
                </div>
            </div>
            ''' if recent_records else ''}
        """)
    except Error as e:
        return render_page("Error", f'<div class="card"><p class="error">Error: {str(e)}</p></div>')
    finally:
        cur.close()
        db.close()

# -------------------------------------------------
# MEDICAL HISTORY
# -------------------------------------------------
@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    db = get_db()
    if db is None:
        return render_page("Error", '<div class="card"><p class="error">Database connection failed</p></div>')
    
    message = ""
    try:
        cur = db.cursor(dictionary=True)

        if request.method == "POST":
            try:
                cur.execute(
                    """INSERT INTO medical_history
                       (patient_email, visit_date, doctor, diagnosis, treatment)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (
                        session["user"],
                        request.form.get("date"),
                        request.form.get("doctor"),
                        request.form.get("diagnosis"),
                        request.form.get("treatment")
                    )
                )
                db.commit()
                message = '<p class="success">✅ Medical record added successfully!</p>'
            except Error as e:
                message = f'<p class="error">Error adding record: {str(e)}</p>'

        cur.execute(
            "SELECT * FROM medical_history WHERE patient_email=%s ORDER BY visit_date DESC",
            (session["user"],)
        )
        records = cur.fetchall()

        if records:
            rows = "<table><thead><tr><th>Date</th><th>Doctor</th><th>Diagnosis</th><th>Treatment</th></tr></thead><tbody>"
            for r in records:
                rows += f"""
                <tr>
                    <td>{r['visit_date']}</td>
                    <td>Dr. {r['doctor']}</td>
                    <td>{r['diagnosis']}</td>
                    <td>{r['treatment']}</td>
                </tr>
                """
            rows += "</tbody></table>"
        else:
            rows = '<p style="text-align: center; color: #64748b; padding: 20px;">No medical records found. Add your first record below!</p>'

        return render_page("Medical History", f"""
            <h2>📋 Medical History</h2>
            {message}
            <div class="card">
                {rows}
            </div>
            <div class="card">
                <h3>➕ Add Medical Record</h3>
                <form method="post">
                    <div class="form-group">
                        <label>Visit Date</label>
                        <input type="date" name="date" max="{datetime.now().strftime('%Y-%m-%d')}" required>
                    </div>
                    <div class="form-group">
                        <label>Doctor Name</label>
                        <input name="doctor" placeholder="e.g., Smith" required>
                    </div>
                    <div class="form-group">
                        <label>Diagnosis</label>
                        <textarea name="diagnosis" rows="3" placeholder="Enter diagnosis details" required></textarea>
                    </div>
                    <div class="form-group">
                        <label>Treatment</label>
                        <textarea name="treatment" rows="3" placeholder="Enter treatment details" required></textarea>
                    </div>
                    <button type="submit">Add Record</button>
                </form>
            </div>
        """)
    except Error as e:
        return render_page("Error", f'<div class="card"><p class="error">Error: {str(e)}</p></div>')
    finally:
        cur.close()
        db.close()

# -------------------------------------------------
# APPOINTMENTS
# -------------------------------------------------
@app.route("/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    db = get_db()
    if db is None:
        return render_page("Error", '<div class="card"><p class="error">Database connection failed</p></div>')
    
    message = ""
    try:
        cur = db.cursor(dictionary=True)

        if request.method == "POST":
            try:
                cur.execute(
                    """INSERT INTO appointments
                       (patient_email, appointment_date, doctor, department, notes)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (
                        session["user"],
                        request.form.get("date"),
                        request.form.get("doctor"),
                        request.form.get("department"),
                        request.form.get("notes")
                    )
                )
                db.commit()
                message = '<p class="success">✅ Appointment booked successfully!</p>'
            except Error as e:
                message = f'<p class="error">Error booking appointment: {str(e)}</p>'

        cur.execute(
            "SELECT * FROM appointments WHERE patient_email=%s ORDER BY appointment_date DESC",
            (session["user"],)
        )
        appointments = cur.fetchall()

        if appointments:
            rows = "<table><thead><tr><th>Date</th><th>Doctor</th><th>Department</th><th>Notes</th><th>Status</th></tr></thead><tbody>"
            for apt in appointments:
                status_color = "#059669" if apt.get('status', 'Pending') == 'Confirmed' else "#f59e0b"
                rows += f"""
                <tr>
                    <td>{apt['appointment_date']}</td>
                    <td>Dr. {apt['doctor']}</td>
                    <td>{apt['department']}</td>
                    <td>{apt['notes']}</td>
                    <td style="color: {status_color}; font-weight: 600;">{apt.get('status', 'Pending')}</td>
                </tr>
                """
            rows += "</tbody></table>"
        else:
            rows = '<p style="text-align: center; color: #64748b; padding: 20px;">No appointments scheduled. Book your first appointment below!</p>'

        return render_page("Appointments", f"""
            <h2>📅 Appointments</h2>
            {message}
            <div class="card">
                {rows}
            </div>
            <div class="card">
                <h3>📝 Book New Appointment</h3>
                <form method="post">
                    <div class="form-group">
                        <label>Appointment Date</label>
                        <input type="datetime-local" name="date" min="{datetime.now().strftime('%Y-%m-%dT%H:%M')}" required>
                    </div>
                    <div class="form-group">
                        <label>Doctor Name</label>
                        <input name="doctor" placeholder="e.g., Johnson" required>
                    </div>
                    <div class="form-group">
                        <label>Department</label>
                        <select name="department" required>
                            <option value="">Select Department</option>
                            <option value="Cardiology">Cardiology</option>
                            <option value="Neurology">Neurology</option>
                            <option value="Orthopedics">Orthopedics</option>
                            <option value="Pediatrics">Pediatrics</option>
                            <option value="General Medicine">General Medicine</option>
                            <option value="Dermatology">Dermatology</option>
                            <option value="ENT">ENT</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Notes</label>
                        <textarea name="notes" rows="3" placeholder="Any special requirements or notes"></textarea>
                    </div>
                    <button type="submit">Book Appointment</button>
                </form>
            </div>
        """)
    except Error as e:
        return render_page("Error", f'<div class="card"><p class="error">Error: {str(e)}</p></div>')
    finally:
        cur.close()
        db.close()

# -------------------------------------------------
# PROFILE
# -------------------------------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db = get_db()
    if db is None:
        return render_page("Error", '<div class="card"><p class="error">Database connection failed</p></div>')
    
    message = ""
    try:
        cur = db.cursor(dictionary=True)
        
        if request.method == "POST":
            try:
                cur.execute(
                    """UPDATE patients SET name=%s, age=%s, gender=%s, phone=%s
                       WHERE email=%s""",
                    (
                        request.form.get("name"),
                        request.form.get("age"),
                        request.form.get("gender"),
                        request.form.get("phone"),
                        session["user"]
                    )
                )
                db.commit()
                session["name"] = request.form.get("name")
                message = '<p class="success">✅ Profile updated successfully!</p>'
            except Error as e:
                message = f'<p class="error">Error updating profile: {str(e)}</p>'
        
        cur.execute("SELECT * FROM patients WHERE email=%s", (session["user"],))
        patient = cur.fetchone()
        
        return render_page("Profile", f"""
            <h2>👤 Your Profile</h2>
            {message}
            <div class="card">
                <form method="post">
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" name="name" value="{patient['name']}" required>
                    </div>
                    <div class="form-group">
                        <label>Age</label>
                        <input type="number" name="age" value="{patient['age']}" min="1" max="120" required>
                    </div>
                    <div class="form-group">
                        <label>Gender</label>
                        <select name="gender" required>
                            <option value="Male" {"selected" if patient['gender'] == 'Male' else ''}>Male</option>
                            <option value="Female" {"selected" if patient['gender'] == 'Female' else ''}>Female</option>
                            <option value="Other" {"selected" if patient['gender'] == 'Other' else ''}>Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Phone Number</label>
                        <input type="tel" name="phone" value="{patient['phone']}" required>
                    </div>
                    <div class="form-group">
                        <label>Email (cannot be changed)</label>
                        <input type="email" value="{patient['email']}" disabled>
                    </div>
                    <button type="submit">Update Profile</button>
                </form>
            </div>
        """)
    except Error as e:
        return render_page("Error", f'<div class="card"><p class="error">Error: {str(e)}</p></div>')
    finally:
        cur.close()
        db.close()

# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------------------------------------
# ERROR HANDLERS
# -------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_page("404 Not Found", '<div class="card"><h2>Page Not Found</h2><p>The page you are looking for does not exist.</p><a href="/dashboard">Go to Dashboard</a></div>'), 404

@app.errorhandler(500)
def server_error(e):
    return render_page("500 Server Error", '<div class="card"><h2>Server Error</h2><p>Something went wrong. Please try again later.</p></div>'), 500
def init_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jinay"
        )
        cur = conn.cursor()

        cur.execute("CREATE DATABASE IF NOT EXISTS patient_system")
        cur.execute("USE patient_system")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            age INT,
            gender VARCHAR(20),
            phone VARCHAR(20)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_email VARCHAR(100),
            visit_date DATE,
            doctor VARCHAR(100),
            diagnosis TEXT,
            treatment TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_email VARCHAR(100),
            appointment_date DATETIME,
            doctor VARCHAR(100),
            department VARCHAR(100),
            notes TEXT,
            status VARCHAR(50) DEFAULT 'Pending'
        )
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("✅ Database checked/created successfully")

    except Error as e:
        print("❌ Database init error:", e)

# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
# -------------------------------------------------
# RUN SERVER (WAITRESS – WINDOWS SAFE)
# -------------------------------------------------
from waitress import serve

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 Patient Healthcare System Starting...")
    print("=" * 60)

    init_database()

    print("📍 Server running at: http://127.0.0.1:8000")
    print("🔐 Demo Login - Email: amit@gmail.com | Password: 1234")
    print("=" * 60)

    serve(app, host="127.0.0.1", port=8000)

