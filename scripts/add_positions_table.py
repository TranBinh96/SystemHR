"""
Script to add positions table and migrate existing position data
"""
from app import app, db
from models import Position, User

def add_positions_table():
    with app.app_context():
        # Create positions table
        db.create_all()
        print("✓ Positions table created")
        
        # Add default positions
        default_positions = [
            {'code': 'NV', 'name': 'Nhân viên'},
            {'code': 'CN', 'name': 'Công nhân'},
            {'code': 'TP', 'name': 'Trưởng phòng'},
            {'code': 'PP', 'name': 'Phó phòng'},
            {'code': 'GS', 'name': 'Giám sát'},
            {'code': 'TN', 'name': 'Trưởng nhóm'},
            {'code': 'QL', 'name': 'Quản lý'},
        ]
        
        for pos_data in default_positions:
            existing = Position.query.filter_by(code=pos_data['code']).first()
            if not existing:
                position = Position(**pos_data)
                db.session.add(position)
        
        db.session.commit()
        print("✓ Default positions added")
        
        # Migrate existing user positions
        users = User.query.all()
        for user in users:
            if user.position and not user.position_id:
                # Try to find matching position
                position = Position.query.filter(
                    db.or_(
                        Position.name.ilike(f'%{user.position}%'),
                        Position.code.ilike(f'%{user.position}%')
                    )
                ).first()
                
                if position:
                    user.position_id = position.id
                    print(f"  Migrated {user.name}: {user.position} -> {position.name}")
        
        db.session.commit()
        print("✓ User positions migrated")
        print("\nDone! Positions table created and data migrated.")

if __name__ == '__main__':
    add_positions_table()
