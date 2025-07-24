from flask import Flask, render_template, request
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)

# 📧 Email Configuration
app.config.update(
    MAIL_SERVER='smtp.yourprovider.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='jadhavnitin75@email.com',
    MAIL_PASSWORD='Pallu@143'
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

# 🙏 Devotional Community (Bhaktgan)
@app.route('/bhaktgan', methods=['GET', 'POST'])
def bhaktgan():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        seva = request.form['seva_interest']

        conn = mysql.connector.connect(
            user='spiritual_user',
            password='Mybabaji@143',
            database='spiritual_db'
        )
        cursor = conn.cursor()

        # Check for duplicates
        cursor.execute("SELECT COUNT(*) FROM bhaktgan WHERE name=%s AND email=%s", (name, email))
        if cursor.fetchone()[0] > 0:
            message = "🌸 You're already part of the Bhaktgan. No need to register again!"
        else:
            cursor.execute(
                "INSERT INTO bhaktgan (name, email, seva_interest) VALUES (%s, %s, %s)",
                (name, email, seva)
            )
            conn.commit()
            message = "🕉️ Thank you for joining the Bhaktgan!"

            # ✉️ Send email confirmation
            msg = Message(
                subject="🌸 Welcome to Bhaktgan",
                sender='jadhavnitin75@email.com',
                recipients=[email]
            )
            msg.html = f"""
            <html>
              <body style="font-family: Georgia, serif; background:#f8f4e3; padding:20px; color:#5c3d00;">
                <h2>Welcome to the Bhaktgan Community 🌿</h2>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Your seva intention has been received:</p>
                <blockquote>{seva}</blockquote>
                <p>May your path be guided with peace and light.</p>
                <p>🕉️ Spiritual Website Team</p>
              </body>
            </html>
            """
            mail.send(msg)

        conn.close()
        return render_template('bhaktgan.html', message=message)

    return render_template('bhaktgan.html')

# 📖 Wisdom Teachings
@app.route('/wisdom')
def wisdom_feed():
    conn = mysql.connector.connect(
        user='spiritual_user',
        password='Mybabaji@143',
        database='spiritual_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT quote, author FROM wisdom_quotes")
    quotes = cursor.fetchall()
    conn.close()
    return render_template('wisdom.html', quotes=quotes)

# 📬 Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 🚀 Launch the server
if __name__ == '__main__':
    print("🕉️ Spiritual Flask app launching...")
    app.run(debug=True, host='0.0.0.0', port=5000)
