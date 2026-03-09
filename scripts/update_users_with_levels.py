#!/usr/bin/env python3
"""
Script to update existing users with department_id, position_id, and level
This maps legacy department strings to new department IDs and assigns levels
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Department, Position

def update_users_with_levels():
    """Update users with department_id, position_id, and level"""
    with app.app_context():
        try:
            print("Updating users with department and level information...")
            print("="*60)
            
            # Get all departments and positions
            departments = {d.code.lower(): d for d in Department.query.all()}
            positions = {p.name.lower(): p for p in Position.query.all()}
            
            # Department mapping (legacy string -> department code)
            dept_mapping = {
                'it': 'IT',
                'công nghệ thông tin': 'IT',
                'hr': 'HR',
                'nhân sự': 'HR',
                'production': 'PROD',
                'sản xuất': 'PROD',
                'warehouse': 'WAREHOUSE',
                'kho': 'WAREHOUSE',
                'qc': 'QC',
                'kiểm soát chất lượng': 'QC',
                'admin': 'ADMIN',
                'hành chính': 'ADMIN'
            }
            
            users = User.query.all()
            updated_count = 0
            
            for user in users:
                updated = False
                
                # Update department_id if not set
                if not user.department_id and user.department:
                    dept_key = user.department.lower().strip()
                    dept_code = dept_mapping.get(dept_key, 'ADMIN')
                    
                    if dept_code.lower() in departments:
                        user.department_id = departments[dept_code.lower()].id
                        updated = True
                        print(f"  User {user.employee_id}: Set department to {dept_code}")
                
                # Update position_id and level if not set
                if not user.position_id and user.position:
                    # Try to find matching position
                    pos_key = user.position.lower().strip()
                    
                    # Direct match
                    if pos_key in positions:
                        user.position_id = positions[pos_key].id
                        user.level = positions[pos_key].level
                        updated = True
                        print(f"  User {user.employee_id}: Set position to {positions[pos_key].name} (Level {user.level})")
                    else:
                        # Partial match
                        for pos_name, pos_obj in positions.items():
                            if pos_key in pos_name or pos_name in pos_key:
                                user.position_id = pos_obj.id
                                user.level = pos_obj.level
                                updated = True
                                print(f"  User {user.employee_id}: Set position to {pos_obj.name} (Level {user.level})")
                                break
                
                # Set default level if still not set
                if not user.level:
                    # Admin gets level 1, others get level 4 (default employee)
                    user.level = 1 if user.role == 'admin' else 4
                    updated = True
                    print(f"  User {user.employee_id}: Set default level to {user.level}")
                
                if updated:
                    updated_count += 1
            
            db.session.commit()
            
            print("="*60)
            print(f"\n[OK] Updated {updated_count} users")
            
            # Print summary
            print("\nUser Summary by Department and Level:")
            print("-"*60)
            
            for dept in Department.query.order_by(Department.code).all():
                dept_users = User.query.filter_by(department_id=dept.id).order_by(
                    User.level.asc(), User.name.asc()
                ).all()
                
                if dept_users:
                    print(f"\n{dept.name} ({dept.code}):")
                    for user in dept_users:
                        pos_name = user.pos.name if user.pos else user.position
                        print(f"  Level {user.level}: {user.name} ({user.employee_id}) - {pos_name}")
            
            # Users without department
            no_dept_users = User.query.filter_by(department_id=None).all()
            if no_dept_users:
                print(f"\nUsers without department ({len(no_dept_users)}):")
                for user in no_dept_users:
                    print(f"  {user.name} ({user.employee_id})")
            
        except Exception as e:
            print(f"\n[ERROR] Update failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    update_users_with_levels()
