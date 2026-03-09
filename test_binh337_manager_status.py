#!/usr/bin/env python3
"""Test if binh337 should see approval menu"""

from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(employee_id='binh337').first()
    
    if not user:
        print("User binh337 not found!")
        exit(1)
    
    print("=" * 60)
    print(f"Testing approval access for: {user.employee_id}")
    print("=" * 60)
    print(f"Name: {user.name}")
    print(f"Department: {user.department}")
    print(f"Position: {user.position}")
    print(f"Role: {user.role}")
    print("=" * 60)
    
    # Test 1: is_manager()
    is_manager = user.is_manager()
    print(f"\n1. is_manager(): {is_manager}")
    
    subordinates = user.get_subordinates()
    print(f"   Subordinates count: {len(subordinates)}")
    for sub in subordinates:
        print(f"   - {sub.employee_id} ({sub.name}) - Position: {sub.position}")
    
    # Test 2: Check if highest level
    is_highest = False
    if user.position and user.department:
        try:
            my_code = int(user.position)
            same_dept_users = User.query.filter(
                User.department == user.department,
                User.position.isnot(None),
                User.is_active == True,
                User.id != user.id
            ).all()
            
            print(f"\n2. Checking if highest level in department:")
            print(f"   My position code: {my_code}")
            print(f"   Users in same department: {len(same_dept_users)}")
            
            is_highest = True
            for u in same_dept_users:
                try:
                    u_code = int(u.position)
                    print(f"   - {u.employee_id}: position code {u_code}")
                    if u_code < my_code:
                        is_highest = False
                        print(f"     ^ This user has lower code, so binh337 is NOT highest")
                except (ValueError, TypeError) as e:
                    print(f"   - {u.employee_id}: invalid position '{u.position}' - {e}")
                    continue
            
            print(f"\n   Result: is_highest = {is_highest}")
        except (ValueError, TypeError) as e:
            print(f"\n2. Error checking position: {e}")
    
    # Final result
    print("\n" + "=" * 60)
    should_see_approval = is_manager or is_highest
    print(f"FINAL: Should see approval menu? {should_see_approval}")
    print(f"  - is_manager: {is_manager}")
    print(f"  - is_highest: {is_highest}")
    print("=" * 60)
    
    if should_see_approval:
        print("\n✓ binh337 SHOULD see the approval menu")
        print("  If not showing, try:")
        print("  1. Clear browser cache (Ctrl+Shift+Delete)")
        print("  2. Logout and login again")
        print("  3. Check browser console for errors (F12)")
    else:
        print("\n✗ binh337 should NOT see the approval menu")
        print("  Reason: Not a manager and not highest level in department")
