# Contributing Guide - OKI VIETNAM HR System

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án! Tài liệu này sẽ hướng dẫn bạn cách đóng góp một cách hiệu quả.

## 📋 Mục lục

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

- Tôn trọng mọi người trong cộng đồng
- Sử dụng ngôn ngữ lịch sự và chuyên nghiệp
- Chấp nhận phản hồi mang tính xây dựng
- Tập trung vào những gì tốt nhất cho dự án

## 🚀 Getting Started

### 1. Fork và Clone Repository

```bash
# Fork repository trên GitHub
# Clone fork của bạn
git clone https://github.com/YOUR_USERNAME/SystemHR.git
cd SystemHR

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/SystemHR.git
```

### 2. Setup Development Environment

```bash
# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt

# Setup database
python scripts/auto_setup_db.py

# Chạy tests để đảm bảo mọi thứ hoạt động
python scripts/run_tests.py
```

### 3. Create Feature Branch

```bash
# Sync với upstream
git fetch upstream
git checkout main
git merge upstream/main

# Tạo branch mới
git checkout -b feature/your-feature-name
# hoặc
git checkout -b fix/bug-description
```

## 🔄 Development Workflow

### 1. Make Changes

- Viết code rõ ràng và dễ hiểu
- Follow coding standards (xem bên dưới)
- Thêm comments cho logic phức tạp
- Update documentation nếu cần

### 2. Test Your Changes

```bash
# Chạy tất cả tests
python scripts/run_tests.py

# Chạy test cụ thể
pytest tests/test_auth.py -v

# Kiểm tra code style
flake8 app.py models/ api/

# Kiểm tra type hints
mypy app.py
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit với message rõ ràng
git commit -m "feat: add user profile picture upload"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Create Pull Request

- Mở Pull Request từ fork của bạn đến repository chính
- Điền đầy đủ thông tin trong PR template
- Link đến issue liên quan (nếu có)
- Chờ review và phản hồi

## 📝 Coding Standards

### Python Code Style

Follow **PEP 8** style guide:

```python
# Good
def calculate_overtime_hours(start_time, end_time):
    """Calculate overtime hours between two times."""
    duration = end_time - start_time
    return duration.total_seconds() / 3600

# Bad
def calc(s,e):
    d=e-s
    return d.total_seconds()/3600
```

### Naming Conventions

```python
# Classes: PascalCase
class OvertimeRequest:
    pass

# Functions/Variables: snake_case
def get_user_by_id(user_id):
    employee_name = "John Doe"
    return employee_name

# Constants: UPPER_SNAKE_CASE
MAX_OVERTIME_HOURS = 8
DEFAULT_LANGUAGE = 'vi'

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

### File Organization

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime

# 2. Third-party imports
from flask import Flask, request
from sqlalchemy import Column, Integer

# 3. Local imports
from models import User
from config import Config
```

### Docstrings

```python
def approve_overtime_request(request_id, approver_id):
    """
    Approve an overtime request.
    
    Args:
        request_id (int): ID of the overtime request
        approver_id (int): ID of the approving user
        
    Returns:
        bool: True if approved successfully, False otherwise
        
    Raises:
        ValueError: If request_id or approver_id is invalid
        PermissionError: If approver doesn't have permission
    """
    pass
```

### Type Hints

```python
from typing import List, Optional, Dict

def get_user_overtime_requests(
    user_id: int,
    status: Optional[str] = None
) -> List[Dict[str, any]]:
    """Get overtime requests for a user."""
    pass
```

## 🧪 Testing Guidelines

### Writing Tests

```python
# tests/test_overtime.py
import pytest
from app import app, db
from models import User, OvertimeRequest

class TestOvertimeAPI:
    """Test overtime API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_create_overtime_request(self, client):
        """Test creating overtime request."""
        # Arrange
        data = {
            'date': '2026-03-10',
            'start_time': '18:00',
            'end_time': '20:00',
            'reason': 'Project deadline'
        }
        
        # Act
        response = client.post('/api/overtime', json=data)
        
        # Assert
        assert response.status_code == 201
        assert 'id' in response.json
```

### Test Coverage

- Aim for **80%+ code coverage**
- Test happy paths and edge cases
- Test error handling
- Test authentication and authorization

```bash
# Run with coverage
pytest --cov=. --cov-report=html tests/

# View coverage report
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

## 📦 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat(overtime): add weekly overtime summary"

# Bug fix
git commit -m "fix(auth): resolve JWT token expiration issue"

# Documentation
git commit -m "docs(api): update API documentation with new endpoints"

# Refactoring
git commit -m "refactor(models): simplify User model relationships"

# Multiple lines
git commit -m "feat(meals): add meal preference selection

- Add vegetarian option
- Add allergy notes field
- Update meal registration form

Closes #123"
```

## 🔍 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main branch
- [ ] Commit messages are clear

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI/CD runs tests automatically
2. **Code Review**: At least 1 reviewer approval required
3. **Testing**: Reviewer tests changes locally
4. **Merge**: Maintainer merges PR

### After Merge

```bash
# Sync your fork
git checkout main
git pull upstream main
git push origin main

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g. Windows 11]
- Browser: [e.g. Chrome 120]
- Python version: [e.g. 3.11.9]

**Additional context**
Any other information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other information, mockups, etc.
```

## 📚 Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PEP 8 Style Guide](https://pep8.org/)

### Project Documentation
- `README.md` - Project overview
- `docs/QUICKSTART.md` - Quick start guide
- `docs/API_DOCUMENTATION.md` - API reference
- `PROJECT_STRUCTURE.md` - Project structure

## 🙏 Thank You!

Cảm ơn bạn đã đóng góp cho dự án OKI VIETNAM HR System!

Mọi đóng góp, dù lớn hay nhỏ, đều được đánh giá cao.

---

**Questions?** Contact: admin@okivietnam.com  
**Version**: 2.0.0  
**Last Updated**: 2026-03-05
