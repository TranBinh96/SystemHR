"""
Script to migrate overtime_requests table to new schema
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
import sqlalchemy

def check_and_migrate():
    with app.app_context():
        inspector = sqlalchemy.inspect(db.engine)
        
        # Check if table exists
        if 'overtime_requests' not in inspector.get_table_names():
            print("[ERROR] Table overtime_requests does not exist!")
            print("Run: python scripts/create_overtime_tables.py")
            return
        
        # Get current columns
        columns = inspector.get_columns('overtime_requests')
        column_names = [col['name'] for col in columns]
        
        print("Current columns in overtime_requests:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")
        
        # Check if new columns exist
        required_columns = [
            'employee_id', 'employee_name', 'department', 'position',
            'overtime_date', 'total_hours', 'manager_id', 
            'manager_approved_at', 'manager_comment'
        ]
        
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"\n[ERROR] Missing columns: {', '.join(missing_columns)}")
            print("\n[WARNING] The table structure is outdated!")
            print("\nOptions:")
            print("1. Drop and recreate table (WILL DELETE ALL DATA):")
            print("   DROP TABLE overtime_requests;")
            print("   Then run: python scripts/create_overtime_tables.py")
            print("\n2. Add missing columns manually (recommended if you have data):")
            
            # Generate ALTER TABLE statements
            alter_statements = []
            if 'employee_id' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN employee_id VARCHAR(50) NOT NULL DEFAULT '';")
            if 'employee_name' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN employee_name VARCHAR(100) NOT NULL DEFAULT '';")
            if 'department' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN department VARCHAR(100) NOT NULL DEFAULT '';")
            if 'position' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN position VARCHAR(50);")
            if 'overtime_date' not in column_names and 'date' in column_names:
                alter_statements.append("ALTER TABLE overtime_requests CHANGE COLUMN date overtime_date DATE NOT NULL;")
            elif 'overtime_date' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN overtime_date DATE NOT NULL;")
            if 'total_hours' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN total_hours DECIMAL(4,2) NOT NULL DEFAULT 0;")
            if 'manager_id' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN manager_id INT NULL;")
            if 'manager_approved_at' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN manager_approved_at TIMESTAMP NULL;")
            if 'manager_comment' not in column_names:
                alter_statements.append("ALTER TABLE overtime_requests ADD COLUMN manager_comment TEXT NULL;")
            
            print("\n   Run these SQL commands:")
            for stmt in alter_statements:
                print(f"   {stmt}")
            
            # Option to auto-migrate
            print("\n3. Auto-migrate (will attempt to add columns):")
            response = input("   Do you want to auto-migrate? (yes/no): ")
            
            if response.lower() == 'yes':
                try:
                    for stmt in alter_statements:
                        print(f"Executing: {stmt}")
                        db.engine.execute(sqlalchemy.text(stmt))
                    print("\n✓ Migration completed successfully!")
                except Exception as e:
                    print(f"\n❌ Migration failed: {e}")
                    print("Please run the SQL commands manually.")
        else:
            print("\n[OK] All required columns exist!")
            print("Table structure is up to date.")

if __name__ == '__main__':
    check_and_migrate()
