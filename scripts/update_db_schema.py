"""
Script to update database schema - add last_activity column
Run this after updating models
"""
from app import app, db
from models import User
from datetime import datetime

def update_schema():
    """Add last_activity column to existing users table"""
    with app.app_context():
        print("Updating database schema...")
        
        try:
            # Try to add the column using raw SQL
            with db.engine.connect() as conn:
                # Check if column exists
                result = conn.execute(db.text("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'last_activity'
                """))
                
                exists = result.scalar() > 0
                
                if not exists:
                    print("Adding last_activity column...")
                    conn.execute(db.text("""
                        ALTER TABLE users 
                        ADD COLUMN last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
                    """))
                    conn.commit()
                    
                    # Update existing users
                    print("Updating existing users...")
                    conn.execute(db.text("""
                        UPDATE users 
                        SET last_activity = CURRENT_TIMESTAMP 
                        WHERE last_activity IS NULL
                    """))
                    conn.commit()
                    
                    print("✓ Schema updated successfully!")
                else:
                    print("✓ Column already exists, no update needed")
                    
        except Exception as e:
            print(f"❌ Error updating schema: {e}")
            print("\nPlease run this SQL manually:")
            print("""
ALTER TABLE users 
ADD COLUMN last_activity DATETIME DEFAULT CURRENT_TIMESTAMP;

UPDATE users 
SET last_activity = CURRENT_TIMESTAMP 
WHERE last_activity IS NULL;
            """)

if __name__ == '__main__':
    update_schema()
