#!/usr/bin/env python3
"""
Migration script to remove can_register_overtime column from users table
This column is redundant - we only need can_approve and overtime_approver_id
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text

def remove_column():
    """Remove can_register_overtime column from users table"""
    with app.app_context():
        try:
            print("\n" + "="*60)
            print("REMOVING can_register_overtime COLUMN")
            print("="*60)
            
            # Check if column exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'users'
                AND COLUMN_NAME = 'can_register_overtime'
            """))
            
            exists = result.fetchone()[0] > 0
            
            if not exists:
                print("✓ Column 'can_register_overtime' does not exist - nothing to do")
                return True
            
            print("\n1. Column 'can_register_overtime' exists - will be removed")
            
            # Drop the column
            print("\n2. Dropping column...")
            db.session.execute(text("""
                ALTER TABLE users
                DROP COLUMN can_register_overtime
            """))
            
            db.session.commit()
            
            print("✅ Successfully removed column 'can_register_overtime'")
            
            print("\n" + "="*60)
            print("MIGRATION COMPLETED")
            print("="*60)
            print("\nNew logic:")
            print("  - Manager (can_approve=True): Tự đăng ký và tự phê duyệt")
            print("  - User thường: Cần có overtime_approver_id để đăng ký")
            print("\nNo more can_register_overtime needed!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = remove_column()
    sys.exit(0 if success else 1)
