#!/usr/bin/env python3
"""
Script to enable overtime registration permission for users
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def enable_overtime_permission(employee_id):
    """Enable overtime registration permission for a user"""
    with app.app_context():
        user = User.query.filter_by(employee_id=employee_id).first()
        
        if not user:
            print(f"❌ User {employee_id} không tồn tại")
            return False
        
        print(f"\n{'='*60}")
        print(f"BẬT QUYỀN ĐĂNG KÝ OVERTIME")
        print(f"{'='*60}")
        print(f"User: {user.name} ({user.employee_id})")
        print(f"\nTrước khi cập nhật:")
        print(f"  can_register_overtime: {user.can_register_overtime}")
        
        # Enable permission
        user.can_register_overtime = True
        
        try:
            db.session.commit()
            print(f"\n✅ ĐÃ CẬP NHẬT THÀNH CÔNG!")
            print(f"\nSau khi cập nhật:")
            print(f"  can_register_overtime: {user.can_register_overtime}")
            
            if user.overtime_approver_id:
                approver = User.query.get(user.overtime_approver_id)
                if approver:
                    print(f"  Người phê duyệt: {approver.name} ({approver.employee_id})")
                else:
                    print(f"  ⚠️  Người phê duyệt ID {user.overtime_approver_id} không tồn tại!")
            else:
                print(f"  ⚠️  Chưa có người phê duyệt - cần chỉ định trong admin!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ LỖI: {e}")
            return False

def enable_all_users():
    """Enable overtime permission for all active users"""
    with app.app_context():
        users = User.query.filter_by(is_active=True, work_status='working').all()
        
        print(f"\n{'='*60}")
        print(f"BẬT QUYỀN ĐĂNG KÝ OVERTIME CHO TẤT CẢ USER")
        print(f"{'='*60}")
        print(f"Tổng số user active: {len(users)}")
        
        updated = 0
        for user in users:
            if not user.can_register_overtime:
                user.can_register_overtime = True
                updated += 1
                print(f"  ✓ {user.employee_id} - {user.name}")
        
        if updated > 0:
            try:
                db.session.commit()
                print(f"\n✅ Đã cập nhật {updated} user")
            except Exception as e:
                db.session.rollback()
                print(f"\n❌ LỖI: {e}")
        else:
            print(f"\n✓ Tất cả user đã có quyền đăng ký overtime")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            enable_all_users()
        else:
            employee_id = sys.argv[1]
            enable_overtime_permission(employee_id)
    else:
        print("Usage:")
        print("  python scripts/enable_overtime_permission.py 10197")
        print("  python scripts/enable_overtime_permission.py --all")
