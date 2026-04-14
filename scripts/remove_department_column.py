#!/usr/bin/env python3
"""
Script to remove the old department column from users table
Only keep department_id foreign key
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User
from sqlalchemy import text

def remove_department_column():
    """Remove the old department string column"""
    with app.app_context():
        try:
            # Check if department column exists
            result = db.session.execute(text("SHOW COLUMNS FROM users LIKE 'department'"))
            if result.fetchone():
                print("Removing department column from users table...")
                
                # Drop the department column
                db.session.execute(text("ALTER TABLE users DROP COLUMN department"))
                db.session.commit()
                
                print("✅ Successfully removed department column")
                print("✅ Users table now only uses department_id foreign key")
            else:
                print("ℹ️  Department column does not exist")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error removing department column: {e}")
            return False
            
        return True

if __name__ == "__main__":
    print("🔄 Starting department column removal...")
    success = remove_department_column()
    
    if success:
        print("✅ Department column removal completed successfully!")
    else:
        print("❌ Department column removal failed!")
        sys.exit(1)