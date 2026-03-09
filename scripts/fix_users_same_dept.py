#!/usr/bin/env python3
"""Fix users to be in same department with correct levels"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Department, Position

with app.app_context():
    # Get PROD department (Kỹ Thuật Sản Xuất)
    prod_dept = Department.query.filter_by(code='PROD').first()
    if not prod_dept:
        print("[ERROR] PROD department not found!")
        exit(1)
    
    # Get positions
    truong_phong = Position.query.filter_by(name='Trưởng phòng').first()
    cong_nhan = Position.query.filter_by(name='Công nhân').first()
    
    print(f"Setting both users to: {prod_dept.name} (ID: {prod_dept.id})")
    print()
    
    # Set binh337 as Trưởng phòng (Level 2)
    binh = User.query.filter_by(employee_id='binh337').first()
    if binh and truong_phong:
        binh.department_id = prod_dept.id
        binh.department = prod_dept.name
        binh.position_id = truong_phong.id
        binh.position = truong_phong.name
        binh.level = truong_phong.level
        print(f"✓ {binh.name}: {truong_phong.name} (Level {binh.level})")
    
    # Set EMP001 as Công nhân (Level 5)
    emp = User.query.filter_by(employee_id='EMP001').first()
    if emp and cong_nhan:
        emp.department_id = prod_dept.id
        emp.department = prod_dept.name
        emp.position_id = cong_nhan.id
        emp.position = cong_nhan.name
        emp.level = cong_nhan.level
        print(f"✓ {emp.name}: {cong_nhan.name} (Level {emp.level})")
    
    db.session.commit()
    
    print("\n" + "="*60)
    print("Testing approval logic:")
    print("="*60)
    print(f"Cùng phòng: {binh.department_id == emp.department_id}")
    print(f"{binh.name} có thể duyệt {emp.name}: {binh.can_approve_for(emp)}")
    print(f"\nSubordinates của {binh.name}:")
    for sub in binh.get_subordinates():
        print(f"  → {sub.name} (Level {sub.level})")
