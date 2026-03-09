#!/usr/bin/env python3
"""Fix binh337 position to use code instead of name"""

from app import app, db
from models import User, Position

with app.app_context():
    # Find user binh337
    user = User.query.filter_by(employee_id='binh337').first()
    
    if user:
        print(f"Current position: {user.position}")
        
        # Check available positions
        positions = Position.query.order_by(Position.code).all()
        print("\nAvailable positions:")
        for pos in positions:
            print(f"  Code {pos.code}: {pos.name}")
        
        # "Trưởng Phòng" should be code 1 (highest level)
        # Let's find it
        truong_phong = Position.query.filter_by(name='Trưởng Phòng').first()
        if truong_phong:
            print(f"\nFound 'Trưởng Phòng' with code: {truong_phong.code}")
            user.position = str(truong_phong.code)
            db.session.commit()
            print(f"✓ Updated binh337 position to: {user.position}")
        else:
            # If not found, assume code 1 for highest level
            print("\n'Trưởng Phòng' not found in positions table")
            print("Setting position to '1' (assumed highest level)")
            user.position = '1'
            db.session.commit()
            print(f"✓ Updated binh337 position to: {user.position}")
    else:
        print("User binh337 not found!")
