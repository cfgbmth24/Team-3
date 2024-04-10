# create the Flask app
import re
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import os

from flask import make_response, render_template_string
from flask import session

app.secret_key="is nothing secret"

from werkzeug import security
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask import flash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

#Database manager

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///eventsite.sqlite'

from db_schema import db, User, Story, dbinit

db.init_app(app)

with app.app_context():
  dbinit()

#Login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#Mail manager

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = False  
app.config['MAIL_USERNAME'] = None 
app.config['MAIL_PASSWORD'] = None 
app.config['MAIL_SUPPRESS_SEND'] = False


from flask_mail import Mail, Message
from flask import Flask, request, redirect, url_for, render_template, flash
from itsdangerous import URLSafeTimedSerializer as safeURL

mail = Mail(app)

@app.route("/")
def index():
   return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

def valid_password(password):
    if len(password) < 8:
        return False
    
    if not re.search(r"[A-Z]", password):
        return False
    
    if not re.search(r"[a-z]", password):
        return False
    
    if not re.search(r"\d", password):
        return False
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True

def valid_email(email):
    if "@" in email:
        parts = email.split("@")
        if len(parts) == 2 and all(parts):
            return True
    return False

def valid_username(username):
    if re.match("^[a-zA-Z0-9_-]{3,20}$", username):
        return True
    else:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template("login.html")
    else:  # POST
        email = request.form.get('email')  # This would be the name attribute of the email input
        password = request.form.get('password')  # This would be the name attribute of the password input

        # Validate the presence of email and password
        if not email or not password:
            print("Hello")  # Assuming you want to keep the print statement for debugging
            return redirect(url_for('login'))

        # Try to fetch the user by email
        user = User.query.filter_by(email=email).first()

        if user is None:
            print("email")
            return redirect(url_for('login'))

        if not user.check_password(password):
            print("password")
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))


@app.get("/volunteer")
def volunteerGET():
    return render_template("volunteering.html")

@app.get('/signup')
def signupGET():
   if current_user.is_authenticated:
        return redirect('/')
   return render_template("signup.html")

@app.post('/signup')
def registerPOST():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    if email is None or password is None:
        return redirect('/signup')

    try:
        user_email = User.query.filter_by(email=email).first()
    except:
        return redirect('/signup')

    if user_email is not None:
        return redirect('/signup')
    
    if not valid_password(password) or not valid_email(email):
        return redirect('/signup')
    
    try:
        newUser = User(name, email, password)
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError as exc:
        db.session.roll
        db.session.rollback()
        return redirect('/signup')

    return redirect('/login')

def send_donation_email():
    recipients = [current_user.email]
    sender = "u2212705@dcs.warwick.ac.uk"
    confirm_url = url_for("login", _external=True)
    mail.send_message(
            sender=("NOREPLY", sender),
            subject="This is how you helped",
            body=f"""Dear {current_user.name}

            On behalf of everyone at Diverse Abilities, I would like to extend our heartfelt thanks for your recent donation. 
            Your generosity is not just a gift, but a commitment to the values we uphold and the community we serve together.

            Thanks to contributions like yours, we continue to enhance the lives of people with disabilities across all age groups. Your donation helps us deliver comprehensive care and support through various programs, such as:

- Langside School: A specialist day school providing personalized education and therapeutic programs to children with complex physical disabilities and health needs.
- Smithers: Offering adults innovative support plans that promote independence, enhance life skills, and provide employment opportunities within the community.
- Supported Living and Residential Services: Helping adults live as independently as possible in welcoming environments, where they can develop personal, social, and emotional skills.
- Domiciliary Care: Extending tailored support to individuals in their own homes, fostering independence with respect, dignity, and encouraging community engagement.

We believe in making every aspect of life accessible and enjoyable for those we support, and your donation directly contributes to this mission. If you are moved to extend your impact further, consider joining our network of passionate volunteers. There are numerous opportunities, from engaging directly with those we support to assisting in events that raise awareness and funds for our cause.
Click here: {confirm_url}

Thank you once again for your kindness and support. Together, we are creating a more inclusive world where every individual has the opportunity to thrive. If you have any questions, or if there's any particular area you're interested in getting involved with, please don't hesitate to reach out.

With gratitude,
Diverse Abilities
""",
            recipients=recipients)

@app.route('/donate', methods=['GET','POST'])
@login_required
def donating():
    if request.method == 'POST':
        #send_donation_email()
        return redirect("/")
    return render_template('donate.html')

if __name__ == "__main__":
    app.run(debug=True, ssl_context=("cert.pem","key.pem"))