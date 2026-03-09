"""
Update existing overtime records with user data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
import sqlalchemy

def update_data():
    with app.app_context():
        print("Updating existing overtime records...")
        
        try:
            with db.engine.connect() as conn:
                # Update existing records with user data
                print("1. Updating employee info from users table...")
                update_stmt = """
                    UPDATE overtime_requests ot
                    JOIN users u ON ot.user_id = u.id
                    SET 
                        ot.employee_id = u.employee_id,
                        ot.employee_name = u.name,
                        ot.department = u.department,
                        ot.position = u.position
                    WHERE ot.employee_id = '' OR ot.employee_id IS NULL;
                """
                result = conn.execute(sqlalchemy.text(update_stmt))
                conn.commit()
                print(f"   Updated {result.rowcount} records")
                
                # Calculate total_hours for existing records
                print("2. Calculating total_hours...")
                calc_stmt = """
                    UPDATE overtime_requests
                    SET total_hours = TIMESTAMPDIFF(HOUR, 
                        CONCAT(overtime_date, ' ', start_time), 
                        CONCAT(overtime_date, ' ', end_time))
                    WHERE total_hours = 0 OR total_hours IS NULL;
                """
                result = conn.execute(sqlalchemy.text(calc_stmt))
                conn.commit()
                print(f"   Calculated {result.rowcount} records")
                
                # Update manager_id from approved_by
                print("3. Updating manager_id from approved_by...")
                manager_stmt = """
                    UPDATE overtime_requests
                    SET manager_id = approved_by,
                        manager_approved_at = approved_at
                    WHERE approved_by IS NOT NULL AND (manager_id IS NULL OR manager_id = 0);
                """
                result = conn.execute(sqlalchemy.text(manager_stmt))
                conn.commit()
                print(f"   Updated {result.rowcount} records")
            
            print("\n[OK] Data update completed successfully!")
            
        except Exception as e:
            print(f"\n[ERROR] Update failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == '__main__':
    update_data()
