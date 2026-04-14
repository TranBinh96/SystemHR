#!/usr/bin/env python3
"""
Script to migrate users from position codes to position_id and set levels
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Position

def migrate_users_to_position_id():
    """Migrate users from position codes to position_id and set levels"""
    with app.app_context():
        try:
            print("Migrating users to use position_id instead of position codes...")
            print("="*60)
            
            # Get all positions
            positions = Position.query.all()
            position_map = {p.code: {'id': p.id, 'name': p.name} for p in positions}
            
            print(f"Available positions:")
            for code, info in position_map.items():
                print(f"  Code {code}: {info['name']} (ID: {info['id']})")
            
            users = User.query.all()
            updated_count = 0
            
            for user in users:
                print(f"\nProcessing user: {user.employee_id} ({user.name})")
                print(f"  Current position code: {user.position}")
                print(f"  Current position_id: {user.position_id}")
                print(f"  Current level: {user.level}")
                
                updated = False
                
                # Migrate position code to position_id
                if user.position and user.position in position_map and not user.position_id:
                    user.position_id = position_map[user.position]['id']
                    print(f"  ✓ Set position_id to {user.position_id} ({position_map[user.position]['name']})")
                    updated = True
                
                # Set level based on position code (if not already set)
                if user.position and not user.level:
                    try:
                        # Convert position code to level (1=level 1, 2=level 2, etc.)
                        user.level = int(user.position)
                        print(f"  ✓ Set level to {user.level}")
                        updated = True
                    except (ValueError, TypeError):
                        # Default level for non-numeric positions
                        user.level = 5
                        print(f"  ✓ Set default level to {user.level}")
                        updated = True
                
                if updated:
                    updated_count += 1
                    print(f"  → Updated user {user.employee_id}")
                else:
                    print(f"  - No updates needed for {user.employee_id}")
            
            db.session.commit()
            
            print("="*60)
            print(f"\n[OK] Updated {updated_count} users")
            
            # Print summary
            print("\nUser Summary by Position and Level:")
            print("-"*60)
            
            for user in User.query.order_by(User.level.asc(), User.name.asc()).all():
                pos_name = user.pos.name if user.pos else f"Code: {user.position}"
                print(f"Level {user.level}: {user.name} ({user.employee_id}) - {pos_name}")
            
        except Exception as e:
            print(f"\n[ERROR] Migration failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_users_to_position_id()
