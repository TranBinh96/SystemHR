#!/usr/bin/env python3
"""
Database migration script to remove personal information fields from User model.
This script removes: gender, phone, citizen_id, hometown, email columns from users table.

Usage: python scripts/remove_personal_info_fields.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db
from app import app
from sqlalchemy import text

def remove_personal_info_fields():
    """Remove personal information fields from users table"""
    
    with app.app_context():
        try:
            print("🔄 Starting removal of personal information fields from users table...")
            
            # List of columns to remove
            columns_to_remove = ['gender', 'phone', 'citizen_id', 'hometown', 'email']
            
            # Check which columns exist before attempting to drop them
            existing_columns = []
            for column in columns_to_remove:
                try:
                    result = db.session.execute(text(f"SELECT {column} FROM users LIMIT 1"))
                    existing_columns.append(column)
                    print(f"✅ Column '{column}' exists and will be removed")
                except Exception:
                    print(f"⚠️  Column '{column}' does not exist, skipping")
            
            if not existing_columns:
                print("ℹ️  No personal information columns found to remove")
                return
            
            # Remove each existing column
            for column in existing_columns:
                try:
                    print(f"🗑️  Removing column '{column}'...")
                    db.session.execute(text(f"ALTER TABLE users DROP COLUMN {column}"))
                    print(f"✅ Successfully removed column '{column}'")
                except Exception as e:
                    print(f"❌ Error removing column '{column}': {str(e)}")
                    # Continue with other columns even if one fails
                    continue
            
            # Commit all changes
            db.session.commit()
            print("✅ Successfully removed personal information fields from users table")
            print("🔒 User privacy enhanced - personal data fields removed")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            raise
        finally:
            db.session.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🔒 REMOVE PERSONAL INFORMATION FIELDS MIGRATION")
    print("=" * 60)
    print("This script will remove personal information fields from the users table:")
    print("- gender")
    print("- phone") 
    print("- citizen_id")
    print("- hometown")
    print("- email")
    print("=" * 60)
    
    confirm = input("⚠️  Are you sure you want to proceed? This action cannot be undone! (yes/no): ")
    if confirm.lower() == 'yes':
        remove_personal_info_fields()
        print("🎉 Migration completed successfully!")
    else:
        print("❌ Migration cancelled by user")