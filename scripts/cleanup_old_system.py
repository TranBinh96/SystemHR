#!/usr/bin/env python3
"""
Cleanup old department_managers system
This table is no longer needed with the new level-based hierarchy
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db
from sqlalchemy import text

def cleanup_old_system():
    """Remove old department_managers table"""
    with app.app_context():
        try:
            print("Cleaning up old department_managers system...")
            
            # Check if table exists
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'department_managers' in tables:
                print("Dropping 'department_managers' table...")
                db.session.execute(text("DROP TABLE department_managers"))
                db.session.commit()
                print("[OK] Dropped 'department_managers' table")
            else:
                print("[SKIP] 'department_managers' table doesn't exist")
            
            print("\n" + "="*60)
            print("Cleanup completed!")
            print("="*60)
            print("\nThe system now uses level-based hierarchy:")
            print("- No need to manually assign managers")
            print("- Users with lower level automatically become approvers")
            print("- More flexible and scalable")
            
        except Exception as e:
            print(f"\n[ERROR] Cleanup failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    cleanup_old_system()
