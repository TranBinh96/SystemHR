#!/usr/bin/env python3
"""
Script to check user overtime permissions
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def check_user_permission(employee_id):
    """Check overtime permission for a specific user"""
    with app.app_context():
        user = User.query.filter_by(employee_id=employee_id).first()
        
        if not user:
            print(f"❌ User {employee_id} không tồn tại")
            return
        
        print(f"\n{'='*60}")
        print(f"THÔNG TIN USER: {employee_id}")
        print(f"{'='*60}")
        print(f"ID: {user.id}")
        print(f"Tên: {user.name}")
        print(f"Mã NV: {user.employee_id}")
        print(f"Phòng ban: {user.dept.name if user.dept else 'Chưa có'}")
        print(f"Chức vụ: {user.pos.name if user.pos else 'Chưa có'}")
        print(f"Role: {user.role}")
        print(f"Trạng thái: {user.work_status}")
        print(f"Is Active: {user.is_active}")
        print(f"\n{'='*60}")
        print(f"QUYỀN OVERTIME")
        print(f"{'='*60}")
        print(f"can_register_overtime: {user.can_register_overtime}")
        print(f"can_approve: {user.can_approve}")
        print(f"overtime_approver_id: {user.overtime_approver_id}")
        
        if user.overtime_approver_id:
            approver = User.query.get(user.overtime_approver_id)
            if approver:
                print(f"Người phê duyệt: {approver.name} ({approver.employee_id})")
            else:
                print(f"⚠️  Người phê duyệt ID {user.overtime_approver_id} không tồn tại!")
        else:
            print(f"⚠️  Chưa có người phê duyệt được chỉ định")
        
        print(f"\n{'='*60}")
        print(f"KẾT LUẬN")
        print(f"{'='*60}")
        
        if not user.can_register_overtime:
            print(f"❌ User KHÔNG có quyền đăng ký overtime")
            print(f"   → Cần bật 'can_register_overtime' = True")
        elif not user.overtime_approver_id:
            print(f"⚠️  User có quyền đăng ký NHƯNG chưa có người phê duyệt")
            print(f"   → Cần chỉ định 'overtime_approver_id'")
        else:
            print(f"✅ User có đủ quyền đăng ký overtime")
            print(f"   - can_register_overtime: True")
            print(f"   - overtime_approver_id: {user.overtime_approver_id}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        employee_id = sys.argv[1]
    else:
        employee_id = '10197'  # Default
    
    check_user_permission(employee_id)
