#!/usr/bin/env python3
"""
Test script to verify overtime permission logic
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def test_overtime_permission():
    """Test who can and cannot access overtime registration"""
    with app.app_context():
        print("=" * 60)
        print("Testing Overtime Permission Logic")
        print("=" * 60)
        
        # Get all active users
        users = User.query.filter_by(is_active=True).all()
        
        can_access = []
        cannot_access = []
        
        for user in users:
            dept_name = user.dept.name if user.dept else 'No department'
            
            # Check permission
            has_permission = user.can_approve or user.overtime_approver_id is not None
            
            user_info = {
                'name': user.name,
                'employee_id': user.employee_id,
                'department': dept_name,
                'can_approve': user.can_approve,
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
            reason = "Manager (self-approve)" if u['can_approve'] else f"Has approver (ID: {u['overtime_approver_id']})"
            print(f"{u['name']} ({u['employee_id']}) - {u['department']}")
            print(f"  → {reason}")
        
        print(f"\n❌ Users CANNOT access overtime registration: {len(cannot_access)}")
        print("-" * 60)
        if cannot_access:
            for u in cannot_access:
                print(f"{u['name']} ({u['employee_id']}) - {u['department']}")
                print(f"  → No approver assigned")
        else:
            print("  (All users have permission)")
        
        # Summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Total active users: {len(users)}")
        print(f"Can access: {len(can_access)} ({len(can_access)*100//len(users) if users else 0}%)")
        print(f"Cannot access: {len(cannot_access)} ({len(cannot_access)*100//len(users) if users else 0}%)")
        
        if cannot_access:
            print("\n⚠️  WARNING: Some users cannot access overtime registration!")
            print("   Admin needs to assign overtime approvers for these users.")
        else:
            print("\n✅ All active users have overtime registration permission!")

if __name__ == '__main__':
    test_overtime_permission()
