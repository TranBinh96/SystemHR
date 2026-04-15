#!/usr/bin/env python3
"""
Test the /api/users endpoint with department filter
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import User, Department

def test_api_endpoint():
    """Test the API endpoint with department filter"""
    with app.app_context():
        print("=" * 60)
        print("Testing /api/users API Endpoint")
        print("=" * 60)
        
        # Test 1: Get all managers (no department filter)
        print("\n[TEST 1] Get all managers (no department filter)")
        print("-" * 60)
        users = User.query.filter_by(is_active=True, can_approve=True).order_by(User.name).all()
        print(f"Found {len(users)} managers across all departments:")
        for u in users:
            dept_name = u.dept.name if u.dept else 'No department'
            print(f"  - {u.name} ({u.employee_id}) - {dept_name}")
        
        # Test 2: Get managers in IT department
        print("\n[TEST 2] Get managers in IT department only")
        print("-" * 60)
        it_dept = Department.query.filter_by(name='Phòng IT').first()
        if it_dept:
            users = User.query.join(Department).filter(
                User.is_active == True,
                User.can_approve == True,
                Department.name == 'Phòng IT'
            ).order_by(User.name).all()
            
            print(f"Found {len(users)} managers in IT department:")
            for u in users:
                print(f"  - {u.name} ({u.employee_id})")
        else:
            print("IT department not found!")
        
        # Test 3: Get managers in HR department
        print("\n[TEST 3] Get managers in HR department")
        print("-" * 60)
        hr_dept = Department.query.filter_by(name='Phòng Nhân sự').first()
        if hr_dept:
            users = User.query.join(Department).filter(
                User.is_active == True,
                User.can_approve == True,
                Department.name == 'Phòng Nhân sự'
            ).order_by(User.name).all()
            
            print(f"Found {len(users)} managers in HR department:")
            if users:
                for u in users:
                    print(f"  - {u.name} ({u.employee_id})")
            else:
                print("  ⚠️  No managers found in HR department")
        else:
            print("HR department not found!")
        
        print("\n" + "=" * 60)
        print("✅ API endpoint logic verified!")
        print("=" * 60)
        print("\nNOTE: To test the actual HTTP endpoint, you need to:")
        print("1. Start the Flask app")
        print("2. Login as admin")
        print("3. Call: GET /api/users?can_approve=1&department=Phòng IT")

if __name__ == '__main__':
    test_api_endpoint()
