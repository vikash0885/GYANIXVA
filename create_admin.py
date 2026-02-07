from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print(f"Admin already exists: {admin.username}")
            return
            
        print("Creating default Admin user...")
        username = input("Enter Admin Username (default: admin): ") or 'admin'
        email = input("Enter Admin Email (default: admin@vsl.com): ") or 'admin@vsl.com'
        password = input("Enter Admin Password (default: admin123): ") or 'admin123'
        
        new_admin = User(full_name="System Admin", username=username, email=email, role='admin')
        new_admin.set_password(password)
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"Success! Admin user '{username}' created.")

if __name__ == '__main__':
    create_admin_user()
