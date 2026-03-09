#!/usr/bin/env python3
"""
Fix position levels in positions table
Level: 1=highest (Giám đốc), 5=lowest (Công nhân)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, Position

def fix_position_levels():
    """Fix position levels based on code"""
    with app.app_context():
        try:
            print("Fixing position levels...")
            print("="*60)
            
            # Define correct levels for each position code
            level_mapping = {
                '0': 1,  # Giám đốc (if exists)
                '1': 2,  # Trưởng Phòng
                '2': 3,  # Phó Phòng
                '3': 4,  # Nhân Viên
                '4': 5,  # Công Nhân
                '5': 3,  # Giám sát
                '6': 3,  # Trưởng nhóm
                '7': 3,  # Quản lý
            }
            
            # Get all positions
            positions = Position.query.all()
            
            print(f"\nFound {len(positions)} positions")
            print("\nBEFORE:")
            print(f"{'Code':<6} {'Name':<20} {'Level (Old)':<12}")
            print("-" * 40)
            for pos in positions:
                print(f"{pos.code:<6} {pos.name:<20} {pos.level:<12}")
            
            # Update levels
            updated_count = 0
            for pos in positions:
                if pos.code in level_mapping:
                    old_level = pos.level
                    new_level = level_mapping[pos.code]
                    if old_level != new_level:
                        pos.level = new_level
                        updated_count += 1
                        print(f"\n✓ Updated {pos.name} (code={pos.code}): level {old_level} → {new_level}")
            
            # Commit changes
            db.session.commit()
            
            print("\n" + "="*60)
            print(f"Updated {updated_count} positions")
            print("="*60)
            
            # Show final state
            positions = Position.query.order_by(Position.level.asc(), Position.code.asc()).all()
            print("\nAFTER (sorted by level):")
            print(f"{'Code':<6} {'Name':<20} {'Level (New)':<12}")
            print("-" * 40)
            for pos in positions:
                print(f"{pos.code:<6} {pos.name:<20} {pos.level:<12}")
            
            print("\n✅ Position levels fixed successfully!")
            print("\nLevel hierarchy:")
            print("  1 = Giám đốc (highest)")
            print("  2 = Trưởng Phòng")
            print("  3 = Phó Phòng, Giám sát, Trưởng nhóm, Quản lý")
            print("  4 = Nhân Viên")
            print("  5 = Công Nhân (lowest)")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    fix_position_levels()
