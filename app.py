# app.py - Flask backend with visitor count, form submission, database storage, and secure email using .env

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'submissions.db')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for contact form submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

# Visitor count storage
def get_visitor_count():
    try:
        with open("counter.txt", "r") as f:
            count = int(f.read().strip())
    except:
        count = 0
    return count

def increase_visitor_count():
    count = get_visitor_count() + 1
    with open("counter.txt", "w") as f:
        f.write(str(count))
    return count

# Send email function
def send_email(name, email, message):
    sender = os.getenv("MY_EMAIL")
    receiver = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("MY_EMAIL_PASS")

    msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = "New Portfolio Contact"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    count = increase_visitor_count()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        new_submission = Submission(name=name, email=email, message=message)
        db.session.add(new_submission)
        db.session.commit()

        send_email(name, email, message)

        return redirect("/")
    return render_template("index.html", count=count)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)











'''
 # app.py - Flask backend with visitor count, form submission, and database storage

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for contact form submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

# Visitor count storage
def get_visitor_count():
    try:
        with open("counter.txt", "r") as f:
            count = int(f.read().strip())
    except:
        count = 0
    return count

def increase_visitor_count():
    count = get_visitor_count() + 1
    with open("counter.txt", "w") as f:
        f.write(str(count))
    return count

# Send email function
def send_email(name, email, message):
    sender = "youremail@example.com"  # Replace with real sender
    receiver = "yourinbox@example.com"  # Replace with real receiver
    password = "yourpassword"  # Replace with real password or app password

    msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = "New Portfolio Contact"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Email failed:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    count = increase_visitor_count()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        new_submission = Submission(name=name, email=email, message=message)
        db.session.add(new_submission)
        db.session.commit()

        send_email(name, email, message)

        return redirect("/")
    return render_template("index.html", count=count)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

'''