"""
Integration tests for application routes
"""
import unittest
from datetime import date, time
from app import app, db
from models import User, OvertimeRequest, MealRegistration
from werkzeug.security import generate_password_hash


class TestRoutes(unittest.TestCase):
    """Test cases for application routes"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(
                employee_id='TEST001',
                name='Test User',
                email='test@example.com',
                password=generate_password_hash('password123'),
                department='IT',
                role='user'
            )
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def login(self):
        """Helper method to login"""
        return self.client.post('/login', data={
            'employee_id': 'TEST001',
            'password': 'password123'
        }, follow_redirects=True)
    
    def test_index_redirect(self):
        """Test index redirects to login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_after_login(self):
        """Test dashboard accessible after login"""
        self.login()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_overtime_page_loads(self):
        """Test overtime page loads after login"""
        self.login()
        response = self.client.get('/overtime')
        self.assertEqual(response.status_code, 200)
    
    def test_overtime_submission(self):
        """Test overtime request submission"""
        self.login()
        
        response = self.client.post('/overtime', data={
            'date': date.today().isoformat(),
            'start_time': '18:00',
            'end_time': '21:00',
            'reason': 'Project deadline approaching, need extra time'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify overtime request was created
        with app.app_context():
            overtime = OvertimeRequest.query.first()
            self.assertIsNotNone(overtime)
            self.assertEqual(overtime.status, 'pending')
    
    def test_meals_page_loads(self):
        """Test meals page loads after login"""
        self.login()
        response = self.client.get('/meals')
        self.assertEqual(response.status_code, 200)
    
    def test_meal_registration(self):
        """Test meal registration submission"""
        self.login()
        
        response = self.client.post('/meals', data={
            'date': date.today().isoformat(),
            'has_meal': 'true',
            'notes': 'Vegetarian option'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify meal registration was created
        with app.app_context():
            meal = MealRegistration.query.first()
            self.assertIsNotNone(meal)
            self.assertTrue(meal.has_meal)
    
    def test_profile_page_loads(self):
        """Test profile page loads after login"""
        self.login()
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
    
    def test_change_password_page_loads(self):
        """Test change password page loads after login"""
        self.login()
        response = self.client.get('/change-password')
        self.assertEqual(response.status_code, 200)
    
    def test_change_password_success(self):
        """Test successful password change"""
        self.login()
        
        response = self.client.post('/change-password', data={
            'current_password': 'password123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify password was changed
        with app.app_context():
            from werkzeug.security import check_password_hash
            user = User.query.filter_by(employee_id='TEST001').first()
            self.assertTrue(check_password_hash(user.password, 'newpassword123'))
    
    def test_language_switching(self):
        """Test language switching"""
        response = self.client.get('/set-language/en', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/set-language/ja', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/set-language/vi', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
