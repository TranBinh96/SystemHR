"""
Unit tests for WTForms
"""
import unittest
from app import app, db
from models import User
from forms import LoginForm, RegisterForm, OvertimeForm, ChangePasswordForm
from werkzeug.security import generate_password_hash
from datetime import date, time


class TestForms(unittest.TestCase):
    """Test cases for form validation"""
    
    def setUp(self):
        """Set up test app and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()
    
    def tearDown(self):
        """Clean up"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_login_form_valid(self):
        """Test valid login form"""
        form = LoginForm(data={
            'employee_id': 'TEST001',
            'password': 'password123'
        })
        self.assertTrue(form.validate())
    
    def test_login_form_missing_fields(self):
        """Test login form with missing fields"""
        form = LoginForm(data={
            'employee_id': '',
            'password': ''
        })
        self.assertFalse(form.validate())
    
    def test_register_form_valid(self):
        """Test valid registration form"""
        form = RegisterForm(data={
            'employee_id': 'TEST001',
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'production',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertTrue(form.validate())
    
    def test_register_form_password_mismatch(self):
        """Test registration with mismatched passwords"""
        form = RegisterForm(data={
            'employee_id': 'TEST001',
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'production',
            'password': 'password123',
            'confirm_password': 'different123'
        })
        self.assertFalse(form.validate())
    
    def test_register_form_short_password(self):
        """Test registration with short password"""
        form = RegisterForm(data={
            'employee_id': 'TEST001',
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'production',
            'password': 'short',
            'confirm_password': 'short'
        })
        self.assertFalse(form.validate())
    
    def test_register_form_invalid_email(self):
        """Test registration with invalid email"""
        form = RegisterForm(data={
            'employee_id': 'TEST001',
            'name': 'Test User',
            'email': 'invalid-email',
            'department': 'production',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())
    
    def test_register_form_duplicate_employee_id(self):
        """Test registration with duplicate employee ID"""
        # Create existing user
        user = User(
            employee_id='TEST001',
            name='Existing User',
            email='existing@example.com',
            password=generate_password_hash('password123'),
            department='IT'
        )
        db.session.add(user)
        db.session.commit()
        
        # Try to register with same employee_id
        form = RegisterForm(data={
            'employee_id': 'TEST001',
            'name': 'New User',
            'email': 'new@example.com',
            'department': 'production',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertFalse(form.validate())
    
    def test_overtime_form_valid(self):
        """Test valid overtime form"""
        form = OvertimeForm(data={
            'date': date.today(),
            'start_time': time(18, 0),
            'end_time': time(21, 0),
            'reason': 'Project deadline approaching, need extra time to complete tasks'
        })
        self.assertTrue(form.validate())
    
    def test_overtime_form_short_reason(self):
        """Test overtime form with short reason"""
        form = OvertimeForm(data={
            'date': date.today(),
            'start_time': time(18, 0),
            'end_time': time(21, 0),
            'reason': 'Short'  # Less than 10 characters
        })
        self.assertFalse(form.validate())
    
    def test_change_password_form_valid(self):
        """Test valid change password form"""
        form = ChangePasswordForm(data={
            'current_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        self.assertTrue(form.validate())
    
    def test_change_password_form_mismatch(self):
        """Test change password with mismatched passwords"""
        form = ChangePasswordForm(data={
            'current_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'different123'
        })
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
