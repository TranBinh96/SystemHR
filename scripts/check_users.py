#!/usr/bin/env python3
"""Check current users and their levels"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Position

def check_users():
    with app.app_context():
        users = User.query.all()
        print("\n" + "="*80)
        print("CURRENT USERS:")
        print("="*80)
        print(f"{'Employee ID':<12} {'Name':<20} {'Department':<25} {'Pos Code':<10}")
        print("-"*80)
        
        for u in users:
            print(f"{u.employee_id:<12} {u.name:<20} {u.department or 'N/A':<25} {u.position or 'N/A':<10}")
        
        print("\n" + "="*80)
        print("APPROVAL LOGIC TEST:")
        print("="*80)
        
        # Test approval logic
        for u in users:
            if u.position and u.department:
                approvers = u.get_approvers()
                subordinates = u.get_subordinates()
                
                print(f"\n{u.employee_id} ({u.name}):")
                print(f"  Department: {u.department}")
                print(f"  Position Code: {u.position}")
                
                if approvers:
                    print(f"  Can be approved by: {', '.join([f'{a.employee_id} (code={a.position})' for a in approvers])}")
                else:
                    print(f"  Can be approved by: (none - highest level in department)")
                
                if subordinates:
                    print(f"  Can approve for: {', '.join([f'{s.employee_id} (code={s.position})' for s in subordinates])}")
                else:
                    print(f"  Can approve for: (none - no subordinates)")

if __name__ == '__main__':
    check_users()
