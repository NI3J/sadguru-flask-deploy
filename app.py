import os
import io
import csv
import random
import hashlib
import requests
from datetime import date
from flask import Flask, render_template, request, redirect, flash, session, make_response, url_for
from flask_mail import Mail, Message
from db_config import get_db_connection
import datetime
app = Flask(__name__, static_folder='static')  # Define it once with static folder

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path="database.env")

app.config['MYSQL_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
# Secret key setup
app.secret_key = os.environ.get("superStrongAndUniqueKey123!@#", "dev_secret_key")

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.environ.get("jadhavnitin75@gmail.com"),
    MAIL_PASSWORD=os.environ.get("fnvd ekzc ooxp roor"),
    MAIL_DEFAULT_SENDER=os.environ.get("jadhavnitin75@gmail.com")
)

mail = Mail(app)

# 🔗 DB Config Import
from db_config import get_db_connection

# 🌼 Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM daily_programs ORDER BY date DESC")
    programs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('about.html', programs=programs)

# 🙏 Bhaktgan Registration
@app.route('/bhaktgan', methods=['GET', 'POST'])
def bhaktgan():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        seva_interest = request.form['seva_interest']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bhaktgan WHERE name=%s AND email=%s", (name, email))

        if cursor.fetchone()[0] > 0:
            message = "🌸 You're already part of the Bhaktgan."
        else:
            cursor.execute(
                "INSERT INTO bhaktgan (name, email, phone, seva_interest, city) VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, seva_interest, city)
            )
            conn.commit()
            message = "🕉️ Thank you for joining the Bhaktgan!"

            msg = Message(
                subject="🌸 Welcome to Bhaktgan",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                html=render_template('bhaktgan_welcome.html', name=name, seva=seva_interest)
            )
            mail.send(msg)

        conn.close()
        return render_template('bhaktgan.html', message=message)

    return render_template('bhaktgan.html')

# 📖 Wisdom Feed
@app.route('/wisdom')
def wisdom_feed():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM sadguru_thoughts")
        total = cursor.fetchone()[0]

        today = date.today().isoformat()
        index = int(hashlib.sha256(today.encode()).hexdigest(), 16) % total

        cursor.execute("SELECT content FROM sadguru_thoughts LIMIT 1 OFFSET %s", (index,))
        thought = cursor.fetchone()[0]

        conn.close()
        return render_template('wisdom.html', quotes=[(thought,)])

    except Exception as e:
        print("❌ Error loading wisdom:", e)
        return "🧘 Unable to load Sadguru's thought today."

# 🔢 OTP Generator
def generate_otp():
    return str(random.randint(100000, 999999))

# 📲 Send OTP via Fast2SMS
def send_sms(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": "08J7CR3Syh2YmZLbsAWQUfTcNI9aveEOGBlziVjqwKtpF54MDglWCZbSdV8GkAHKPBrFamI35eOy6MQE",  # Replace with yours securely
        "Content-Type": "application/json"
    }
    payload = {
        "route": "otp",
        "variables_values": otp,
        "numbers": mobile
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("📲 SMS API Response:", response.text)
    except Exception as e:
        print("❌ Failed to send OTP:", e)

# 🔐 OTP Request
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    username = request.form['username']
    mobile = request.form['mobile']
    otp = generate_otp()
    session['otp'] = otp
    session['username'] = username
    send_sms(mobile, otp)
    return render_template('enter_otp.html', username=username)

# 🔓 OTP Validation
@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    entered_otp = request.form['otp']
    actual_otp = session.get('otp')
    username = session.get('username')
    if entered_otp == actual_otp:
        return render_template('wisdom_access_granted.html', username=username)
    else:
        flash("❌ OTP चुकीचा आहे.")
        return redirect('/retry-otp')

@app.route('/retry-otp')
def retry_otp():
    username = session.get('username', 'भक्त')
    return render_template('enter_otp.html', username=username)

# 📬 Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message_content = request.form['message']

        if email:
            reply_html = render_template('contact_autoreply.html', name=name, message=message_content)
            msg = Message(
                subject="आपला संदेश प्राप्त झाला आहे 🙏",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                html=reply_html
            )
            mail.send(msg)

        return render_template('contact.html', success=True)

    return render_template('contact.html')

# 📊 Admin Dashboard
@app.route('/admin/bhaktgan')
def bhaktgan_dashboard():
    seva_filter = request.args.get('seva')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if seva_filter:
        cursor.execute("SELECT * FROM bhaktgan WHERE seva_interest = %s ORDER BY submitted_at DESC", (seva_filter,))
    else:
        cursor.execute("SELECT * FROM bhaktgan ORDER BY submitted_at DESC")

    bhaktgan_list = cursor.fetchall()
    conn.close()
    return render_template('admin/bhaktgan_dashboard.html', bhaktgan_list=bhaktgan_list, current_seva=seva_filter)

# 📁 Export CSV
@app.route('/admin/bhaktgan/export')
def export_bhaktgan_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, phone, seva_interest, city, submitted_at FROM bhaktgan")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['नाव', 'ईमेल', 'फोन', 'सेवा', 'शहर', 'नोंदणी वेळ'])
    for row in rows:
        writer.writerow(row)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=bhaktgan_suchi.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# 🧘 Thoughts Manager
@app.route('/admin/thoughts', methods=['GET', 'POST'])
def manage_thoughts():
    if request.method == 'POST':
        new_thought = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sadguru_thoughts (content) VALUES (%s)", (new_thought,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("🙏 Thought added successfully.")
    return render_template('admin_thoughts.html')

@app.route('/wisdom/archive')
def archive():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT content, added_on FROM sadguru_thoughts ORDER BY added_on DESC")
    thoughts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('wisdom_archive.html', thoughts=thoughts)

@app.route('/fast2sms_verify.txt')
def fast2sms_file():
    return app.send_static_file('fast2sms_verify.txt')

# 📽️ Katha Page
@app.route('/katha')
def katha():
    video_path = os.path.join(app.static_folder, 'videos/sadguru_katha.mp4')
    video_exists = os.path.exists(video_path)
    return render_template('katha.html', video_exists=video_exists)


# 📝 Submit Daily Program



def normalize(phone):
    # Clean up phone format (strip spaces, country code, leading zeros)
    return phone.strip().replace('+91', '').lstrip('0')

from flask import request, session, render_template
import mysql.connector

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    show_submission_form = False

    try:
        # Connect to DB
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 🔄 Case 1: Form submitted with name and mobile
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            mobile = normalize(request.form.get('mobile', ''))

            # Query DB for matching admin
            cursor.execute(
                "SELECT * FROM authorized_admins WHERE name = %s AND phone = %s",
                (name, mobile)
            )
            admin = cursor.fetchone()

            if admin:
                # ✅ Set session if valid
                session['admin_phone'] = mobile
                session['admin_name'] = name
                show_submission_form = True

        # 🔄 Case 2: Already in session, revalidate
        elif 'admin_phone' in session and 'admin_name' in session:
            cursor.execute(
                "SELECT * FROM authorized_admins WHERE name = %s AND phone = %s",
                (session['admin_name'], session['admin_phone'])
            )
            admin = cursor.fetchone()
            show_submission_form = bool(admin)

    except mysql.connector.Error as err:
        print("❌ DB Error:", err)

    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass

    return render_template("admin_dashboard.html", show_submission_form=show_submission_form)

from flask import render_template
import datetime
from collections import defaultdict

@app.route('/programs')
def programs():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT date, content FROM daily_programs ORDER BY date DESC")
        records = cursor.fetchall()
    except Exception as err:
        print("❌ Error fetching programs:", err)
        records = []

    finally:
        cursor.close()
        connection.close()

    # Group programs by date
    grouped_days = defaultdict(list)
    for entry in records:
        grouped_days[entry['date']].append(entry['content'])

    # Prepare list for template
    days = [{'date': date, 'programs': entries} for date, entries in grouped_days.items()]
    today = datetime.date.today().strftime('%Y-%m-%d')

    return render_template('program/program.html', days=days, today=today)

@app.route('/submit_program', methods=['POST'])
def submit_program():
    date = request.form.get('date')
    content = request.form.get('content')
    created_by = session.get('admin_name')  # or session.get('admin_phone')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO daily_programs (date, content, created_by) VALUES (%s, %s, %s)",
            (date, content, created_by)
        )
        connection.commit()

    except mysql.connector.Error as err:
        print("❌ Database error:", err)

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('programs'))  # redirect to the route displaying programs

# 🚀 Launch Server
if __name__ == '__main__':
    print("🕉️ Spiritual Flask app launching...")
    app.run(debug=True, host='0.0.0.0', port=5000)
