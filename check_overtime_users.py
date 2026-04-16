from app import app, db
from models import OvertimeRequest, User

with app.app_context():
    # Get all overtime requests
    requests = OvertimeRequest.query.all()
    
    print(f"\n=== Kiểm tra {len(requests)} overtime requests ===\n")
    
    for r in requests:
        print(f"Overtime Request ID: {r.id}")
        print(f"  - Employee: {r.employee_name} ({r.employee_id})")
        print(f"  - Department: {r.department}")
        print(f"  - Date: {r.overtime_date}")
        print(f"  - User ID: {r.user_id}")
        
        # Check if user exists
        if r.user_id:
            user = User.query.get(r.user_id)
            if user:
                print(f"  - ✅ User found: {user.name} ({user.employee_id})")
            else:
                print(f"  - ❌ User NOT found with ID {r.user_id}")
        else:
            print(f"  - ⚠️  No user_id")
        
        # Check manager
        print(f"  - Manager ID: {r.manager_id}")
        if r.manager_id:
            manager = User.query.get(r.manager_id)
            if manager:
                print(f"  - ✅ Manager found: {manager.name} ({manager.employee_id})")
            else:
                print(f"  - ❌ Manager NOT found with ID {r.manager_id}")
        else:
            print(f"  - ⚠️  No manager_id (chưa duyệt)")
        
        print()
