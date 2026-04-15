#!/usr/bin/env python3
"""
Test script to verify department filtering for overtime approvers
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Department

def test_department_filter():
    """Test the department filter in /api/users endpoint"""
    with app.app_context():
        print("=" * 60)
        print("Testing Department Filter for Overtime Approvers")
        print("=" * 60)
        
        # Get all departments
        departments = Department.query.all()
        print(f"\nFound {len(departments)} departments:")
        for dept in departments:
            print(f"  - {dept.name} (ID: {dept.id})")
        
        # For each department, show managers
        for dept in departments:
            print(f"\n{'=' * 60}")
            print(f"Department: {dept.name}")
            print(f"{'=' * 60}")
            
            # Get all users in this department
            all_users = User.query.filter_by(
                department_id=dept.id,
                is_active=True
            ).all()
            
            # Get managers (can_approve=True) in this department
            managers = User.query.filter_by(
                department_id=dept.id,
                is_active=True,
                can_approve=True
            ).all()
            
            print(f"Total active users: {len(all_users)}")
            print(f"Managers (can_approve=True): {len(managers)}")
            
            if managers:
                print("\nManagers in this department:")
                for mgr in managers:
                    print(f"  - {mgr.name} ({mgr.employee_id})")
            else:
                print("\n⚠️  WARNING: No managers found in this department!")
            
            # Show regular users who need approvers
            regular_users = [u for u in all_users if not u.can_approve]
            if regular_users:
                print(f"\nRegular users ({len(regular_users)}):")
                for user in regular_users[:5]:  # Show first 5
                    approver_name = "Not assigned"
                    if user.overtime_approver_id:
                        approver = User.query.get(user.overtime_approver_id)
                        if approver:
                            approver_name = f"{approver.name} ({approver.employee_id})"
                    print(f"  - {user.name} ({user.employee_id}) -> Approver: {approver_name}")
                
                if len(regular_users) > 5:
                    print(f"  ... and {len(regular_users) - 5} more users")
        
        print("\n" + "=" * 60)
        print("Test completed!")
        print("=" * 60)

if __name__ == '__main__':
    test_department_filter()
