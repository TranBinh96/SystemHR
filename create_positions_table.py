"""
Quick script to create positions table and add default data
Run this once: python create_positions_table.py
"""
from app import app, db
from models import Position

with app.app_context():
    # Create positions table
    db.create_all()
    print("✓ Tables created")
    
    # Check if positions already exist
    if Position.query.count() == 0:
        print("Adding default positions...")
        default_positions = [
            {'code': '1', 'name': 'Nhân viên'},
            {'code': '2', 'name': 'Công nhân'},
            {'code': '3', 'name': 'Trưởng phòng'},
            {'code': '4', 'name': 'Phó phòng'},
            {'code': '5', 'name': 'Giám sát'},
            {'code': '6', 'name': 'Trưởng nhóm'},
            {'code': '7', 'name': 'Quản lý'},
        ]
        
        for pos_data in default_positions:
            position = Position(**pos_data)
            db.session.add(position)
        
        db.session.commit()
        print("✓ Added 7 default positions")
        print("\nPositions created:")
        for pos in Position.query.all():
            print(f"  - {pos.code}: {pos.name}")
    else:
        print(f"✓ Positions table already has {Position.query.count()} records")
        print("\nExisting positions:")
        for pos in Position.query.all():
            print(f"  - {pos.code}: {pos.name}")

print("\n✅ Done! You can now access /admin/positions")
