from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', foreign_keys='User.department_id', backref='dept', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.code} - {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    # Work status
    work_status = db.Column(db.String(20), default='working')
    
    # Personal info
    avatar_url = db.Column(db.String(255))
    
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    
    # Permission fields
    can_approve = db.Column(db.Boolean, default=False)  # Quyền phê duyệt overtime
    can_register = db.Column(db.Boolean, default=True)  # Quyền đăng ký overtime
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    overtime_requests = db.relationship('OvertimeRequest', 
                                       foreign_keys='OvertimeRequest.user_id',
                                       backref='user', 
                                       lazy=True)
    meal_registrations = db.relationship('MealRegistration', 
                                        foreign_keys='MealRegistration.user_id',
                                        backref='user', 
                                        lazy=True)
    confirmed_meals = db.relationship('MealRegistration',
                                     foreign_keys='MealRegistration.confirmed_by',
                                     backref='confirmer',
                                     lazy=True)
    
    def __repr__(self):
        return f'<User {self.employee_id} - {self.name}>'
    
    def get_id(self):
        return str(self.id)
    
    def update_last_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
        db.session.commit()
    
    def set_password(self, password):
        """Set password hash"""
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)
    
    def get_approvers(self):
        """
        Get list of users who can approve this user's overtime requests.
        Returns users in the same department with can_approve = True.
        """
        if not self.department_id:
            return []
        
        # Find users in same department with approval permission
        approvers = User.query.filter(
            User.department_id == self.department_id,
            User.can_approve == True,
            User.is_active == True,
            User.id != self.id
        ).all()
        
        return approvers
    
    def can_approve_for(self, user):
        """
        Check if this user can approve overtime for another user.
        Returns True if this user has can_approve = True in same department.
        """
        if not self.department_id or not user.department_id:
            return False
        
        # Must be same department and have approval permission
        return (self.department_id == user.department_id and 
                self.can_approve and 
                self.is_active)
    
    def get_subordinates(self):
        """
        Get list of users this user can approve for.
        Returns users in the same department if this user has can_approve = True.
        """
        if not self.department_id or not self.can_approve:
            return []
        
        # Find users in same department (excluding self)
        subordinates = User.query.filter(
            User.department_id == self.department_id,
            User.is_active == True,
            User.id != self.id
        ).all()
        
        return subordinates
    
    def is_manager(self):
        """Check if user is a manager (has approval permission)"""
        return self.can_approve


class OvertimeRequest(db.Model):
    __tablename__ = 'overtime_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    # Overtime info
    overtime_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    total_hours = db.Column(db.Numeric(4, 2), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    
    # Approval status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    # Manager approval
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    manager_approved_at = db.Column(db.DateTime)
    manager_comment = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Backward compatibility aliases (not in database)
    @property
    def date(self):
        return self.overtime_date
    
    @property
    def approved_by(self):
        return self.manager_id
    
    @property
    def approved_at(self):
        return self.manager_approved_at
    
    def __repr__(self):
        return f'<OvertimeRequest {self.id} - {self.status}>'


class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    # Leave info
    leave_type = db.Column(db.String(50), nullable=False)  # annual, sick, personal, maternity, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    
    # Emergency contact (for sick leave)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    
    # Approval status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    # Manager approval
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    manager_approved_at = db.Column(db.DateTime)
    manager_comment = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='leave_requests')
    manager = db.relationship('User', foreign_keys=[manager_id])
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} - {self.leave_type} - {self.status}>'


class MealRegistration(db.Model):
    __tablename__ = 'meal_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('menus.id'))  # Reference to Menu
    meal_type = db.Column(db.String(20))  # breakfast, lunch, dinner
    has_meal = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    is_confirmed = db.Column(db.Boolean, default=False)  # Xác nhận hoàn thành (cho cơm cải thiện)
    confirmed_at = db.Column(db.DateTime)  # Thời gian xác nhận
    confirmed_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Người xác nhận
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to Menu
    menu = db.relationship('Menu', backref='registrations', lazy=True)
    
    def __repr__(self):
        return f'<MealRegistration {self.id}>'


class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner
    dish_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_special = db.Column(db.Boolean, default=False)  # Special diet option
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Menu {self.date} - {self.dish_name}>'








class ExitEntryRequest(db.Model):
    __tablename__ = 'exit_entry_requests'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    # Request info
    request_date = db.Column(db.Date, nullable=False)
    exit_time = db.Column(db.Time)  # Thời gian ra
    entry_time = db.Column(db.Time)  # Thời gian vào
    reason = db.Column(db.Text, nullable=False)

    # Approval status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected

    # Manager approval
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    manager_approved_at = db.Column(db.DateTime)
    manager_comment = db.Column(db.Text)

    # HR approval
    hr_approved = db.Column(db.Boolean, default=False)
    hr_approved_at = db.Column(db.DateTime)
    hr_comment = db.Column(db.Text)

    # Security confirmation
    security_confirmed = db.Column(db.Boolean, default=False)
    security_confirmed_at = db.Column(db.DateTime)
    security_comment = db.Column(db.Text)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='exit_entry_requests')
    manager = db.relationship('User', foreign_keys=[manager_id])

    def __repr__(self):
        return f'<ExitEntryRequest {self.id} - {self.status}>'



class AutoRegisterLog(db.Model):
    """Lịch sử tự động đăng ký suất ăn"""
    __tablename__ = 'auto_register_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    run_date = db.Column(db.Date, nullable=False)  # Ngày chạy auto-register
    run_time = db.Column(db.DateTime, nullable=False)  # Thời gian chạy
    target_date = db.Column(db.Date, nullable=False)  # Ngày đăng ký (ngày mai)
    total_users = db.Column(db.Integer, default=0)  # Tổng số user
    already_registered = db.Column(db.Integer, default=0)  # Đã đăng ký trước
    auto_registered = db.Column(db.Integer, default=0)  # Tự động đăng ký
    status = db.Column(db.String(20), default='success')  # success, failed
    error_message = db.Column(db.Text)  # Thông báo lỗi nếu có
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AutoRegisterLog {self.run_date} - {self.status}>'
