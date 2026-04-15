#!/usr/bin/env python3
"""
Check permissions for user 10002
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def check_user_10002():
    """Check permissions for user 10002"""
    with app.app_context():
        print("=" * 60)
        print("Checking User 10002 Permissions")
        print("=" * 60)
        
        # Get user 10002
        user = User.query.filter_by(employee_id='10002').first()
        
        if not user:
            print("\n❌ User 10002 NOT FOUND!")
            return
        
        print(f"\n📋 User Information:")
        print(f"  Employee ID: {user.employee_id}")
        print(f"  Name: {user.name}")
        print(f"  Department: {user.dept.name if user.dept else 'No department'}")
        print(f"  Position: {user.pos.name if user.pos else 'No position'}")
        print(f"  Work Status: {user.work_status}")
        print(f"  Is Active: {user.is_active}")
        
        print(f"\n🔐 Permission Fields:")
        print(f"  can_approve: {user.can_approve}")
        print(f"  can_register: {user.can_register}")
        print(f"  overtime_approver_id: {user.overtime_approver_id}")
        
        # Check if has approver
        if user.overtime_approver_id:
            approver = db.session.get(User, user.overtime_approver_id)
            if approver:
                print(f"\n👤 Overtime Approver:")
                print(f"  Name: {approver.name}")
                print(f"  Employee ID: {approver.employee_id}")
                print(f"  Department: {approver.dept.name if approver.dept else 'No department'}")
                print(f"  Can Approve: {approver.can_approve}")
            else:
                print(f"\n⚠️  Approver ID {user.overtime_approver_id} exists but user not found!")
        else:
            print(f"\n⚠️  No overtime approver assigned")
        
        # Check permission
        print(f"\n{'=' * 60}")
        print("Permission Check Results")
        print(f"{'=' * 60}")
        
        can_register_overtime = user.can_approve or user.overtime_approver_id is not None
        
        if can_register_overtime:
            print("\n✅ User 10002 CAN register overtime")
            if user.can_approve:
                print("   Reason: User is manager (can_approve=True)")
            else:
                print(f"   Reason: Has overtime approver (ID: {user.overtime_approver_id})")
            
            print("\n📱 UI Visibility:")
            print("   ✅ Will see 'Làm thêm' in sidebar menu")
            print("   ✅ Will see 'Làm Thêm' card in dashboard")
            print("   ✅ Will see overtime icon in mobile bottom nav")
            print("   ✅ Can access /overtime page")
        else:
            print("\n❌ User 10002 CANNOT register overtime")
            print("   Reason: No approver assigned and not a manager")
            
            print("\n📱 UI Visibility:")
            print("   ❌ Will NOT see 'Làm thêm' in sidebar menu")
            print("   ❌ Will NOT see 'Làm Thêm' card in dashboard")
            print("   ❌ Will NOT see overtime icon in mobile bottom nav")
            print("   ❌ Cannot access /overtime page (will be redirected)")
        
        print("\n" + "=" * 60)

if __name__ == '__main__':
    check_user_10002()
