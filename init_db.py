from app import db, app  # Import your app and db objects

def init_db():
 with app.app_context():  # Ensure you're in the app's context
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    init_db()