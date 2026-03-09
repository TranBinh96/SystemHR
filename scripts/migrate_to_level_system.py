#!/usr/bin/env python3
"""
Migration script to add level-based hierarchy system
Adds department_id and level fields to users table
Updates positions table to include level
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db
from sqlalchemy import text

def migrate_to_level_system():
    """Add level and department_id fields to support hierarchy"""
    with app.app_context():
        try:
            print("Starting migration to level-based system...")
            
            # Check current schema
            inspector = db.inspect(db.engine)
            users_columns = [col['name'] for col in inspector.get_columns('users')]
            positions_columns = [col['name'] for col in inspector.get_columns('positions')]
            
            # 1. Add level to positions table if not exists
            if 'level' not in positions_columns:
                print("Adding 'level' column to positions table...")
                db.session.execute(text("""
                    ALTER TABLE positions 
                    ADD COLUMN level INT DEFAULT 5
                """))
                db.session.commit()
                print("[OK] Added 'level' column to positions")
            else:
                print("[SKIP] 'level' column already exists in positions")
            
            # 2. Add department_id to users table if not exists
            if 'department_id' not in users_columns:
                print("Adding 'department_id' column to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN department_id INT
                """))
                db.session.commit()
                print("[OK] Added 'department_id' column to users")
            else:
                print("[SKIP] 'department_id' column already exists in users")
            
            # 3. Add position_id to users table if not exists
            if 'position_id' not in users_columns:
                print("Adding 'position_id' column to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN position_id INT
                """))
                db.session.commit()
                print("[OK] Added 'position_id' column to users")
            else:
                print("[SKIP] 'position_id' column already exists in users")
            
            # 4. Add level to users table if not exists (denormalized for performance)
            if 'level' not in users_columns:
                print("Adding 'level' column to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN level INT DEFAULT 5
                """))
                db.session.commit()
                print("[OK] Added 'level' column to users")
            else:
                print("[SKIP] 'level' column already exists in users")
            
            # 5. Create departments table if not exists
            if 'departments' not in inspector.get_table_names():
                print("Creating 'departments' table...")
                db.session.execute(text("""
                    CREATE TABLE departments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        code VARCHAR(50) UNIQUE NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        description TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """))
                db.session.commit()
                print("[OK] Created 'departments' table")
                
                # Insert default departments
                print("Inserting default departments...")
                db.session.execute(text("""
                    INSERT INTO departments (code, name, description) VALUES
                    ('IT', 'Công nghệ thông tin', 'Phòng IT'),
                    ('HR', 'Nhân sự', 'Phòng nhân sự'),
                    ('PROD', 'Sản xuất', 'Phòng sản xuất'),
                    ('WAREHOUSE', 'Kho', 'Phòng kho'),
                    ('QC', 'Kiểm soát chất lượng', 'Phòng QC'),
                    ('ADMIN', 'Hành chính', 'Phòng hành chính')
                """))
                db.session.commit()
                print("[OK] Inserted default departments")
            else:
                print("[SKIP] 'departments' table already exists")
            
            # 6. Update positions with default levels
            print("Updating positions with default levels...")
            position_levels = {
                'Giám đốc': 1,
                'Phó giám đốc': 1,
                'Trợ lý': 2,
                'Trưởng phòng': 2,
                'Phó phòng': 3,
                'Giám sát': 3,
                'Trưởng nhóm': 3,
                'Quản lý': 3,
                'Nhân viên': 4,
                'Công nhân': 5
            }
            
            for position_name, level in position_levels.items():
                db.session.execute(text(f"""
                    UPDATE positions 
                    SET level = {level}
                    WHERE name LIKE '%{position_name}%'
                """))
            db.session.commit()
            print("[OK] Updated position levels")
            
            print("\n" + "="*50)
            print("Migration completed successfully!")
            print("="*50)
            print("\nNext steps:")
            print("1. Update user records to set department_id and position_id")
            print("2. System will automatically determine approvers based on level")
            print("3. Remove old department_managers table if no longer needed")
            
        except Exception as e:
            print(f"\n[ERROR] Migration failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_to_level_system()
