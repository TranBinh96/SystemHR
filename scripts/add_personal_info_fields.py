"""
Migration script to add personal information fields to users table
Adds: gender, phone, citizen_id, hometown
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text

def add_personal_info_fields():
    """Add gender, phone, citizen_id, and hometown fields to users table"""
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            fields_to_add = []
            if 'gender' not in columns:
                fields_to_add.append(('gender', 'VARCHAR(10)'))
            if 'phone' not in columns:
                fields_to_add.append(('phone', 'VARCHAR(20)'))
            if 'citizen_id' not in columns:
                fields_to_add.append(('citizen_id', 'VARCHAR(20)'))
            if 'hometown' not in columns:
                fields_to_add.append(('hometown', 'VARCHAR(200)'))
            
            if not fields_to_add:
                print("✓ All personal info fields already exist in users table")
                return
            
            # Add missing columns
            for field_name, field_type in fields_to_add:
                sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                db.session.execute(text(sql))
                print(f"✓ Added {field_name} column to users table")
            
            db.session.commit()
            print(f"\n✓ Successfully added {len(fields_to_add)} personal info field(s) to users table")
            print("✓ Fields added:", ', '.join([f[0] for f in fields_to_add]))
            print("\nPlease restart your Flask application for changes to take effect.")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding personal info fields: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("Adding personal information fields to users table...")
    print("Fields: gender, phone, citizen_id, hometown\n")
    add_personal_info_fields()
