#!/usr/bin/env python3
"""Quick setup users for testing"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Department, Position

with app.app_context():
    # Get departments and positions
    it_dept = Department.query.filter_by(code='IT').first()
    prod_dept = Department.query.filter_by(code='PROD').first()
    
    truong_phong = Position.query.filter_by(name='Trưởng phòng').first()
    nhan vien = Position.query.filter_by(name='Nhân viên').first()
    cong_nhan = Position.query.filter_by(name='Công nhân').first()
    
    print("Setting up users...")
    print(f"IT Department ID: {it_dept.id if it_dept else 'NOT FOUND'}")
    print(f"PROD Department ID: {prod_dept.id if prod_dept else 'NOT FOUND'}")
    print(f"Trưởng phòng: Level {truong_phong.level if truong_phong else 'NOT FOUND'}")
    print(f"Nhân viên: Level {nhan_vien.level if nhan_vien else 'NOT FOUND'}")
    print(f"Công nhân: Level {cong_nhan.level if cong_nhan else 'NOT FOUND'}")
    print()
    
    # Setup binh337 as Trưởng phòng IT (Level 2)
    binh = User.query.filter_by(employee_id='binh337').first()
    if binh and it_dept and truong_phong:
        binh.department_id = it_dept.id
        binh.department = it_dept.name
        binh.position_id = truong_phong.id
        binh.position = truong_phong.name
        binh.level = truong_phong.level
        print(f"✓ {binh.name}: {truong_phong.name} (Level {binh.level}) - {it_dept.name}")
    
    # Setup EMP001 as Công nhân IT (Level 5)
    emp001 = User.query.filter_by(employee_id='EMP001').first()
    if emp001 and it_dept and cong_nhan:
        emp001.department_id = it_dept.id
        emp001.department = it_dept.name
        emp001.position_id = cong_nhan.id
        emp001.position = cong_nhan.name
        emp001.level = cong_nhan.level
        print(f"✓ {emp001.name}: {cong_nhan.name} (Level {emp001.level}) - {it_dept.name}")
    
    # Setup ADMIN as Trưởng phòng PROD (Level 2)
    admin = User.query.filter_by(employee_id='ADMIN').first()
    if admin and prod_dept and truong_phong:
        admin.department_id = prod_dept.id
        admin.department = prod_dept.name
        admin.position_id = truong_phong.id
        admin.position = truong_phong.name
        admin.level = truong_phong.level
        print(f"✓ {admin.name}: {truong_phong.name} (Level {admin.level}) - {prod_dept.name}")
    
    db.session.commit()
    print("\n✓ Done! Users updated successfully")
    
    # Show who can approve for whom
    print("\n" + "="*60)
    print("Approval hierarchy:")
    print("="*60)
    for user in User.query.order_by(User.department_id, User.level).all():
        subordinates = user.get_subordinates()
        if subordinates:
            print(f"\n{user.name} (Level {user.level}) can approve for:")
            for sub in subordinates:
                print(f"  → {sub.name} (Level {sub.level})")
