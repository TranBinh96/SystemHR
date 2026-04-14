#!/usr/bin/env python3
"""
Script to create departments table
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db

def create_departments_table():
    """Create departments table"""
    with app.app_context():
        try:
            print("Creating departments table...")
            print("="*60)
            
            # Create departments table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                manager_id INT,
                is_active TINYINT(1) DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_code (code),
                INDEX idx_name (name),
                INDEX idx_manager (manager_id)
            )
            """
            
            with db.engine.connect() as conn:
                conn.execute(db.text(create_table_sql))
                conn.commit()
            print("✅ Created departments table")
            
            # Insert default departments
            print("\nInserting default departments...")
            default_departments = [
                ('IT', 'IT', 'Phòng Công Nghệ Thông Tin'),
                ('HR', 'Nhân Sự', 'Phòng Nhân Sự'),
                ('ACC', 'Kế Toán', 'Phòng Kế Toán'),
                ('SALES', 'Kinh Doanh', 'Phòng Kinh Doanh'),
                ('PROD', 'Sản Xuất', 'Phòng Sản Xuất'),
                ('QC', 'Kiểm Soát Chất Lượng', 'Phòng Kiểm Soát Chất Lượng'),
                ('WAREHOUSE', 'Kho Vận', 'Phòng Kho Vận'),
                ('TECH', 'Kỹ Thuật Sản Xuất', 'Phòng Kỹ Thuật Sản Xuất')
            ]
            
            for code, name, description in default_departments:
                try:
                    with db.engine.connect() as conn:
                        conn.execute(db.text(
                            "INSERT INTO departments (code, name, description) VALUES (:code, :name, :description)"
                        ), {"code": code, "name": name, "description": description})
                        conn.commit()
                    print(f"✅ Added department: {name}")
                except Exception as e:
                    print(f"⚠️  Department {name} may already exist: {e}")
            
            print("\n" + "="*60)
            print("✅ Departments table created successfully!")
            
            # Show departments
            print("\nDepartments in table:")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT id, code, name, description FROM departments ORDER BY name"))
                for row in result:
                    print(f"  {row[0]}: {row[1]} - {row[2]} ({row[3]})")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            raise

if __name__ == '__main__':
    create_departments_table()