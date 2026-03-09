# Tests - OKI Vietnam HR System

## Cấu Trúc Tests

```
tests/
├── __init__.py           # Package initialization
├── test_auth.py          # Authentication tests
├── test_models.py        # Database model tests
├── test_routes.py        # Route integration tests
├── test_forms.py         # Form validation tests
└── README.md            # This file
```

## Các Loại Tests

### 1. test_auth.py - Authentication Tests
Kiểm tra các chức năng xác thực:
- ✅ Login thành công
- ✅ Login với thông tin sai
- ✅ Logout
- ✅ Đăng ký user mới
- ✅ Đăng ký với employee_id trùng
- ✅ Phân quyền admin
- ✅ Bảo vệ routes với @login_required

### 2. test_models.py - Model Tests
Kiểm tra database models:
- ✅ Tạo User
- ✅ Hash password
- ✅ Relationships (User -> OvertimeRequest, MealRegistration)
- ✅ Tạo OvertimeRequest với các status
- ✅ Tạo MealRegistration

### 3. test_routes.py - Route Tests
Kiểm tra các routes:
- ✅ Index redirect
- ✅ Dashboard access
- ✅ Overtime submission
- ✅ Meal registration
- ✅ Profile page
- ✅ Change password
- ✅ Language switching

### 4. test_forms.py - Form Validation Tests
Kiểm tra form validation:
- ✅ LoginForm validation
- ✅ RegisterForm validation
- ✅ Password mismatch detection
- ✅ Email validation
- ✅ Duplicate employee_id detection
- ✅ OvertimeForm validation
- ✅ ChangePasswordForm validation

## Chạy Tests

### Chạy Tất Cả Tests
```bash
python -m pytest tests/
```

Hoặc với unittest:
```bash
python -m unittest discover tests/
```

### Chạy Test Cụ Thể
```bash
# Chạy authentication tests
python -m pytest tests/test_auth.py

# Chạy model tests
python -m pytest tests/test_models.py

# Chạy route tests
python -m pytest tests/test_routes.py

# Chạy form tests
python -m pytest tests/test_forms.py
```

### Chạy Test Case Cụ Thể
```bash
python -m pytest tests/test_auth.py::TestAuthentication::test_login_success
```

### Chạy Với Coverage
```bash
# Cài đặt coverage
pip install pytest-cov

# Chạy với coverage report
python -m pytest tests/ --cov=. --cov-report=html

# Xem report
# Mở htmlcov/index.html trong browser
```

## Cài Đặt Dependencies Cho Testing

```bash
pip install pytest pytest-cov
```

Hoặc thêm vào requirements.txt:
```
pytest==7.4.3
pytest-cov==4.1.0
```

## Test Database

Tests sử dụng SQLite in-memory database:
- Không ảnh hưởng đến database thật
- Tự động tạo và xóa sau mỗi test
- Nhanh và độc lập

## Best Practices

1. **Isolation**: Mỗi test độc lập, không phụ thuộc vào test khác
2. **setUp/tearDown**: Tạo và dọn dẹp test data
3. **Descriptive Names**: Tên test mô tả rõ ràng
4. **Assertions**: Kiểm tra kết quả cụ thể
5. **Coverage**: Đảm bảo coverage > 80%

## Thêm Tests Mới

### Template cho Test Case Mới

```python
import unittest
from app import app, db
from models import User

class TestNewFeature(unittest.TestCase):
    """Test cases for new feature"""
    
    def setUp(self):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_something(self):
        """Test description"""
        # Arrange
        # Act
        # Assert
        pass

if __name__ == '__main__':
    unittest.main()
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors
```bash
# Đảm bảo PYTHONPATH đúng
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Errors
- Kiểm tra SQLAlchemy URI
- Đảm bảo models được import đúng
- Verify db.create_all() được gọi trong setUp

### CSRF Errors
- Disable CSRF trong test config: `WTF_CSRF_ENABLED = False`

## Kết Quả Mong Đợi

Khi chạy tất cả tests:
```
tests/test_auth.py ........... (11 tests)
tests/test_models.py ........ (8 tests)
tests/test_routes.py ......... (9 tests)
tests/test_forms.py .......... (10 tests)

========== 38 passed in 2.5s ==========
```

## Next Steps

- [ ] Thêm integration tests cho overtime approval workflow
- [ ] Thêm tests cho email notifications
- [ ] Thêm performance tests
- [ ] Thêm security tests
- [ ] Thêm API tests (nếu có REST API)
