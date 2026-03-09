"""
Unit tests for database models
"""
import unittest
from datetime import datetime, date, time
from app import app, db
from models import User, OvertimeRequest, MealRegistration
from werkzeug.security import generate_password_hash, check_password_hash


class TestUserModel(unittest.TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_user(self):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                employee_id='TEST001',
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                department='IT'
            )
            db.session.add(user)
            db.session.commit()
            
            # Verify user was created
            found_user = User.query.filter_by(employee_id='TEST001').first()
            self.assertIsNotNone(found_user)
            self.assertEqual(found_user.name, 'Test User')
            self.assertEqual(found_user.email, 'test@example.com')
    
    def test_user_password_hashing(self):
        """Test password hashing"""
        with app.app_context():
            password = 'mypassword123'
            hashed = generate_password_hash(password)
            
            user = User(
                employee_id='TEST002',
                name='Test User 2',
                email='test2@example.com',
                password=hashed,
                department='HR'
            )
            db.session.add(user)
            db.session.commit()
            
            # Verify password check works
            found_user = User.query.filter_by(employee_id='TEST002').first()
            self.assertTrue(check_password_hash(found_user.password, password))
            self.assertFalse(check_password_hash(found_user.password, 'wrongpassword'))
    
    def test_user_relationships(self):
        """Test user relationships with overtime and meals"""
        with app.app_context():
            # Create user
            user = User(
                employee_id='TEST003',
                name='Test User 3',
                email='test3@example.com',
                password=generate_password_hash('password123'),
                department='Production'
            )
            db.session.add(user)
            db.session.commit()
            
            # Create overtime request
            overtime = OvertimeRequest(
                user_id=user.id,
                date=date.today(),
                start_time=time(18, 0),
                end_time=time(20, 0),
                reason='Project deadline'
            )
            db.session.add(overtime)
            
            # Create meal registration
            meal = MealRegistration(
                user_id=user.id,
                date=date.today(),
                has_meal=True
            )
            db.session.add(meal)
            db.session.commit()
            
            # Verify relationships
            found_user = User.query.filter_by(employee_id='TEST003').first()
            self.assertEqual(len(found_user.overtime_requests), 1)
            self.assertEqual(len(found_user.meal_registrations), 1)


class TestOvertimeRequestModel(unittest.TestCase):
    """Test cases for OvertimeRequest model"""
    
    def setUp(self):
        """Set up test database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(
                employee_id='TEST001',
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                department='IT'
            )
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_overtime_request(self):
        """Test creating overtime request"""
        with app.app_context():
            user = User.query.first()
            
            overtime = OvertimeRequest(
                user_id=user.id,
                date=date.today(),
                start_time=time(18, 0),
                end_time=time(21, 0),
                reason='Urgent project work',
                status='pending'
            )
            db.session.add(overtime)
            db.session.commit()
            
            # Verify overtime request
            found = OvertimeRequest.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(found)
            self.assertEqual(found.reason, 'Urgent project work')
            self.assertEqual(found.status, 'pending')
    
    def test_overtime_status_values(self):
        """Test overtime status values"""
        with app.app_context():
            user = User.query.first()
            
            for status in ['pending', 'approved', 'rejected']:
                overtime = OvertimeRequest(
                    user_id=user.id,
                    date=date.today(),
                    start_time=time(18, 0),
                    end_time=time(20, 0),
                    reason=f'Test {status}',
                    status=status
                )
                db.session.add(overtime)
            
            db.session.commit()
            
            # Verify all statuses
            self.assertEqual(OvertimeRequest.query.filter_by(status='pending').count(), 1)
            self.assertEqual(OvertimeRequest.query.filter_by(status='approved').count(), 1)
            self.assertEqual(OvertimeRequest.query.filter_by(status='rejected').count(), 1)


class TestMealRegistrationModel(unittest.TestCase):
    """Test cases for MealRegistration model"""
    
    def setUp(self):
        """Set up test database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(
                employee_id='TEST001',
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                department='IT'
            )
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_meal_registration(self):
        """Test creating meal registration"""
        with app.app_context():
            user = User.query.first()
            
            meal = MealRegistration(
                user_id=user.id,
                date=date.today(),
                has_meal=True,
                notes='Vegetarian option'
            )
            db.session.add(meal)
            db.session.commit()
            
            # Verify meal registration
            found = MealRegistration.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(found)
            self.assertTrue(found.has_meal)
            self.assertEqual(found.notes, 'Vegetarian option')


if __name__ == '__main__':
    unittest.main()
