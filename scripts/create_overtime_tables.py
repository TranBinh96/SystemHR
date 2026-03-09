#!/usr/bin/env python3
"""
Script to create overtime tables in the database
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

def create_overtime_tables():
    """Create overtime_requests and department_managers tables"""
    try:
        with app.app_context():
            print("Creating overtime tables...")
            
            # Read SQL file
            sql_file = os.path.join(os.path.dirname(__file__), 'create_overtime_table_mysql.sql')
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement separately
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    db.session.execute(db.text(statement))
            
            db.session.commit()
            
            print("✓ Overtime tables created successfully!")
            print("\nTables created:")
            print("  - overtime_requests: Lưu yêu cầu tăng ca")
            print("  - department_managers: Lưu thông tin trưởng phòng")
            print("\nQuy trình phê duyệt:")
            print("  1. Nhân viên gửi yêu cầu (status: pending)")
            print("  2. Trưởng phòng duyệt (status: approved/rejected)")
            print("  3. Admin xem tổng hợp (không cần duyệt)")
            print("\nLưu ý: Cần cập nhật bảng department_managers với thông tin trưởng phòng thực tế!")
        
    except Exception as e:
        print(f"✗ Error creating overtime tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    create_overtime_tables()
