"""
Reset database: drop all tables, recreate, seed default data
Usage: python scripts/reset_db.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Department, Position, OvertimeRequest, LeaveRequest, MealRegistration, Menu, ApprovalHierarchy, ExitEntryRequest
from werkzeug.security import generate_password_hash


def reset_database():
    with app.app_context():
        print("=" * 50)
        print("RESET DATABASE")
        print("=" * 50)

        # Drop all tables
        print("\n[1/3] Dropping all tables...")
        db.drop_all()
        print("✓ All tables dropped")

        # Recreate all tables
        print("\n[2/3] Recreating tables...")
        db.create_all()
        print("✓ Tables created:")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        for table in sorted(inspector.get_table_names()):
            print(f"    - {table}")

        # Seed default data
        print("\n[3/3] Seeding default data...")

        # Default departments
        departments = [
            Department(code='IT',   name='Phòng IT',          description='Công nghệ thông tin'),
            Department(code='HR',   name='Phòng Nhân sự',     description='Quản lý nhân sự'),
            Department(code='PRD',  name='Phòng Sản xuất',    description='Sản xuất'),
            Department(code='QC',   name='Phòng QC',          description='Kiểm soát chất lượng'),
            Department(code='ACC',  name='Phòng Kế toán',     description='Kế toán tài chính'),
        ]
        db.session.add_all(departments)
        db.session.flush()
        print(f"✓ {len(departments)} departments created")

        # Default positions
        positions = [
            Position(code='1', name='Nhân viên'),
            Position(code='2', name='Công nhân'),
            Position(code='3', name='Trưởng phòng'),
            Position(code='4', name='Phó phòng'),
            Position(code='5', name='Giám sát'),
            Position(code='6', name='Trưởng nhóm'),
            Position(code='7', name='Quản lý'),
        ]
        db.session.add_all(positions)
        db.session.flush()
        print(f"✓ {len(positions)} positions created")

        # Get references
        it_dept = next(d for d in departments if d.code == 'IT')
        hr_dept = next(d for d in departments if d.code == 'HR')
        pos_manager  = next(p for p in positions if p.code == '7')  # Quản lý
        pos_truong   = next(p for p in positions if p.code == '3')  # Trưởng phòng
        pos_nhanvien = next(p for p in positions if p.code == '1')  # Nhân viên

        # Default users
        admin = User(
            employee_id='ADMIN',
            name='Administrator',
            password=generate_password_hash('admin123'),
            department_id=it_dept.id,
            position_id=pos_manager.id,
            role='admin',
            can_approve=True,
            can_register=True,
            work_status='working',
        )
        emp001 = User(
            employee_id='EMP001',
            name='Nguyen Van A',
            password=generate_password_hash('password123'),
            department_id=hr_dept.id,
            position_id=pos_nhanvien.id,
            role='user',
            can_approve=False,
            can_register=True,
            work_status='working',
        )
        db.session.add_all([admin, emp001])
        db.session.flush()
        print("✓ 2 default users created (ADMIN / admin123, EMP001 / password123)")

        # Default approval hierarchy: Trưởng phòng approves Nhân viên (IT dept)
        rule = ApprovalHierarchy(
            department_id=it_dept.id,
            approver_position_id=pos_truong.id,
            approvee_position_id=pos_nhanvien.id,
            can_approve=True,
        )
        db.session.add(rule)

        db.session.commit()
        print("✓ Default approval hierarchy created")

        print("\n" + "=" * 50)
        print("✓ Database reset completed!")
        print("=" * 50)
        print("\nDefault credentials:")
        print("  Admin : ADMIN    / admin123")
        print("  User  : EMP001   / password123")


if __name__ == '__main__':
    confirm = input("\n⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
    if confirm.strip().lower() == 'yes':
        reset_database()
    else:
        print("Cancelled.")
        sys.exit(0)
