"""
Script to update overtime_requests table schema
- Add number_of_people column
- Make start_time, end_time, total_hours nullable
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from sqlalchemy import text

def update_overtime_schema():
    with app.app_context():
        try:
            print("🔄 Updating overtime_requests table schema...")
            
            # Check if number_of_people column exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'db_hr'
                AND TABLE_NAME = 'overtime_requests'
                AND COLUMN_NAME = 'number_of_people'
            """))
            exists = result.fetchone()[0] > 0
            
            if not exists:
                # Add number_of_people column
                db.session.execute(text("""
                    ALTER TABLE overtime_requests 
                    ADD COLUMN number_of_people INTEGER DEFAULT 1 NOT NULL
                """))
                print("   ✓ Added column: number_of_people")
            else:
                print("   ℹ Column number_of_people already exists")
            
            # Make start_time, end_time, total_hours nullable
            db.session.execute(text("""
                ALTER TABLE overtime_requests 
                MODIFY COLUMN start_time TIME NULL
            """))
            print("   ✓ Modified: start_time (now nullable)")
            
            db.session.execute(text("""
                ALTER TABLE overtime_requests 
                MODIFY COLUMN end_time TIME NULL
            """))
            print("   ✓ Modified: end_time (now nullable)")
            
            db.session.execute(text("""
                ALTER TABLE overtime_requests 
                MODIFY COLUMN total_hours DECIMAL(4,2) NULL
            """))
            print("   ✓ Modified: total_hours (now nullable)")
            
            db.session.commit()
            print("✅ Schema updated successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating schema: {e}")
            return False
        
        return True

if __name__ == '__main__':
    update_overtime_schema()
