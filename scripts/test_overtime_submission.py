#!/usr/bin/env python3
"""
Test script to verify overtime submission works correctly
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, OvertimeRequest
from datetime import datetime, timedelta

def test_overtime_submission():
    """Test overtime submission for different user types"""
    with app.app_context():
        print("=" * 60)
        print("Testing Overtime Submission")
        print("=" * 60)
        
        # Test 1: Check user with overtime permission
        print("\n[TEST 1] Check IT department users")
        print("-" * 60)
        it_users = User.query.join(User.dept).filter(
            User.dept.has(name='Phòng IT'),
            User.is_active == True
        ).all()
        
        for user in it_users:
            dept_name = user.dept.name if user.dept else 'No department'
            pos_name = user.pos.name if user.pos else 'No position'
            approver_info = "Self-approve" if user.can_approve else f"Approver ID: {user.overtime_approver_id}"
            
            print(f"\n{user.name} ({user.employee_id})")
            print(f"  Department: {dept_name}")
            print(f"  Position: {pos_name}")
            print(f"  Can approve: {user.can_approve}")
            print(f"  {approver_info}")
            
            # Check if user can submit overtime
            can_submit = user.can_approve or user.overtime_approver_id is not None
            status = "✅ CAN SUBMIT" if can_submit else "❌ CANNOT SUBMIT"
            print(f"  Status: {status}")
        
        # Test 2: Simulate overtime submission
        print("\n\n[TEST 2] Simulate Overtime Submission")
        print("-" * 60)
        
        # Get a test user (10197)
        test_user = User.query.filter_by(employee_id='10197').first()
        if test_user:
            print(f"\nTest user: {test_user.name} ({test_user.employee_id})")
            print(f"Department: {test_user.dept.name if test_user.dept else 'None'}")
            print(f"Position: {test_user.pos.name if test_user.pos else 'None'}")
            print(f"Can approve: {test_user.can_approve}")
            print(f"Overtime approver ID: {test_user.overtime_approver_id}")
            
            # Check if can submit
            if test_user.can_approve:
                print("\n✅ User is manager - can self-approve")
            elif test_user.overtime_approver_id:
                approver = db.session.get(User, test_user.overtime_approver_id)
                if approver:
                    print(f"\n✅ User has approver: {approver.name} ({approver.employee_id})")
                else:
                    print(f"\n⚠️  Approver ID {test_user.overtime_approver_id} not found!")
            else:
                print("\n❌ User cannot submit - no approver assigned")
        else:
            print("Test user 10197 not found!")
        
        # Test 3: Check recent overtime requests
        print("\n\n[TEST 3] Recent Overtime Requests")
        print("-" * 60)
        recent_requests = OvertimeRequest.query.order_by(
            OvertimeRequest.created_at.desc()
        ).limit(5).all()
        
        if recent_requests:
            for req in recent_requests:
                print(f"\nID: {req.id}")
                print(f"  User: {req.employee_name} ({req.employee_id})")
                print(f"  Department: {req.department}")
                print(f"  Date: {req.overtime_date}")
                print(f"  People: {req.number_of_people}")
                print(f"  Status: {req.status}")
                print(f"  Created: {req.created_at}")
        else:
            print("No overtime requests found")
        
        print("\n" + "=" * 60)
        print("Test completed!")
        print("=" * 60)

if __name__ == '__main__':
    test_overtime_submission()
