#!/usr/bin/env python3
"""
Script tạo dữ liệu test cho meal registrations
"""

import sys
import os
sys.path.append('.')

from app import app
from models import db, User, Menu, MealRegistration, Department
from datetime import date, timedelta
from utils.timezone_utils import today

def create_test_data():
    """Tạo dữ liệu test"""
    
    with app.app_context():
        try:
            print("🔧 CREATING TEST DATA")
            print("=" * 40)
            
            # 1. Kiểm tra users
            users = User.query.filter(
                User.work_status == 'working',
                User.employee_id.like('10%')
            ).limit(5).all()
            
            print(f"📊 Found {len(users)} working users with 10xx IDs")
            
            if len(users) == 0:
                print("❌ No users found! Creating test users...")
                
                # Tạo department nếu chưa có
                dept = Department.query.filter_by(name='Production').first()
                if not dept:
                    dept = Department(name='Production', description='Production Department')
                    db.session.add(dept)
                    db.session.commit()
                
                # Tạo test users
                for i in range(1, 6):
                    user = User(
                        employee_id=f'100{i}',
                        name=f'Test User {i}',
                        email=f'test{i}@okivietnam.com',
                        department_id=dept.id,
                        work_status='working',
                        is_active=True,
                        can_register=True
                    )
                    user.set_password('password123')
                    db.session.add(user)
                
                db.session.commit()
                users = User.query.filter(User.employee_id.like('100%')).all()
                print(f"✅ Created {len(users)} test users")
            
            # 2. Kiểm tra menus
            today_date = today()
            
            # Tạo menus cho 7 ngày tới
            for day_offset in range(0, 7):
                target_date = today_date + timedelta(days=day_offset)
                
                # Kiểm tra menu đã có chưa
                existing_menu = Menu.query.filter_by(date=target_date, meal_type='lunch').first()
                
                if not existing_menu:
                    # Tạo menu bình thường
                    normal_menu = Menu(
                        date=target_date,
                        meal_type='lunch',
                        dish_name=f'Cơm gà xối mỡ - {target_date.strftime("%d/%m")}',
                        description='Gà chiên giòn, cơm trắng, canh chua',
                        is_special=False,
                        is_active=True
                    )
                    db.session.add(normal_menu)
                    
                    # Tạo menu cải thiện
                    special_menu = Menu(
                        date=target_date,
                        meal_type='lunch',
                        dish_name=f'Bún bò Huế - {target_date.strftime("%d/%m")}',
                        description='Bún bò đặc biệt, chả cua, giò heo',
                        is_special=True,
                        is_active=True
                    )
                    db.session.add(special_menu)
            
            db.session.commit()
            
            menus = Menu.query.filter(
                Menu.date >= today_date,
                Menu.date <= today_date + timedelta(days=6)
            ).all()
            print(f"📋 Found/Created {len(menus)} menus for next 7 days")
            
            # 3. Tạo meal registrations
            registrations_created = 0
            
            for day_offset in range(0, 7):
                target_date = today_date + timedelta(days=day_offset)
                
                # Lấy menu cho ngày này
                normal_menu = Menu.query.filter_by(
                    date=target_date, 
                    meal_type='lunch', 
                    is_special=False
                ).first()
                
                special_menu = Menu.query.filter_by(
                    date=target_date, 
                    meal_type='lunch', 
                    is_special=True
                ).first()
                
                if not normal_menu:
                    continue
                
                # Đăng ký cho từng user
                for i, user in enumerate(users):
                    # Kiểm tra đã đăng ký chưa
                    existing = MealRegistration.query.filter_by(
                        user_id=user.id,
                        date=target_date
                    ).first()
                    
                    if existing:
                        continue
                    
                    # 80% đăng ký bình thường, 20% cải thiện
                    menu_to_use = special_menu if (i % 5 == 0 and special_menu) else normal_menu
                    
                    registration = MealRegistration(
                        user_id=user.id,
                        date=target_date,
                        meal_id=menu_to_use.id,
                        meal_type='lunch',
                        has_meal=True,
                        notes='Test data'
                    )
                    
                    db.session.add(registration)
                    registrations_created += 1
            
            db.session.commit()
            print(f"🍽️  Created {registrations_created} meal registrations")
            
            # 4. Kiểm tra kết quả
            total_registrations = MealRegistration.query.filter(
                MealRegistration.date >= today_date,
                MealRegistration.date <= today_date + timedelta(days=6)
            ).count()
            
            print(f"\n✅ SUMMARY:")
            print(f"   Users: {len(users)}")
            print(f"   Menus: {len(menus)}")
            print(f"   Registrations: {total_registrations}")
            print(f"\n🎯 Test data created successfully!")
            print(f"📅 Date range: {today_date.strftime('%d/%m/%Y')} - {(today_date + timedelta(days=6)).strftime('%d/%m/%Y')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_test_data()