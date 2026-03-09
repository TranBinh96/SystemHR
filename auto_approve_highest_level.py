#!/usr/bin/env python3
"""
Auto-approve pending overtime requests for users with highest level in their department
"""

from app import app, db
from models import User, OvertimeRequest
from sqlalchemy import func

def auto_approve_highest_level_requests():
    with app.app_context():
        # Get all departments
        departments = db.session.query(User.department).distinct().all()
        
        approved_count = 0
        
        for (dept,) in departments:
            if not dept:
                continue
            
            # Find highest level in this department
            highest_level = db.session.query(func.max(User.level)).filter(
                User.department == dept,
                User.work_status != 'resigned'
            ).scalar()
            
            if not highest_level:
                continue
            
            # Get all users with highest level in this department
            highest_level_users = User.query.filter(
                User.department == dept,
                User.level == highest_level,
                User.work_status != 'resigned'
            ).all()
            
            # Auto-approve their pending requests
            for user in highest_level_users:
                pending_requests = OvertimeRequest.query.filter_by(
                    user_id=user.id,
                    status='pending'
                ).all()
                
                for req in pending_requests:
                    req.status = 'approved'
                    req.manager_comment = 'Tự động duyệt (cấp cao nhất trong phòng)'
                    approved_count += 1
                    print(f"✓ Auto-approved request #{req.id} for {user.name} ({user.employee_id})")
        
        db.session.commit()
        print(f"\n✓ Đã tự động duyệt {approved_count} yêu cầu tăng ca")

if __name__ == '__main__':
    auto_approve_highest_level_requests()
