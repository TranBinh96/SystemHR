"""
Migration script to remove position-related tables and columns
Run this script to clean up position data from database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text

def remove_position_tables():
    """Remove position-related tables and columns from database"""
    with app.app_context():
        try:
            print("Starting position removal migration...")
            
            # Drop foreign key constraints first
            print("1. Dropping foreign key constraints...")
            
            # Drop position_id from users table
            try:
                with db.engine.connect() as conn:
                    # Check if column exists
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'users' 
                        AND COLUMN_NAME = 'position_id'
                    """))
                    if result.scalar() > 0:
                        print("   - Dropping position_id from users table...")
                        conn.execute(text("ALTER TABLE users DROP FOREIGN KEY IF EXISTS users_ibfk_2"))
                        conn.execute(text("ALTER TABLE users DROP COLUMN position_id"))
                        conn.commit()
                        print("   OK Removed position_id from users")
                    else:
                        print("   - position_id column not found in users table")
            except Exception as e:
                print(f"   Warning dropping position_id: {e}")


            
            # Drop position column from overtime_requests
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'overtime_requests' 
                        AND COLUMN_NAME = 'position'
                    """))
                    if result.scalar() > 0:
                        print("   - Dropping position from overtime_requests table...")
                        conn.execute(text("ALTER TABLE overtime_requests DROP COLUMN position"))
                        conn.commit()
                        print("   OK Removed position from overtime_requests")
                    else:
                        print("   - position column not found in overtime_requests table")
            except Exception as e:
                print(f"   Warning dropping position from overtime_requests: {e}")
            
            # Drop position column from leave_requests
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'leave_requests' 
                        AND COLUMN_NAME = 'position'
                    """))
                    if result.scalar() > 0:
                        print("   - Dropping position from leave_requests table...")
                        conn.execute(text("ALTER TABLE leave_requests DROP COLUMN position"))
                        conn.commit()
                        print("   OK Removed position from leave_requests")
                    else:
                        print("   - position column not found in leave_requests table")
            except Exception as e:
                print(f"   Warning dropping position from leave_requests: {e}")
            
            # Drop position column from exit_entry_requests
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'exit_entry_requests' 
                        AND COLUMN_NAME = 'position'
                    """))
                    if result.scalar() > 0:
                        print("   - Dropping position from exit_entry_requests table...")
                        conn.execute(text("ALTER TABLE exit_entry_requests DROP COLUMN position"))
                        conn.commit()
                        print("   OK Removed position from exit_entry_requests")
                    else:
                        print("   - position column not found in exit_entry_requests table")
            except Exception as e:
                print(f"   Warning dropping position from exit_entry_requests: {e}")
            
            print("\n2. Dropping approval_hierarchy table...")
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.TABLES 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'approval_hierarchy'
                    """))
                    if result.scalar() > 0:
                        conn.execute(text("DROP TABLE IF EXISTS approval_hierarchy"))
                        conn.commit()
                        print("   OK Dropped approval_hierarchy table")
                    else:
                        print("   - approval_hierarchy table not found")
            except Exception as e:
                print(f"   Warning dropping approval_hierarchy: {e}")
            
            print("\n3. Dropping positions table...")
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT COUNT(*) 
                        FROM information_schema.TABLES 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'positions'
                    """))
                    if result.scalar() > 0:
                        conn.execute(text("DROP TABLE IF EXISTS positions"))
                        conn.commit()
                        print("   OK Dropped positions table")
                    else:
                        print("   - positions table not found")
            except Exception as e:
                print(f"   Warning dropping positions: {e}")
            
            print("\n=== Migration completed successfully ===")
            print("Position-related tables and columns have been removed.")
            
        except Exception as e:
            print(f"\nError during migration: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    print("=" * 60)
    print("REMOVE POSITION TABLES MIGRATION")
    print("=" * 60)
    print("\nThis will remove:")
    print("- positions table")
    print("- approval_hierarchy table")
    print("- position_id column from users table")
    print("- position column from overtime_requests, leave_requests, exit_entry_requests")
    print("\n" + "=" * 60)
    
    confirm = input("\nAre you sure you want to continue? (yes/no): ")
    if confirm.lower() == 'yes':
        remove_position_tables()
    else:
        print("Migration cancelled.")
