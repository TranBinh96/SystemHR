#!/usr/bin/env python3
"""
Script to check overtime permissions for IT department users
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Department

def check_it_department():
    """Check all users in IT department"""
    with app.app_context():
        # Find IT department
        it_dept = Department.query.filter(
            (Department.name.like('%IT%')) | 
            (Department.code.like('%IT%'))
        ).first()
        
        if not it_dept:
            print("❌ Không tìm thấy phòng IT")
            return
        
        print(f"\n{'='*80}")
        print(f"PHÒNG: {it_dept.name} (ID: {it_dept.id})")
        print(f"{'='*80}")
        
        # Get all users in IT department
        users = User.query.filter_by(
            department_id=it_dept.id,
            is_active=True
        ).order_by(User.employee_id).all()
        
        print(f"\nTổng số user: {len(users)}")
        print(f"\n{'─'*80}")
        
        managers = []
        users_with_approver = []
        users_without_approver = []
        
        for user in users:
            print(f"\n👤 {user.name} ({user.employee_id})")
            print(f"   Chức vụ: {user.pos.name if user.pos else 'Chưa có'}")
            print(f"   can_approve: {user.can_approve}")
            print(f"   overtime_approver_id: {user.overtime_approver_id}")
            
            if user.can_approve:
                managers.append(user)
                print(f"   ✅ MANAGER - Tự phê duyệt")
            elif user.overtime_approver_id:
                approver = User.query.get(user.overtime_approver_id)
                if approver:
                    users_with_approver.append(user)
                    print(f"   ✅ Có người phê duyệt: {approver.name} ({approver.employee_id})")
                else:
                    users_without_approver.append(user)
                    print(f"   ❌ Người phê duyệt ID {user.overtime_approver_id} KHÔNG TỒN TẠI!")
            else:
                users_without_approver.append(user)
                print(f"   ❌ CHƯA CÓ NGƯỜI PHÊ DUYỆT")
        
        print(f"\n{'='*80}")
        print(f"TỔNG KẾT")
        print(f"{'='*80}")
        print(f"👔 Manager (tự phê duyệt): {len(managers)}")
        for m in managers:
            print(f"   - {m.name} ({m.employee_id})")
        
        print(f"\n✅ User có người phê duyệt: {len(users_with_approver)}")
        for u in users_with_approver:
            approver = User.query.get(u.overtime_approver_id)
            print(f"   - {u.name} ({u.employee_id}) → {approver.name}")
        
        print(f"\n❌ User CHƯA có người phê duyệt: {len(users_without_approver)}")
        for u in users_without_approver:
            print(f"   - {u.name} ({u.employee_id})")
        
        if users_without_approver:
            print(f"\n⚠️  CẦN HÀNH ĐỘNG:")
            print(f"   Admin cần vào Admin → Users và chỉ định 'Người phê duyệt overtime'")
            print(f"   cho {len(users_without_approver)} user trên")

if __name__ == '__main__':
    check_it_department()
