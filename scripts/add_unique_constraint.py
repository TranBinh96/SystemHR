#!/usr/bin/env python3
"""
Script để thêm UNIQUE constraint cho bảng meal_registrations
Ngăn chặn việc tạo nhiều đăng ký cho cùng user trong cùng ngày
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db
from sqlalchemy import text

def add_unique_constraint():
    """Thêm UNIQUE constraint vào bảng meal_registrations"""
    
    with app.app_context():
        try:
            print("\n=== THÊM UNIQUE CONSTRAINT ===")
            
            # Kiểm tra xem constraint đã tồn tại chưa
            check_constraint_sql = """
            SELECT COUNT(*) as count
            FROM information_schema.table_constraints 
            WHERE constraint_name = 'unique_user_date_meal' 
            AND table_name = 'meal_registrations'
            """
            
            result = db.session.execute(text(check_constraint_sql)).fetchone()
            
            if result and result.count > 0:
                print("✅ UNIQUE constraint đã tồn tại!")
                return
            
            print("🔧 Đang thêm UNIQUE constraint...")
            
            # Thêm constraint
            add_constraint_sql = """
            ALTER TABLE meal_registrations 
            ADD CONSTRAINT unique_user_date_meal 
            UNIQUE (user_id, date)
            """
            
            db.session.execute(text(add_constraint_sql))
            db.session.commit()
            
            print("✅ Đã thêm UNIQUE constraint thành công!")
            print("📋 Constraint: unique_user_date_meal (user_id, date)")
            
        except Exception as e:
            print(f"❌ Lỗi khi thêm constraint: {str(e)}")
            db.session.rollback()
            
            # Nếu lỗi do duplicate data, hướng dẫn user
            if "Duplicate entry" in str(e) or "UNIQUE constraint failed" in str(e):
                print("\n⚠️  LỖI: Có dữ liệu duplicate trong database!")
                print("🔧 Hãy chạy script dọn dẹp trước:")
                print("   python scripts/cleanup_duplicate_meals.py --cleanup")
                print("   Sau đó chạy lại script này.")

def check_constraint_status():
    """Kiểm tra trạng thái constraint"""
    
    with app.app_context():
        try:
            print("\n=== KIỂM TRA CONSTRAINT ===")
            
            # Kiểm tra constraint
            check_sql = """
            SELECT 
                constraint_name,
                constraint_type,
                table_name
            FROM information_schema.table_constraints 
            WHERE table_name = 'meal_registrations'
            AND constraint_type = 'UNIQUE'
            """
            
            constraints = db.session.execute(text(check_sql)).fetchall()
            
            if constraints:
                print("📋 UNIQUE constraints hiện tại:")
                for constraint in constraints:
                    print(f"  - {constraint.constraint_name} ({constraint.constraint_type})")
            else:
                print("❌ Không có UNIQUE constraint nào!")
                
            # Kiểm tra có duplicate không
            duplicate_check_sql = """
            SELECT 
                user_id, 
                date, 
                COUNT(*) as count
            FROM meal_registrations 
            GROUP BY user_id, date 
            HAVING COUNT(*) > 1
            LIMIT 5
            """
            
            duplicates = db.session.execute(text(duplicate_check_sql)).fetchall()
            
            if duplicates:
                print(f"\n⚠️  Tìm thấy {len(duplicates)} nhóm duplicate (hiển thị 5 đầu tiên):")
                for dup in duplicates:
                    print(f"  User {dup.user_id}, ngày {dup.date}: {dup.count} đăng ký")
                print("\n🔧 Cần dọn dẹp duplicate trước khi thêm constraint!")
            else:
                print("\n✅ Không có duplicate data!")
                
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Thêm UNIQUE constraint cho meal_registrations')
    parser.add_argument('--check', action='store_true', help='Kiểm tra trạng thái constraint')
    parser.add_argument('--add', action='store_true', help='Thêm constraint')
    
    args = parser.parse_args()
    
    if args.check:
        check_constraint_status()
    elif args.add:
        check_constraint_status()
        add_unique_constraint()
    else:
        print("Sử dụng:")
        print("  python add_unique_constraint.py --check   # Kiểm tra trạng thái")
        print("  python add_unique_constraint.py --add     # Thêm constraint")