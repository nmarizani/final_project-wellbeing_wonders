
from flask import Flask, render_template, redirect, url_for, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, submit
from flask_migrate import Migrate  
import logging  
import os   
from dotenv import load_dotenv
from werkzeug.security import check_password_hash




load_dotenv()
app = Flask(__name__)
def create_app():
    app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_file.db'  # Modify to your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to disable modification tracking
app.config['SECRET_KEY'] = '28bc6cce497a59b9fccae6890f4067f718f375230002a7c3'  # Required for sessions and flash messages
from flask_mail import Mail, Message

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'uloveclub@gail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'U-LOVE2023'     # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = ('U-LOVE Wonders', 'uloveclub@gmail.com')

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'uloveclub@gmail.com'
app.config['MAIL_PASSWORD'] = 'U-LOVE2023'

def send_feedback_email(feedback_message):
    msg = Message('New Feedback Submission', recipients=['uloveclub@gmail.com'])
    msg.body = f"Feedback: {feedback_message}"
    mail.send(msg)
# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect unauthorized users to login
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return True  # Returns True if the user is active
    
    def get_id(self):
        """Return the unique identifier for the user."""
        return str(self.id)
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
    


    # Password hashing and verification
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# User loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists. Please proceed to login.", "danger")
            return redirect(url_for('register'))

        try:
            user = User(username=username, email=email, role=role)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
            login_user(user)

            # Redirect all users to a single dashboard
            flash("Registration successful! Please log in to continue.", "success")
            return redirect(url_for('main_dashboard'))

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error during registration: {e}")
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('register'))
    
    if form.errors:
        flash("Please check the form for errors.", "danger")
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/main_dashboard')
@login_required
def main_dashboard():
    if current_user.is_authenticated:
        role = getattr(current_user, 'role', 'default_role')  # Use a default if role doesn't exist
    else:
        role = None  # Anonymous users don't have roles
    return render_template('main_dashboard.html', role=current_user.role)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)    
        session.pop('role', None)
    
    return render_template('logout.html')

@app.route('/logout_page')
def logout_page():
    logout_user()
    return render_template('logout.html')

@app.route('/support_group')
def support_group():
    return render_template('support_group.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
     if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create and send the email
        try:
            msg = Message(
                subject="New Contact Us Message",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=['uloveclub@gmail'],  # Replace with your receiving email
                body=f"Message from {name} ({email}):\n\n{message}"
            )
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send message. Error: {e}", "danger")

        return redirect(url_for('contact'))
     return render_template('contact.html')     

@app.route('/resources/')
def resources():
    return render_template('resources.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/support')
def support():
    return render_template('support.html')  

@app.route('/chat') 
def chat():
    return render_template('chat.html')

@app.route('/feedback') 
def feedback():
    return render_template('feedback.html')


@app.route('/process_feedback', methods=['POST'])
def process_feedback():
    message = request.form['message']
    send_feedback_email( message)
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('feedback'))
    

@app.route('/counsellor')
def counsellor():
    return render_template('counsellor.html')

@app.route('/peer_support_dashboard')
def peer_dashboard():
    return render_template('peer_support_dashboard.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
 return render_template('admin_dashboard.html')

@app.route('/counsellor_dashboard')
def counsellor_dashboard():
    return render_template('counsellor_dashboard.html')

@app.route('/book_session')
def book_session():
    return render_template('book_session.html')

@app.route('/process_booking', methods=['POST'])
def process_booking():
    # Extract data from the form submission
    session_date = request.form.get('session_date')
    session_time = request.form.get('session_time')
    notes = request.form.get('notes', '')

    # Here, save the booking to the database or process it further if required.
    # For now, we'll just flash a success message.
    flash(f"Booking successful for {session_date} at {session_time}!", "success")
    
    # Redirect the user back to their dashboard or another page
    return redirect(url_for('counsellor'))

# Initialize the database and run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

