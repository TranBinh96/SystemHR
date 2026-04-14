#!/usr/bin/env python3
"""
Script to remove unused fields from users table
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

def remove_unused_fields():
    """Remove unused fields from users table"""
    with app.app_context():
        try:
            print("Removing unused fields from users table...")
            print("="*60)
            
            # List of fields to remove
            fields_to_remove = [
                'gender',
                'phone', 
                'citizen_id',
                'hometown'
            ]
            
            # Drop constraints first (if any)
            print("Dropping constraints...")
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE users DROP INDEX email"))
                    conn.commit()
                print("✅ Dropped email unique constraint")
            except Exception as e:
                print(f"⚠️  Email constraint may not exist: {e}")
            
            # Drop columns
            print("\nDropping columns...")
            for field in fields_to_remove:
                try:
                    with db.engine.connect() as conn:
                        conn.execute(db.text(f"ALTER TABLE users DROP COLUMN {field}"))
                        conn.commit()
                    print(f"✅ Dropped column: {field}")
                except Exception as e:
                    print(f"❌ Failed to drop {field}: {e}")
            
            print("\n" + "="*60)
            print("✅ Cleanup completed!")
            
            # Show remaining columns
            print("\nRemaining columns in users table:")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("DESCRIBE users"))
                for row in result:
                    print(f"  {row[0]}: {row[1]}")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise

if __name__ == '__main__':
    remove_unused_fields()