"""
Database initialization script
Run this to create all tables in the database
"""
from app import app, db
from models import User, OvertimeRequest, MealRegistration
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and sample data"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(employee_id='ADMIN').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                employee_id='ADMIN',
                name='Administrator',
                email='admin@okivietnam.com',
                password=generate_password_hash('admin123'),
                department='IT',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created!")
            print("  Employee ID: ADMIN")
            print("  Password: admin123")
        else:
            print("\n✓ Admin user already exists")
        
        # Create sample user
        sample_user = User.query.filter_by(employee_id='EMP001').first()
        if not sample_user:
            print("\nCreating sample user...")
            sample_user = User(
                employee_id='EMP001',
                name='Nguyen Van A',
                email='nguyenvana@okivietnam.com',
                password=generate_password_hash('password123'),
                department='production',
                role='user'
            )
            db.session.add(sample_user)
            db.session.commit()
            print("✓ Sample user created!")
            print("  Employee ID: EMP001")
            print("  Password: password123")
        else:
            print("\n✓ Sample user already exists")
        
        print("\n" + "="*50)
        print("Database initialization completed successfully!")
        print("="*50)

if __name__ == '__main__':
    init_database()
