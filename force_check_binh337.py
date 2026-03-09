#!/usr/bin/env python3
"""Force check binh337 approval status"""

from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(employee_id='binh337').first()
    
    if not user:
        print("❌ User binh337 not found!")
        exit(1)
    
    print("=" * 70)
    print(f"CHECKING APPROVAL ACCESS FOR: {user.employee_id}")
    print("=" * 70)
    print(f"Name: {user.name}")
    print(f"Position: {user.position}")
    print(f"Position type: {type(user.position)}")
    print(f"Department: {user.department}")
    print(f"Role: {user.role}")
    print("=" * 70)
    
    # Check condition 1: position == '1'
    check1 = (user.position == '1')
    print(f"\n✓ Check 1: position == '1'")
    print(f"  Result: {check1}")
    print(f"  Comparison: '{user.position}' == '1' → {check1}")
    
    # Check condition 2: is_manager()
    check2 = user.is_manager()
    print(f"\n✓ Check 2: is_manager()")
    print(f"  Result: {check2}")
    subordinates = user.get_subordinates()
    print(f"  Subordinates: {len(subordinates)}")
    
    # Final result
    print("\n" + "=" * 70)
    should_see = check1 or check2
    print(f"FINAL RESULT: Should see approval menu? {should_see}")
    print(f"  - position == '1': {check1}")
    print(f"  - is_manager(): {check2}")
    print("=" * 70)
    
    if should_see:
        print("\n✅ binh337 SHOULD see approval menu!")
        print("\nIf still not showing:")
        print("1. Restart Flask server (Ctrl+C then run again)")
        print("2. Clear browser cache completely")
        print("3. Logout and login again")
        print("4. Try incognito/private window")
    else:
        print("\n❌ binh337 should NOT see approval menu")
        print(f"\nProblem: position is '{user.position}' (type: {type(user.position).__name__})")
        print("Expected: position should be string '1'")
