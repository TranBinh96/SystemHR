"""
Script to add work_status column to users table
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from sqlalchemy import text

def add_work_status_column():
    """Add work_status column to users table"""
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'work_status'
            """))
            
            exists = result.fetchone()[0] > 0
            
            if exists:
                print("✓ Column 'work_status' already exists in users table")
                return
            
            # Add work_status column
            print("Adding work_status column to users table...")
            db.session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN work_status VARCHAR(20) DEFAULT 'working' AFTER position
            """))
            
            # Update existing records to 'working'
            db.session.execute(text("""
                UPDATE users 
                SET work_status = 'working' 
                WHERE work_status IS NULL
            """))
            
            db.session.commit()
            print("✓ Successfully added work_status column")
            print("  - Default value: 'working'")
            print("  - Possible values: 'working', 'business_trip', 'resigned'")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding work_status column: {str(e)}")
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("Adding work_status column to users table")
    print("=" * 60)
    add_work_status_column()
    print("\nMigration completed!")
