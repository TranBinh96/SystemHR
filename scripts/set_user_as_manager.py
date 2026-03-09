#!/usr/bin/env python3
"""
Script to set a user as manager (lower level)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Position

def set_user_as_manager(employee_id, position_name='Trưởng phòng', level=2):
    """Set a user as manager with specified position and level"""
    with app.app_context():
        try:
            # Find user
            user = User.query.filter_by(employee_id=employee_id).first()
            if not user:
                print(f"[ERROR] User {employee_id} not found")
                return
            
            # Find position
            position = Position.query.filter_by(name=position_name).first()
            
            print(f"Setting {user.name} ({employee_id}) as {position_name} (Level {level})")
            print(f"Current: Dept_ID={user.department_id}, Level={user.level}")
            
            # Update user
            if position:
                user.position_id = position.id
                user.level = position.level
            else:
                user.level = level
            
            user.position = position_name  # Legacy field
            
            db.session.commit()
            
            print(f"[OK] Updated: Dept_ID={user.department_id}, Level={user.level}")
            print(f"\nUser can now approve for:")
            subordinates = user.get_subordinates()
            if subordinates:
                for sub in subordinates:
                    print(f"  - {sub.name} ({sub.employee_id}) Level {sub.level}")
            else:
                print("  (No subordinates - need users with higher level in same department)")
            
        except Exception as e:
            print(f"\n[ERROR] Failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python set_user_as_manager.py <employee_id> [position_name] [level]")
        print("\nExamples:")
        print("  python set_user_as_manager.py ADMIN")
        print("  python set_user_as_manager.py binh337 'Trưởng phòng' 2")
        print("  python set_user_as_manager.py EMP001 'Nhân viên' 4")
        sys.exit(1)
    
    employee_id = sys.argv[1]
    position_name = sys.argv[2] if len(sys.argv) > 2 else 'Trưởng phòng'
    level = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    set_user_as_manager(employee_id, position_name, level)
