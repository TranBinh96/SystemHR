"""
Auto setup database and tables
Automatically creates database and tables if they don't exist
Supports automatic table creation when new models are added
"""
import mysql.connector
from mysql.connector import Error
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from werkzeug.security import generate_password_hash

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute(f"SHOW DATABASES LIKE '{Config.DB_NAME}'")
            result = cursor.fetchone()
            
            if not result:
                print(f"📦 Database '{Config.DB_NAME}' not found. Creating...")
                cursor.execute(f"CREATE DATABASE {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✓ Database '{Config.DB_NAME}' created successfully!")
            else:
                print(f"✓ Database '{Config.DB_NAME}' already exists")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def get_existing_tables():
    """Get list of existing tables in database"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            connection.close()
            return tables
    except Error as e:
        print(f"Warning: Could not get existing tables: {e}")
        return []

def create_tables_if_not_exist():
    """
    Create tables if they don't exist
    Automatically detects all models and creates corresponding tables
    """
    try:
        from app import app, db
        from models import User, OvertimeRequest, MealRegistration
        
        with app.app_context():
            print("\n📋 Checking and creating tables...")
            
            # Get existing tables before creation
            existing_tables_before = get_existing_tables()
            print(f"   Existing tables: {existing_tables_before if existing_tables_before else 'None'}")
            
            # Create all tables (SQLAlchemy will skip existing ones)
            db.create_all()
            
            # Get tables after creation
            existing_tables_after = get_existing_tables()
            new_tables = set(existing_tables_after) - set(existing_tables_before)
            
            if new_tables:
                print(f"✓ New tables created: {', '.join(new_tables)}")
            else:
                print("✓ All tables already exist")
            
            print(f"   Total tables: {len(existing_tables_after)}")
            
            # List all tables with their models
            print("\n📊 Database Schema:")
            model_table_map = {
                'users': 'User',
                'overtime_requests': 'OvertimeRequest',
                'meal_registrations': 'MealRegistration'
            }
            
            for table in sorted(existing_tables_after):
                model_name = model_table_map.get(table, 'Unknown')
                status = "✓" if table in existing_tables_before else "🆕"
                print(f"   {status} {table} ({model_name})")
            
            # Create default users if needed
            create_default_users()
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_default_users():
    """Create default admin and sample users if they don't exist"""
    from app import app, db
    from models import User
    
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(employee_id='ADMIN').first()
        if not admin:
            print("\n👤 Creating default admin user...")
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
        
        # Check if sample user exists
        sample_user = User.query.filter_by(employee_id='EMP001').first()
        if not sample_user:
            print("\n👤 Creating sample user...")
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

def verify_database_structure():
    """Verify database structure and show statistics"""
    try:
        from app import app, db
        from models import User, OvertimeRequest, MealRegistration
        
        with app.app_context():
            print("\n📈 Database Statistics:")
            
            # Count records in each table
            user_count = User.query.count()
            overtime_count = OvertimeRequest.query.count()
            meal_count = MealRegistration.query.count()
            
            print(f"   Users: {user_count}")
            print(f"   Overtime Requests: {overtime_count}")
            print(f"   Meal Registrations: {meal_count}")
            
            return True
    except Exception as e:
        print(f"⚠️  Could not verify database structure: {e}")
        return False

def main():
    """Main setup function"""
    print("="*60)
    print("OKI VIETNAM HR SYSTEM - Auto Database Setup")
    print("="*60)
    print()
    
    # Step 1: Create database
    print("Step 1: Database Creation")
    print("-" * 60)
    if not create_database_if_not_exists():
        print("\n❌ Failed to create database. Please check your MySQL connection.")
        print("\nTroubleshooting:")
        print("1. Check MySQL server is running")
        print("2. Verify credentials in .env file")
        print("3. Ensure user has CREATE DATABASE privilege")
        return False
    
    # Step 2: Create tables
    print("\nStep 2: Table Creation")
    print("-" * 60)
    if not create_tables_if_not_exist():
        print("\n❌ Failed to create tables. Please check the error above.")
        return False
    
    # Step 3: Verify structure
    print("\nStep 3: Verification")
    print("-" * 60)
    verify_database_structure()
    
    print("\n" + "="*60)
    print("✓ Database setup completed successfully!")
    print("="*60)
    print("\n🚀 You can now run the application:")
    print("   python app.py")
    print("\n🔑 Default login credentials:")
    print("   Admin: ADMIN / admin123")
    print("   User: EMP001 / password123")
    print("\n💡 Tips:")
    print("   - Change default passwords after first login")
    print("   - Access admin panel at /admin")
    print("   - API documentation at /api (with JWT tokens)")
    print("="*60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
