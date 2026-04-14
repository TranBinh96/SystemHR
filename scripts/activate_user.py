"""
Script kích hoạt user
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User


def activate_user(employee_id):
    """Kích hoạt user"""
    with app.app_context():
        user = User.query.filter_by(employee_id=employee_id).first()
        
        if not user:
            print(f"❌ Không tìm thấy user với mã: {employee_id}")
            return
        
        print(f"\n📋 User: {user.name} ({user.employee_id})")
        print(f"   Trạng thái hiện tại:")
        print(f"   • is_active: {user.is_active}")
        print(f"   • work_status: {user.work_status}")
        print(f"   • can_register: {user.can_register}")
        
        # Kích hoạt
        user.is_active = True
        user.work_status = 'working'
        user.can_register = True
        
        db.session.commit()
        
        print(f"\n✅ Đã kích hoạt user {user.name}!")
        print(f"   Trạng thái mới:")
        print(f"   • is_active: {user.is_active}")
        print(f"   • work_status: {user.work_status}")
        print(f"   • can_register: {user.can_register}\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python activate_user.py <employee_id>")
        print("Example: python activate_user.py 10197")
        sys.exit(1)
    
    activate_user(sys.argv[1])
