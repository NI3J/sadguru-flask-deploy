import os
import io
import csv
import random
import requests
from datetime import date
from flask import Flask, render_template, request, redirect, flash, session, make_response
from flask_mail import Mail, Message
import mysql.connector

# 🔐 Flask App Setup
app = Flask(__name__)
app.secret_key = os.environ.get('superStrongAndUniqueKey123!@#', 'dev_secret_key')

# 📧 Email Configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.environ.get('jadhavnitin75@gmail.com'),
    MAIL_PASSWORD=os.environ.get('ystg xbox peao vpfn')
)
mail = Mail(app)

# 🌼 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 🧘 About Page
@app.route('/about')
def about():
    return render_template('about.html')

# 📅 Programs & Events
@app.route('/programs')
def programs():
    return render_template('programs.html')

# 🙏 Bhaktgan Registration
@app.route('/bhaktgan', methods=['GET', 'POST'])
def bhaktgan():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        seva_interest = request.form['seva_interest']

        conn = mysql.connector.connect(user='spiritual_user', password='Mybabaji@143', database='spiritual_db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM bhaktgan WHERE name=%s AND email=%s", (name, email))
        if cursor.fetchone()[0] > 0:
            message = "🌸 You're already part of the Bhaktgan."
        else:
            cursor.execute("INSERT INTO bhaktgan (name, email, phone, seva_interest, city) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, phone, seva_interest, city))
            conn.commit()
            message = "🕉️ Thank you for joining the Bhaktgan!"

            msg = Message(
                subject="🌸 Welcome to Bhaktgan",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                html=render_template('email_templates/bhaktgan_welcome.html', name=name, seva=seva_interest)
            )
            mail.send(msg)

        conn.close()
        return render_template('bhaktgan.html', message=message)

    return render_template('bhaktgan.html')


# 📖 Wisdom Teachings
from datetime import date
import hashlib

@app.route('/wisdom')
def wisdom_feed():
    try:
        conn = mysql.connector.connect(
            user='spiritual_user',
            password='Mybabaji@143',
            database='spiritual_db'
        )
        cursor = conn.cursor()

        # 🔢 Get total number of thoughts
        cursor.execute("SELECT COUNT(*) FROM sadguru_thoughts")
        total = cursor.fetchone()[0]

        # 📅 Use today's date to generate a consistent index
        today = date.today().isoformat()
        index = int(hashlib.sha256(today.encode()).hexdigest(), 16) % total

        # 🎯 Fetch one thought using OFFSET
        cursor.execute(f"SELECT content FROM sadguru_thoughts LIMIT 1 OFFSET {index}")
        thought = cursor.fetchone()[0]

        conn.close()
        return render_template('wisdom.html', quotes=[(thought,)])

    except Exception as e:
        print(f"Error loading daily thought: {e}")
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
    conn = mysql.connector.connect(user='spiritual_user', password='Mybabaji@143', database='spiritual_db')
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
    conn = mysql.connector.connect(user='spiritual_user', password='Mybabaji@143', database='spiritual_db')
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

# 🧘 Manage Thoughts
@app.route('/admin/thoughts', methods=['GET', 'POST'])
def manage_thoughts():
    if request.method == 'POST':
        new_thought = request.form['content']
        conn = mysql.connector.connect(user='spiritual_user', password='Mybabaji@143', database='spiritual_db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sadguru_thoughts (content) VALUES (%s)", (new_thought,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("🙏 Thought added successfully.")
    return render_template('admin_thoughts.html')

# 📚 Thought Archive
@app.route('/wisdom/archive')
def archive():
    conn = mysql.connector.connect(user='spiritual_user', password='Mybabaji@143', database='spiritual_db')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT content, added_on FROM sadguru_thoughts ORDER BY added_on DESC")
    thoughts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('wisdom_archive.html', thoughts=thoughts)

@app.route('/fast2sms_verify.txt')
def fast2sms_file():
    return app.send_static_file('fast2sms_verify.txt')

# 🚀 Launch Server
if __name__ == '__main__':
    print("🕉️ Spiritual Flask app launching...")
    app.run(debug=True, host='0.0.0.0', port=5000)