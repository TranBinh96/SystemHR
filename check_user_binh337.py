#!/usr/bin/env python3
"""Check user binh337 information"""

from app import app, db
from models import User

with app.app_context():
    # Find user binh337
    user = User.query.filter_by(employee_id='binh337').first()
    
    if user:
        print("=" * 60)
        print(f"User Information for: {user.employee_id}")
        print("=" * 60)
        print(f"ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Department: {user.department}")
        print(f"Position: {user.position}")
        print(f"Role: {user.role}")
        print(f"Work Status: {user.work_status}")
        print(f"Is Active: {user.is_active}")
        print(f"Gender: {user.gender}")
        print("=" * 60)
        
        # Check subordinates
        subordinates = user.get_subordinates()
        print(f"\nSubordinates: {len(subordinates)}")
        for sub in subordinates:
            print(f"  - {sub.employee_id} ({sub.name}) - Position: {sub.position}")
        
        # Check if is manager
        print(f"\nIs Manager: {user.is_manager()}")
        
        # Check if highest level in department
        if user.position and user.department:
            try:
                my_code = int(user.position)
                same_dept_users = User.query.filter(
                    User.department == user.department,
                    User.position.isnot(None),
                    User.is_active == True,
                    User.id != user.id
                ).all()
                
                print(f"\nUsers in same department ({user.department}):")
                for u in same_dept_users:
                    try:
                        u_code = int(u.position)
                        print(f"  - {u.employee_id} ({u.name}) - Position: {u.position} (code: {u_code})")
                    except:
                        print(f"  - {u.employee_id} ({u.name}) - Position: {u.position} (invalid code)")
                
                is_highest = True
                for u in same_dept_users:
                    try:
                        u_code = int(u.position)
                        if u_code < my_code:
                            is_highest = False
                            print(f"\n{u.employee_id} has lower code ({u_code} < {my_code}), so binh337 is NOT highest level")
                            break
                    except:
                        continue
                
                if is_highest:
                    print(f"\nbinh337 IS the highest level in department (code: {my_code})")
                
            except Exception as e:
                print(f"\nError checking position: {e}")
        
    else:
        print("User binh337 not found!")
