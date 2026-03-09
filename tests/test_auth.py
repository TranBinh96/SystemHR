"""
Integration tests for authentication
"""
import unittest
from app import app, db
from models import User
from werkzeug.security import generate_password_hash


class TestAuthentication(unittest.TestCase):
    """Test cases for authentication routes"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
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
            
            # Create admin user
            admin = User(
                employee_id='ADMIN',
                name='Admin User',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                department='IT',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    def tearDown(self):
        """Clean up test database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/login', data={
            'employee_id': 'TEST001',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/login', data={
            'employee_id': 'TEST001',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid', response.data)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = self.client.post('/login', data={
            'employee_id': 'NONEXISTENT',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid', response.data)
    
    def test_logout(self):
        """Test logout functionality"""
        # Login first
        self.client.post('/login', data={
            'employee_id': 'TEST001',
            'password': 'password123'
        })
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_protected_route_requires_login(self):
        """Test that protected routes require login"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
    
    def test_register_new_user(self):
        """Test user registration"""
        response = self.client.post('/register', data={
            'employee_id': 'TEST002',
            'name': 'New User',
            'email': 'newuser@example.com',
            'department': 'production',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify user was created
        with app.app_context():
            user = User.query.filter_by(employee_id='TEST002').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'New User')
    
    def test_register_duplicate_employee_id(self):
        """Test registration with duplicate employee ID"""
        response = self.client.post('/register', data={
            'employee_id': 'TEST001',  # Already exists
            'name': 'Duplicate User',
            'email': 'duplicate@example.com',
            'department': 'hr',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'already exists', response.data)
    
    def test_admin_access(self):
        """Test admin can access admin dashboard"""
        # Login as admin
        self.client.post('/login', data={
            'employee_id': 'ADMIN',
            'password': 'admin123'
        })
        
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cannot_access_admin(self):
        """Test regular user cannot access admin dashboard"""
        # Login as regular user
        self.client.post('/login', data={
            'employee_id': 'TEST001',
            'password': 'password123'
        })
        
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should be redirected with error message


if __name__ == '__main__':
    unittest.main()
