from app import db  # Import db from the app module where it was initialized
from flask_login import UserMixin   
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    # Flask-Login required properties
    #Password hashing and verification
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return bcrypt.check_password_hash(self.password, password)

