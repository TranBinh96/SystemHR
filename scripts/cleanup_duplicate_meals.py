#!/usr/bin/env python3
"""
Script để dọn dẹp các đăng ký suất ăn duplicate
Giữ lại đăng ký đầu tiên (ID nhỏ nhất) cho mỗi user/ngày
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, MealRegistration, User
from sqlalchemy import func
from datetime import datetime

def cleanup_duplicate_meals():
    """Dọn dẹp các đăng ký suất ăn duplicate"""
    
    with app.app_context():
        try:
            print("\n=== DỌN DẸP ĐĂNG KÝ SUẤT ĂN DUPLICATE ===")
            
            # Tìm các duplicate: cùng user_id và date nhưng có nhiều hơn 1 record
            duplicates_query = db.session.query(
                MealRegistration.user_id,
                MealRegistration.date,
                func.count(MealRegistration.id).label('count'),
                func.min(MealRegistration.id).label('keep_id')
            ).group_by(
                MealRegistration.user_id,
                MealRegistration.date
            ).having(func.count(MealRegistration.id) > 1)
            
            duplicates = duplicates_query.all()
            
            if not duplicates:
                print("✓ Không tìm thấy đăng ký duplicate nào!")
                return
            
            print(f"Tìm thấy {len(duplicates)} nhóm duplicate:")
            
            total_deleted = 0
            
            for dup in duplicates:
                user_id, date, count, keep_id = dup
                
                # Lấy thông tin user
                user = User.query.get(user_id)
                user_name = user.name if user else f"User ID {user_id}"
                
                print(f"\n📅 {date.strftime('%d/%m/%Y')} - {user_name} ({user_id}): {count} đăng ký")
                
                # Lấy tất cả records của user này trong ngày này
                all_records = MealRegistration.query.filter_by(
                    user_id=user_id,
                    date=date
                ).order_by(MealRegistration.id).all()
                
                # Hiển thị chi tiết
                for i, record in enumerate(all_records):
                    status = "🔒 GIỮ LẠI" if record.id == keep_id else "❌ XÓA"
                    meal_name = record.menu.dish_name if record.menu else "N/A"
                    meal_type = "Cải thiện" if (record.menu and record.menu.is_special) else "Bình thường"
                    print(f"  {i+1}. ID {record.id} - {meal_name} ({meal_type}) - {status}")
                
                # Xóa các records không phải keep_id
                deleted_records = MealRegistration.query.filter(
                    MealRegistration.user_id == user_id,
                    MealRegistration.date == date,
                    MealRegistration.id != keep_id
                ).all()
                
                for record in deleted_records:
                    db.session.delete(record)
                    total_deleted += 1
            
            # Xác nhận trước khi commit
            print(f"\n⚠️  CHUẨN BỊ XÓA {total_deleted} ĐĂNG KÝ DUPLICATE")
            confirm = input("Bạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
            
            if confirm == 'y':
                db.session.commit()
                print(f"✅ Đã xóa {total_deleted} đăng ký duplicate!")
                print("✅ Dọn dẹp hoàn tất!")
            else:
                db.session.rollback()
                print("❌ Đã hủy thao tác!")
                
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
            db.session.rollback()

def show_duplicate_stats():
    """Hiển thị thống kê duplicate"""
    
    with app.app_context():
        try:
            print("\n=== THỐNG KÊ ĐĂNG KÝ DUPLICATE ===")
            
            # Đếm tổng số đăng ký
            total_registrations = MealRegistration.query.count()
            print(f"Tổng số đăng ký: {total_registrations}")
            
            # Đếm số user/date unique
            unique_combinations = db.session.query(
                MealRegistration.user_id,
                MealRegistration.date
            ).distinct().count()
            print(f"Số tổ hợp user/ngày unique: {unique_combinations}")
            
            # Đếm duplicate
            duplicates = total_registrations - unique_combinations
            print(f"Số đăng ký duplicate: {duplicates}")
            
            if duplicates > 0:
                print(f"📊 Tỷ lệ duplicate: {duplicates/total_registrations*100:.1f}%")
                
                # Top users có nhiều duplicate nhất
                top_duplicates = db.session.query(
                    MealRegistration.user_id,
                    func.count(MealRegistration.id).label('total_count'),
                    func.count(func.distinct(MealRegistration.date)).label('unique_dates')
                ).group_by(
                    MealRegistration.user_id
                ).having(
                    func.count(MealRegistration.id) > func.count(func.distinct(MealRegistration.date))
                ).order_by(
                    (func.count(MealRegistration.id) - func.count(func.distinct(MealRegistration.date))).desc()
                ).limit(10).all()
                
                if top_duplicates:
                    print("\n🔝 Top 10 users có nhiều duplicate nhất:")
                    for user_id, total_count, unique_dates in top_duplicates:
                        user = User.query.get(user_id)
                        user_name = user.name if user else f"User ID {user_id}"
                        duplicate_count = total_count - unique_dates
                        print(f"  {user_name} ({user_id}): {duplicate_count} duplicate ({total_count} total, {unique_dates} unique)")
            else:
                print("✅ Không có duplicate!")
                
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Dọn dẹp đăng ký suất ăn duplicate')
    parser.add_argument('--stats', action='store_true', help='Chỉ hiển thị thống kê')
    parser.add_argument('--cleanup', action='store_true', help='Dọn dẹp duplicate')
    
    args = parser.parse_args()
    
    if args.stats:
        show_duplicate_stats()
    elif args.cleanup:
        show_duplicate_stats()
        cleanup_duplicate_meals()
    else:
        print("Sử dụng:")
        print("  python cleanup_duplicate_meals.py --stats     # Xem thống kê")
        print("  python cleanup_duplicate_meals.py --cleanup   # Dọn dẹp duplicate")