
from flask import Flask, render_template, redirect, url_for, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm  # Ensure forms are correctly defined
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
        logging.debug("Form is valid")
        # Extract form data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data  # Ensure your form includes a role field

        logging.debug(f"Form data - Username: {username}, Email: {email}, Password: {password}, Role: {role}")

        # Check for duplicate users
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists. Please use a different one.", "danger")
            return redirect(url_for('register'))

        try:
            # Create a new user instance and hash the password
            user = User(username=username, email=email, role=role)
            user.set_password(password)

            # Save the user to the database
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!", "success")
            # Log the user in immediately after registration
            login_user(user)
            print(f"Logged in user: {user.username}, Role: {user.role}")

            # Redirect based on user's role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'peer_supporter':
                return redirect(url_for('peer_supporter_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))

        except Exception as e:
            logging.error(f"An error occurred during registration: {str(e)}")
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('register'))
    
    else:
        if form.errors:
            logging.debug("Form errors")
            flash("Please check the form for errors.", "danger")
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard'))  # Redirect if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')

            # Redirect based on user role
            role_redirects = {
                'admin': 'admin_dashboard',
                'counsellor': 'counsellor_dashboard',
                'peer_supporter': 'peer_supporter_dashboard',
                'student': 'student_dashboard'

            }
            return redirect(url_for(role_redirects.get(user.role, 'dashboard')))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('peer_support_dashboard.html', form=form)

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

@app.route('/contact')
def contact():
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

@app.route('/counsellor')
def counsellor():
    return render_template('counsellor.html')

@app.route('/peer_support_dashboard')
@login_required
def peer_dashboard():
    if current_user.role != 'peer_supporter':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    return render_template('peer_support_dashboard.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login')) 
    return render_template('student_dashboard.html')

@app.route('/admin-dashboard' , methods=['GET'])
@login_required
def admin_dashboard():
     print(f"Is user authenticated? {current_user.is_authenticated}")
     print(f"User ID: {getattr(current_user, 'id', None)}")
     print(f"User role: {getattr(current_user, 'role', None)}")
     if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
     return render_template('admin_dashboard.html')

# Initialize the database and run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
