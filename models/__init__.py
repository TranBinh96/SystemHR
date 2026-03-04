from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Position {self.code} - {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Department and Position (simple string fields)
    department = db.Column(db.String(100))  # Department name
    position = db.Column(db.String(50))     # Position code (1, 2, 3, 4...)
    
    # Work status: working, business_trip, resigned
    work_status = db.Column(db.String(20), default='working')
    
    # Avatar/Photo
    avatar_url = db.Column(db.String(255))  # Path to avatar image
    
    # Personal Information
    gender = db.Column(db.String(10))  # male, female, other
    phone = db.Column(db.String(20))  # Phone number
    citizen_id = db.Column(db.String(20))  # CCCD/ID card number
    hometown = db.Column(db.String(200))  # Quê quán
    
    role = db.Column(db.String(20), default='user')  # user, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    overtime_requests = db.relationship('OvertimeRequest', 
                                       foreign_keys='OvertimeRequest.user_id',
                                       backref='user', 
                                       lazy=True)
    meal_registrations = db.relationship('MealRegistration', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.employee_id} - Position {self.position}>'
    
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
        Returns users in the same department with lower position code (higher authority).
        Logic: Code càng nhỏ = cấp càng cao (1 > 2 > 3 > 4)
        """
        if not self.department or not self.position:
            return []
        
        try:
            my_code = int(self.position)
        except (ValueError, TypeError):
            return []
        
        # Find users in same department with lower code (higher authority)
        approvers = User.query.filter(
            User.department == self.department,
            User.position.isnot(None),
            User.is_active == True,
            User.id != self.id
        ).all()
        
        # Filter by code comparison
        result = []
        for user in approvers:
            try:
                user_code = int(user.position)
                if user_code < my_code:  # Lower code = higher authority
                    result.append(user)
            except (ValueError, TypeError):
                continue
        
        # Sort by code ascending (highest authority first)
        result.sort(key=lambda u: int(u.position))
        return result
    
    def can_approve_for(self, user):
        """
        Check if this user can approve overtime for another user.
        Returns True if this user has lower code (higher authority) in same department.
        """
        if not self.department or not user.department or not self.position or not user.position:
            return False
        
        # Must be same department
        if self.department != user.department:
            return False
        
        try:
            my_code = int(self.position)
            their_code = int(user.position)
            return my_code < their_code and self.is_active  # Lower code = can approve
        except (ValueError, TypeError):
            return False
    
    def get_subordinates(self):
        """
        Get list of users this user can approve for.
        Returns users in the same department with higher code (lower authority).
        """
        if not self.department or not self.position:
            return []
        
        try:
            my_code = int(self.position)
        except (ValueError, TypeError):
            return []
        
        # Find users in same department with higher code (lower authority)
        subordinates = User.query.filter(
            User.department == self.department,
            User.position.isnot(None),
            User.is_active == True,
            User.id != self.id
        ).all()
        
        # Filter by code comparison
        result = []
        for user in subordinates:
            try:
                user_code = int(user.position)
                if user_code > my_code:  # Higher code = lower authority
                    result.append(user)
            except (ValueError, TypeError):
                continue
        
        # Sort by code ascending
        result.sort(key=lambda u: int(u.position))
        return result
    
    def is_manager(self):
        """Check if user is a manager (has subordinates)"""
        return len(self.get_subordinates()) > 0


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
