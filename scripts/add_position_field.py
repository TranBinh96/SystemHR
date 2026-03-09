"""
Script to add position field to users table
Run this script to add the position column to existing database
"""
from app import app, db
from sqlalchemy import text

def add_position_field():
    with app.app_context():
        try:
            # Check if column exists (MySQL version)
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "AND TABLE_NAME = 'users' "
                "AND COLUMN_NAME = 'position'"
            ))
            exists = result.scalar() > 0
            
            if not exists:
                # Add position column for MySQL
                db.session.execute(text(
                    "ALTER TABLE users ADD COLUMN position VARCHAR(50) DEFAULT 'staff'"
                ))
                db.session.commit()
                print("✓ Successfully added 'position' column to users table")
            else:
                print("✓ Column 'position' already exists")
                
        except Exception as e:
            print(f"✗ Error adding position field: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_position_field()
