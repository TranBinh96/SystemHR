"""
Script to add overtime permission fields to users table
- Add can_register_overtime column
- Add overtime_approver_id column
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from sqlalchemy import text

def update_user_schema():
    with app.app_context():
        try:
            print("🔄 Updating users table for overtime permissions...")
            
            # Check if can_register_overtime column exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'db_hr'
                AND TABLE_NAME = 'users'
                AND COLUMN_NAME = 'can_register_overtime'
            """))
            exists = result.fetchone()[0] > 0
            
            if not exists:
                # Add can_register_overtime column
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN can_register_overtime TINYINT(1) DEFAULT 0
                """))
                print("   ✓ Added column: can_register_overtime")
            else:
                print("   ℹ Column can_register_overtime already exists")
            
            # Check if overtime_approver_id column exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'db_hr'
                AND TABLE_NAME = 'users'
                AND COLUMN_NAME = 'overtime_approver_id'
            """))
            exists = result.fetchone()[0] > 0
            
            if not exists:
                # Add overtime_approver_id column
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN overtime_approver_id INTEGER NULL,
                    ADD CONSTRAINT fk_overtime_approver 
                    FOREIGN KEY (overtime_approver_id) REFERENCES users(id)
                """))
                print("   ✓ Added column: overtime_approver_id")
            else:
                print("   ℹ Column overtime_approver_id already exists")
            
            db.session.commit()
            print("✅ Schema updated successfully!")
            print("\n📝 Next steps:")
            print("   1. Go to Admin > Users")
            print("   2. Set 'can_register_overtime' = True for users who can register")
            print("   3. Set 'overtime_approver_id' to assign approver for each user")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating schema: {e}")
            return False
        
        return True

if __name__ == '__main__':
    update_user_schema()
