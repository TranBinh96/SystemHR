#!/usr/bin/env python3
"""
Script to remove the level field from users table
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

def remove_level_field():
    """Remove level field from users table"""
    with app.app_context():
        try:
            print("Removing level field from users table...")
            print("="*60)
            
            # Drop the level column
            print("Dropping level column...")
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE users DROP COLUMN level"))
                    conn.commit()
                print("✅ Dropped column: level")
            except Exception as e:
                print(f"❌ Failed to drop level: {e}")
            
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
    remove_level_field()