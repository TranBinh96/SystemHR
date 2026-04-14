#!/usr/bin/env python3
"""
Script to add permission fields to users table
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

def add_permission_fields():
    """Add permission fields to users table"""
    with app.app_context():
        try:
            print("Adding permission fields to users table...")
            print("="*60)
            
            # Add can_approve field
            print("Adding can_approve field...")
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN can_approve TINYINT(1) DEFAULT 0"))
                    conn.commit()
                print("✅ Added column: can_approve")
            except Exception as e:
                print(f"❌ Failed to add can_approve: {e}")
            
            # Add can_register field
            print("Adding can_register field...")
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN can_register TINYINT(1) DEFAULT 1"))
                    conn.commit()
                print("✅ Added column: can_register")
            except Exception as e:
                print(f"❌ Failed to add can_register: {e}")
            
            print("\n" + "="*60)
            print("✅ Permission fields added!")
            
            # Set default permissions based on position_id
            print("\nSetting default permissions...")
            try:
                with db.engine.connect() as conn:
                    # Users with position_id = 1 can approve
                    conn.execute(db.text("UPDATE users SET can_approve = 1 WHERE position_id = 1"))
                    # All active users can register by default
                    conn.execute(db.text("UPDATE users SET can_register = 1 WHERE is_active = 1"))
                    conn.commit()
                print("✅ Set default permissions")
            except Exception as e:
                print(f"❌ Failed to set default permissions: {e}")
            
            # Show updated table structure
            print("\nUpdated users table structure:")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("DESCRIBE users"))
                for row in result:
                    print(f"  {row[0]}: {row[1]}")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise

if __name__ == '__main__':
    add_permission_fields()