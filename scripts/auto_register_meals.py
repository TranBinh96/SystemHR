"""
Script tự động đăng ký suất ăn bình thường cho user chưa đăng ký
Chạy script này mỗi ngày để đảm bảo tất cả user có suất ăn
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Menu, MealRegistration
from datetime import datetime, timedelta


def auto_register_meals_for_date(target_date):
    """
    Tự động đăng ký suất ăn bình thường cho user chưa đăng ký
    
    Args:
        target_date: Ngày cần đăng ký (date object)
    """
    with app.app_context():
        print(f"\n=== Tự động đăng ký suất ăn cho ngày {target_date.strftime('%d/%m/%Y')} ===\n")
        
        # Lấy tất cả user đang hoạt động (active và đang làm việc)
        active_users = User.query.filter(
            User.is_active == True,
            User.work_status == 'working'
        ).all()
        
        print(f"Tìm thấy {len(active_users)} user đang hoạt động")
        
        # Lấy menu bình thường (không phải cải thiện) cho ngày này
        normal_menu = Menu.query.filter(
            Menu.date == target_date,
            Menu.is_special == False,
            Menu.is_active == True,
            Menu.meal_type == 'lunch'
        ).first()
        
        if not normal_menu:
            print(f"⚠️  Không tìm thấy menu bình thường cho ngày {target_date.strftime('%d/%m/%Y')}")
            print("Vui lòng tạo menu trước khi chạy script này")
            return
        
        print(f"Menu bình thường: {normal_menu.dish_name}")
        
        # Đếm số user đã đăng ký và chưa đăng ký
        registered_count = 0
        auto_registered_count = 0
        
        for user in active_users:
            # Kiểm tra xem user đã đăng ký chưa
            existing_registration = MealRegistration.query.filter_by(
                user_id=user.id,
                date=target_date
            ).first()
            
            if existing_registration:
                registered_count += 1
                print(f"✓ {user.employee_id} - {user.name}: Đã đăng ký")
            else:
                # Tự động đăng ký suất ăn bình thường
                new_registration = MealRegistration(
                    user_id=user.id,
                    date=target_date,
                    meal_id=normal_menu.id,
                    meal_type='lunch',
                    has_meal=True,
                    notes='Tự động đăng ký bởi hệ thống'
                )
                db.session.add(new_registration)
                auto_registered_count += 1
                print(f"+ {user.employee_id} - {user.name}: Tự động đăng ký suất ăn bình thường")
        
        # Commit tất cả thay đổi
        db.session.commit()
        
        print(f"\n=== Kết quả ===")
        print(f"Tổng số user: {len(active_users)}")
        print(f"Đã đăng ký trước: {registered_count}")
        print(f"Tự động đăng ký: {auto_registered_count}")
        print(f"✓ Hoàn thành!\n")


def auto_register_meals_for_tomorrow():
    """Tự động đăng ký suất ăn cho ngày mai"""
    tomorrow = datetime.now().date() + timedelta(days=1)
    auto_register_meals_for_date(tomorrow)


def auto_register_meals_for_week():
    """Tự động đăng ký suất ăn cho cả tuần tới"""
    today = datetime.now().date()
    
    for i in range(1, 8):  # 7 ngày tới
        target_date = today + timedelta(days=i)
        auto_register_meals_for_date(target_date)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Tự động đăng ký suất ăn cho user chưa đăng ký')
    parser.add_argument('--mode', choices=['tomorrow', 'week', 'date'], default='tomorrow',
                       help='Chế độ: tomorrow (ngày mai), week (cả tuần), date (ngày cụ thể)')
    parser.add_argument('--date', help='Ngày cụ thể (format: YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    if args.mode == 'tomorrow':
        auto_register_meals_for_tomorrow()
    elif args.mode == 'week':
        auto_register_meals_for_week()
    elif args.mode == 'date':
        if not args.date:
            print("Vui lòng cung cấp --date khi dùng mode 'date'")
            sys.exit(1)
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
            auto_register_meals_for_date(target_date)
        except ValueError:
            print("Format ngày không đúng. Vui lòng dùng YYYY-MM-DD")
            sys.exit(1)
