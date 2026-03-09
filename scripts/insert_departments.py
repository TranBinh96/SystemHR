#!/usr/bin/env python3
"""Quick script to insert departments"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, Department

with app.app_context():
    # Check if departments exist
    if Department.query.count() > 0:
        print("Departments already exist")
    else:
        print("Inserting departments...")
        departments = [
            Department(code='IT', name='Công nghệ thông tin', description='Phòng IT'),
            Department(code='HR', name='Nhân sự', description='Phòng nhân sự'),
            Department(code='PROD', name='Sản xuất', description='Phòng sản xuất'),
            Department(code='WAREHOUSE', name='Kho', description='Phòng kho'),
            Department(code='QC', name='Kiểm soát chất lượng', description='Phòng QC'),
            Department(code='ADMIN', name='Hành chính', description='Phòng hành chính')
        ]
        
        for dept in departments:
            db.session.add(dept)
        
        db.session.commit()
        print(f"Inserted {len(departments)} departments")
        
        for d in Department.query.all():
            print(f"  {d.code}: {d.name}")
