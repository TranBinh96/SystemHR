"""
Auto-migrate overtime_requests table to new schema
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
import sqlalchemy

def auto_migrate():
    with app.app_context():
        print("Starting auto-migration...")
        
        # SQL statements to add missing columns
        alter_statements = [
            "ALTER TABLE overtime_requests ADD COLUMN employee_id VARCHAR(50) NOT NULL DEFAULT '';",
            "ALTER TABLE overtime_requests ADD COLUMN employee_name VARCHAR(100) NOT NULL DEFAULT '';",
            "ALTER TABLE overtime_requests ADD COLUMN department VARCHAR(100) NOT NULL DEFAULT '';",
            "ALTER TABLE overtime_requests ADD COLUMN position VARCHAR(50);",
            "ALTER TABLE overtime_requests CHANGE COLUMN date overtime_date DATE NOT NULL;",
            "ALTER TABLE overtime_requests ADD COLUMN total_hours DECIMAL(4,2) NOT NULL DEFAULT 0;",
            "ALTER TABLE overtime_requests ADD COLUMN manager_id INT NULL;",
            "ALTER TABLE overtime_requests ADD COLUMN manager_approved_at TIMESTAMP NULL;",
            "ALTER TABLE overtime_requests ADD COLUMN manager_comment TEXT NULL;",
        ]
        
        try:
            with db.engine.connect() as conn:
                for stmt in alter_statements:
                    print(f"Executing: {stmt}")
                    conn.execute(sqlalchemy.text(stmt))
                    conn.commit()
                
                # Update existing records with user data
                print("\nUpdating existing records with user data...")
                update_stmt = """
                    UPDATE overtime_requests ot
                    JOIN users u ON ot.user_id = u.id
                    SET 
                        ot.employee_id = u.employee_id,
                        ot.employee_name = u.name,
                        ot.department = u.department,
                        ot.position = u.position
                    WHERE ot.employee_id = '';
                """
                conn.execute(sqlalchemy.text(update_stmt))
                conn.commit()
                
                # Calculate total_hours for existing records
                print("Calculating total_hours for existing records...")
                calc_stmt = """
                    UPDATE overtime_requests
                    SET total_hours = TIMESTAMPDIFF(HOUR, 
                        CONCAT(overtime_date, ' ', start_time), 
                        CONCAT(overtime_date, ' ', end_time))
                    WHERE total_hours = 0;
                """
                conn.execute(sqlalchemy.text(calc_stmt))
                conn.commit()
                
                # Update manager_id from approved_by
                print("Updating manager_id from approved_by...")
                manager_stmt = """
                    UPDATE overtime_requests
                    SET manager_id = approved_by,
                        manager_approved_at = approved_at
                    WHERE approved_by IS NOT NULL AND manager_id IS NULL;
                """
                conn.execute(sqlalchemy.text(manager_stmt))
                conn.commit()
            
            print("\n[OK] Migration completed successfully!")
            print("\nTable structure is now up to date.")
            
        except Exception as e:
            print(f"\n[ERROR] Migration failed: {e}")
            print("\nPlease check the error and try again.")
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == '__main__':
    auto_migrate()
