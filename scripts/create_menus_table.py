"""
Script to create menus table for meal management
Run this script to add the menus table to your database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Menu
from datetime import datetime, timedelta

def create_menus_table():
    with app.app_context():
        # Create table
        db.create_all()
        print("✅ Menus table created successfully!")
        
        # Add sample data
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        
        sample_menus = [
            {
                'date': start_of_week,
                'meal_type': 'lunch',
                'dish_name': 'Cơm gà xối mỡ',
                'description': 'Cơm trắng, gà luộc, nước mắm gừng',
                'is_special': False,
                'is_vegetarian': False
            },
            {
                'date': start_of_week,
                'meal_type': 'lunch',
                'dish_name': 'Cơm chay đậu hũ',
                'description': 'Cơm trắng, đậu hũ chiên, rau xào',
                'is_special': True,
                'is_vegetarian': True
            },
            {
                'date': start_of_week + timedelta(days=1),
                'meal_type': 'lunch',
                'dish_name': 'Cơm sườn nướng',
                'description': 'Cơm trắng, sườn nướng, rau sống',
                'is_special': False,
                'is_vegetarian': False
            },
            {
                'date': start_of_week + timedelta(days=2),
                'meal_type': 'lunch',
                'dish_name': 'Cơm cá kho tộ',
                'description': 'Cơm trắng, cá kho, canh chua',
                'is_special': False,
                'is_vegetarian': False
            },
        ]
        
        for menu_data in sample_menus:
            # Check if menu already exists
            existing = Menu.query.filter_by(
                date=menu_data['date'],
                meal_type=menu_data['meal_type'],
                dish_name=menu_data['dish_name']
            ).first()
            
            if not existing:
                menu = Menu(**menu_data)
                db.session.add(menu)
        
        db.session.commit()
        print("✅ Sample menus added!")
        
        # Show all menus
        all_menus = Menu.query.all()
        print(f"\n📋 Total menus in database: {len(all_menus)}")
        for menu in all_menus:
            print(f"  - {menu.date} ({menu.meal_type}): {menu.dish_name}")

if __name__ == '__main__':
    create_menus_table()
    print("\n✅ Done! You can now access /admin/meals")
