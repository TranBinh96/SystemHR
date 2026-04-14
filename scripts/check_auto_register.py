"""
Script kiểm tra điều kiện auto-register của users
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import User, Menu, MealRegistration
from datetime import datetime, timedelta


def check_auto_register():
    """Kiểm tra users có đủ điều kiện auto-register không"""
    with app.app_context():
        print("\n" + "="*80)
        print("KIỂM TRA ĐIỀU KIỆN AUTO-REGISTER")
        print("="*80)
        
        # Lấy tất cả users
        all_users = User.query.all()
        print(f"\n📊 Tổng số users trong hệ thống: {len(all_users)}\n")
        
        # Kiểm tra từng user
        print(f"{'Mã NV':<12} {'Tên':<25} {'Active':<8} {'Work Status':<15} {'Can Register':<15} {'Kết quả':<20}")
        print("-" * 110)
        
        eligible_count = 0
        
        for user in all_users:
            is_active = "✓" if user.is_active else "✗"
            work_status = user.work_status or "N/A"
            can_register = "✓" if user.can_register else "✗"
            
            # Kiểm tra điều kiện
            is_eligible = (
                user.is_active and 
                user.work_status in ['working', 'business_trip'] and 
                user.can_register
            )
            
            result = "✅ ĐỦ ĐIỀU KIỆN" if is_eligible else "❌ KHÔNG ĐỦ"
            
            if is_eligible:
                eligible_count += 1
            
            print(f"{user.employee_id:<12} {user.name:<25} {is_active:<8} {work_status:<15} {can_register:<15} {result:<20}")
        
        print("-" * 110)
        print(f"\n📈 Kết quả:")
        print(f"   • Tổng users: {len(all_users)}")
        print(f"   • Đủ điều kiện auto-register: {eligible_count}")
        print(f"   • Không đủ điều kiện: {len(all_users) - eligible_count}")
        
        # Kiểm tra menu cho hôm nay và ngày mai
        print(f"\n" + "="*80)
        print("KIỂM TRA MENU")
        print("="*80)
        
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        for check_date in [today, tomorrow]:
            normal_menu = Menu.query.filter(
                Menu.date == check_date,
                Menu.is_special == False,
                Menu.is_active == True,
                Menu.meal_type == 'lunch'
            ).first()
            
            date_str = check_date.strftime('%d/%m/%Y')
            if normal_menu:
                print(f"✅ {date_str}: Có menu bình thường - {normal_menu.dish_name}")
            else:
                print(f"❌ {date_str}: KHÔNG có menu bình thường")
        
        # Kiểm tra đăng ký cho hôm nay
        print(f"\n" + "="*80)
        print(f"KIỂM TRA ĐĂNG KÝ HÔM NAY ({today.strftime('%d/%m/%Y')})")
        print("="*80)
        
        registrations_today = MealRegistration.query.filter_by(date=today).all()
        print(f"\nTổng đăng ký hôm nay: {len(registrations_today)}")
        
        if registrations_today:
            print(f"\n{'Mã NV':<12} {'Tên':<25} {'Món ăn':<30} {'Loại':<15}")
            print("-" * 85)
            for reg in registrations_today:
                meal_name = reg.menu.dish_name if reg.menu else "N/A"
                meal_type = "Cải thiện" if (reg.menu and reg.menu.is_special) else "Bình thường"
                print(f"{reg.user.employee_id:<12} {reg.user.name:<25} {meal_name:<30} {meal_type:<15}")
        
        print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    check_auto_register()
