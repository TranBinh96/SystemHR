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


class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Position {self.code} - {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Department and Position
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    
    # Work status
    work_status = db.Column(db.String(20), default='working')
    
    # Personal info
    avatar_url = db.Column(db.String(255))
    
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    
    # Permission fields
    can_approve = db.Column(db.Boolean, default=False)  # Quyền phê duyệt overtime (Manager)
    can_register = db.Column(db.Boolean, default=True)  # Quyền đăng ký suất ăn
    
    # Overtime approver (chỉ dành cho user thường, manager tự phê duyệt)
    overtime_approver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    overtime_requests = db.relationship('OvertimeRequest', 
                                       foreign_keys='OvertimeRequest.user_id',
                                       backref='user', 
                                       lazy=True)
    meal_registrations = db.relationship('MealRegistration', backref='user', lazy=True)
    pos = db.relationship('Position', backref='users', lazy=True)
    overtime_approver = db.relationship('User', remote_side=[id], backref='overtime_subordinates', foreign_keys=[overtime_approver_id])
    
    def __repr__(self):
        return f'<User {self.employee_id} - Position ID {self.position_id}>'
    
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
    position = db.Column(db.String(50))
    
    # Overtime info
    overtime_date = db.Column(db.Date, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False, default=1)  # Số người đăng ký
    reason = db.Column(db.Text, nullable=False)
    
    # Legacy fields (kept for backward compatibility, nullable)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    total_hours = db.Column(db.Numeric(4, 2), nullable=True)
    
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
    position = db.Column(db.String(50))
    
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


class ApprovalHierarchy(db.Model):
    __tablename__ = 'approval_hierarchy'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    approver_position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    approvee_position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    can_approve = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', backref='approval_rules', lazy=True)
    approver_position = db.relationship('Position', foreign_keys=[approver_position_id], backref='can_approve_positions', lazy=True)
    approvee_position = db.relationship('Position', foreign_keys=[approvee_position_id], backref='approved_by_positions', lazy=True)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('department_id', 'approver_position_id', 'approvee_position_id', 
                          name='unique_approval_rule'),
    )
    
    def __repr__(self):
        return f'<ApprovalHierarchy Dept:{self.department_id} {self.approver_position_id}->{self.approvee_position_id}>'
    
    @staticmethod
    def can_user_approve(approver_user, approvee_user):
        """
        Check if approver_user can approve requests from approvee_user
        based on department and position hierarchy
        """
        if not approver_user.department_id or not approvee_user.department_id:
            return False
        
        if approver_user.department_id != approvee_user.department_id:
            return False
        
        if not approver_user.position_id or not approvee_user.position_id:
            return False
        
        # Check approval hierarchy
        rule = ApprovalHierarchy.query.filter_by(
            department_id=approver_user.department_id,
            approver_position_id=approver_user.position_id,
            approvee_position_id=approvee_user.position_id,
            can_approve=True
        ).first()
        
        return rule is not None
    
    @staticmethod
    def get_approvers_for_user(user):
        """
        Get list of users who can approve for the given user
        based on approval hierarchy
        """
        if not user.department_id or not user.position_id:
            return []
        
        # Find approval rules for this user's position in their department
        rules = ApprovalHierarchy.query.filter_by(
            department_id=user.department_id,
            approvee_position_id=user.position_id,
            can_approve=True
        ).all()
        
        if not rules:
            return []
        
        # Get approver position IDs
        approver_position_ids = [rule.approver_position_id for rule in rules]
        
        # Find active users with those positions in the same department
        approvers = User.query.filter(
            User.department_id == user.department_id,
            User.position_id.in_(approver_position_ids),
            User.is_active == True,
            User.work_status.in_(['working', 'business_trip']),
            User.id != user.id
        ).all()
        
        return approvers
    
    @staticmethod
    def get_approvees_for_user(user):
        """
        Get list of users that the given user can approve for
        based on approval hierarchy
        """
        if not user.department_id or not user.position_id:
            return []
        
        # Find approval rules where this user's position is the approver
        rules = ApprovalHierarchy.query.filter_by(
            department_id=user.department_id,
            approver_position_id=user.position_id,
            can_approve=True
        ).all()
        
        if not rules:
            return []
        
        # Get approvee position IDs
        approvee_position_ids = [rule.approvee_position_id for rule in rules]
        
        # Find active users with those positions in the same department
        approvees = User.query.filter(
            User.department_id == user.department_id,
            User.position_id.in_(approvee_position_ids),
            User.is_active == True,
            User.work_status.in_(['working', 'business_trip']),
            User.id != user.id
        ).all()
        
        return approvees





class ExitEntryRequest(db.Model):
    __tablename__ = 'exit_entry_requests'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))

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
