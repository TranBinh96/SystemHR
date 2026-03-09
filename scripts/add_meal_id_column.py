"""
Add meal_id column to meal_registrations table
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

def add_meal_id_column():
    with app.app_context():
        try:
            # Check if column exists first
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('meal_registrations')]
            
            if 'meal_id' in columns:
                print("✓ meal_id column already exists")
                return
            
            # Add meal_id column
            with db.engine.connect() as conn:
                conn.execute(db.text('''
                    ALTER TABLE meal_registrations 
                    ADD COLUMN meal_id INTEGER REFERENCES menus(id)
                '''))
                conn.commit()
            print("✓ Added meal_id column to meal_registrations table")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    add_meal_id_column()
