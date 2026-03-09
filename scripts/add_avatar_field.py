"""
Add avatar_url field to users table
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

def add_avatar_field():
    with app.app_context():
        try:
            # Add avatar_url column to users table
            db.session.execute(db.text("""
                ALTER TABLE users 
                ADD COLUMN avatar_url VARCHAR(255) DEFAULT NULL
            """))
            db.session.commit()
            print("✓ Successfully added avatar_url column to users table")
        except Exception as e:
            db.session.rollback()
            if "Duplicate column name" in str(e) or "already exists" in str(e):
                print("✓ Column avatar_url already exists")
            else:
                print(f"✗ Error adding avatar_url column: {e}")
                raise

if __name__ == '__main__':
    add_avatar_field()
