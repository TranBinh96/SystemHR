#!/usr/bin/env python3
"""
Script to automatically assign overtime approver for users without one
Logic: Assign the manager (can_approve=True) in the same department
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Department

def auto_assign_approvers():
    """Auto assign overtime approver for users without one"""
    with app.app_context():
        try:
            print("\n" + "="*80)
            print("TỰ ĐỘNG CHỈ ĐỊNH NGƯỜI PHÊ DUYỆT OVERTIME")
            print("="*80)
            
            # Get all departments
            departments = Department.query.all()
            
            total_assigned = 0
            
            for dept in departments:
                print(f"\n📁 {dept.name}")
                print(f"   {'─'*70}")
                
                # Find managers in this department
                managers = User.query.filter_by(
                    department_id=dept.id,
                    can_approve=True,
                    is_active=True
                ).all()
                
                if not managers:
                    print(f"   ⚠️  Không có manager trong phòng này")
                    continue
                
                # Use first manager as default approver
                default_approver = managers[0]
                print(f"   👔 Manager: {default_approver.name} ({default_approver.employee_id})")
                
                # Find users without approver
                users_without_approver = User.query.filter_by(
                    department_id=dept.id,
                    overtime_approver_id=None,
                    is_active=True
                ).filter(User.can_approve == False).all()
                
                if not users_without_approver:
                    print(f"   ✓ Tất cả user đã có người phê duyệt")
                    continue
                
                print(f"   📝 Chỉ định cho {len(users_without_approver)} user:")
                
                for user in users_without_approver:
                    user.overtime_approver_id = default_approver.id
                    print(f"      ✓ {user.name} ({user.employee_id}) → {default_approver.name}")
                    total_assigned += 1
            
            if total_assigned > 0:
                db.session.commit()
                print(f"\n{'='*80}")
                print(f"✅ ĐÃ CHỈ ĐỊNH THÀNH CÔNG CHO {total_assigned} USER")
                print(f"{'='*80}")
            else:
                print(f"\n{'='*80}")
                print(f"✓ TẤT CẢ USER ĐÃ CÓ NGƯỜI PHÊ DUYỆT")
                print(f"{'='*80}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ LỖI: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = auto_assign_approvers()
    sys.exit(0 if success else 1)
