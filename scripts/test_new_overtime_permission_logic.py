#!/usr/bin/env python3
"""
Test new overtime permission logic based on can_register field
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def test_new_permission_logic():
    """Test new overtime permission logic"""
    with app.app_context():
        print("=" * 60)
        print("Testing NEW Overtime Permission Logic")
        print("(Based on can_register field)")
        print("=" * 60)
        
        # Get all active users
        users = User.query.filter_by(is_active=True).all()
        
        can_access = []
        cannot_access = []
        
        for user in users:
            dept_name = user.dept.name if user.dept else 'No department'
            
            # NEW LOGIC: Check can_approve OR can_register
            has_permission = user.can_approve or user.can_register
            
            user_info = {
                'name': user.name,
                'employee_id': user.employee_id,
                'department': dept_name,
                'can_approve': user.can_approve,
                'can_register': user.can_register,
                'overtime_approver_id': user.overtime_approver_id
            }
            
            if has_permission:
                can_access.append(user_info)
            else:
                cannot_access.append(user_info)
        
        # Display results
        print(f"\n✅ Users CAN access overtime registration: {len(can_access)}")
        print("-" * 60)
        for u in can_access:
            if u['can_approve']:
                reason = "Manager (can_approve=True)"
            else:
                reason = "Has can_register=True"
            print(f"{u['name']} ({u['employee_id']}) - {u['department']}")
            print(f"  → {reason}")
            print(f"  → can_approve={u['can_approve']}, can_register={u['can_register']}")
        
        print(f"\n❌ Users CANNOT access overtime registration: {len(cannot_access)}")
        print("-" * 60)
        if cannot_access:
            for u in cannot_access:
                print(f"{u['name']} ({u['employee_id']}) - {u['department']}")
                print(f"  → can_approve={u['can_approve']}, can_register={u['can_register']}")
                if u['overtime_approver_id']:
                    print(f"  → Has overtime_approver_id={u['overtime_approver_id']} (IGNORED)")
        else:
            print("  (All users have permission)")
        
        # Summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Total active users: {len(users)}")
        print(f"Can access: {len(can_access)} ({len(can_access)*100//len(users) if users else 0}%)")
        print(f"Cannot access: {len(cannot_access)} ({len(cannot_access)*100//len(users) if users else 0}%)")
        
        print("\n" + "=" * 60)
        print("NEW PERMISSION LOGIC")
        print("=" * 60)
        print("User can access overtime if:")
        print("  can_approve = True  (Manager)")
        print("  OR")
        print("  can_register = True  (Has permission)")
        print("\nField 'overtime_approver_id' is NO LONGER used for permission check")
        
        # Specific check for user 10002
        print("\n" + "=" * 60)
        print("Specific Check: User 10002")
        print("=" * 60)
        user_10002 = User.query.filter_by(employee_id='10002').first()
        if user_10002:
            print(f"Name: {user_10002.name}")
            print(f"can_approve: {user_10002.can_approve}")
            print(f"can_register: {user_10002.can_register}")
            print(f"overtime_approver_id: {user_10002.overtime_approver_id}")
            
            has_permission = user_10002.can_approve or user_10002.can_register
            if has_permission:
                print(f"\n✅ User 10002 CAN access overtime")
            else:
                print(f"\n❌ User 10002 CANNOT access overtime")
                print("   → Need to set can_register=True in admin panel")

if __name__ == '__main__':
    test_new_permission_logic()
