# OKI Vietnam HR System - Project Structure

## 📁 Cấu Trúc Project

```
SystemHR/
├── 📱 Core Application
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration (Database, JWT, Session)
│   ├── forms.py                    # WTForms (Login, Register, Overtime, etc.)
│   ├── translations.py             # Translation utilities
│   └── translations.ini            # Translation data (vi/en/ja)
│
├── 🗄️ Database
│   └── models/
│       └── __init__.py             # SQLAlchemy models (User, Overtime, Meal)
│
├── 🌐 API
│   └── api/
│       ├── __init__.py             # API Blueprint
│       ├── auth.py                 # JWT authentication endpoints
│       ├── overtime.py             # Overtime API endpoints
│       └── meals.py                # Meal API endpoints
│
├── 🎨 Frontend
│   ├── templates/                  # HTML templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── overtime.html
│   │   ├── meals.html
│   │   ├── profile.html
│   │   └── ...
│   └── static/                     # Static files
│       ├── manifest.json           # PWA manifest
│       ├── service-worker.js       # PWA service worker
│       └── icon.svg                # App icon
│
├── 🔧 Scripts
│   ├── __init__.py
│   ├── setup.py                    # Installation wizard
│   ├── init_db.py                  # Database initialization
│   ├── auto_setup_db.py            # Auto database setup
│   ├── update_db_schema.py         # Schema migration
│   └── run_tests.py                # Test runner
│
├── 🧪 Tests
│   ├── __init__.py
│   ├── README.md
│   ├── test_auth.py                # Authentication tests
│   ├── test_models.py              # Model tests
│   ├── test_routes.py              # Route tests
│   └── test_forms.py               # Form tests
│
├── 📚 Documentation
│   ├── README.md                   # Main documentation
│   ├── API_DOCUMENTATION.md        # API reference
│   ├── AUTO_SETUP_GUIDE.md         # Database setup guide
│   ├── ADD_NEW_MODEL_GUIDE.md      # Model creation guide
│   └── CONTRIBUTING.md             # Contributing guide
│
├── ⚙️ Configuration Files
│   ├── .env                        # Environment variables (not in git)
│   ├── .env.example                # Environment template
│   ├── requirements.txt            # Python dependencies
│   ├── runtime.txt                 # Python version
│   ├── Procfile                    # Railway deployment
│   └── .gitignore                  # Git ignore rules
│
└── 📄 Root Files
    ├── README.md                   # Project overview
    └── PROJECT_STRUCTURE.md        # This file
```

## 🎯 File Purposes

### Core Files
- **app.py** (500+ lines) - Main application with routes, middleware, Flask-Login
- **config.py** - Database config, JWT config, session config
- **forms.py** - WTForms for login, register, overtime, etc.
- **translations.py** - Multi-language support utilities

### Models
- **models/__init__.py** - User, OvertimeRequest, MealRegistration models

### API
- **api/auth.py** - JWT login, register, refresh token
- **api/overtime.py** - CRUD overtime requests, approve/reject
- **api/meals.py** - CRUD meal registrations

### Scripts (Utilities)
- **setup.py** - Interactive setup wizard
- **auto_setup_db.py** - Auto-create database & tables
- **init_db.py** - Manual database initialization
- **update_db_schema.py** - Add new columns to existing tables
- **run_tests.py** - Run all tests with coverage

## 🚀 Quick Commands

### Development
```bash
# Setup
python scripts/setup.py

# Run app
python app.py

# Initialize database
python scripts/auto_setup_db.py

# Run tests
python scripts/run_tests.py
```

### Production
```bash
# Deploy to Railway
git push

# Manual deployment
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Statistics

- **Total Python Files**: 15+
- **Total Templates**: 10+
- **Total Tests**: 38 test cases
- **Lines of Code**: ~3000+
- **API Endpoints**: 15+
- **Database Tables**: 3

## 🔑 Key Features

1. ✅ **Web UI** - Flask-Login session-based
2. ✅ **REST API** - JWT Bearer token authentication
3. ✅ **Auto Database Setup** - Creates DB & tables automatically
4. ✅ **Multi-language** - Vietnamese, English, Japanese
5. ✅ **PWA Support** - Install as mobile app
6. ✅ **Admin Panel** - Flask-Admin at /admin
7. ✅ **Auto Logout** - After 3 weeks inactivity
8. ✅ **Comprehensive Tests** - Unit & integration tests

## 🎯 Design Principles

### 1. Separation of Concerns
- **Core Application** (`app.py`, `config.py`, `forms.py`) - Main business logic
- **Models** (`models/`) - Database layer
- **API** (`api/`) - REST API endpoints with JWT
- **Scripts** (`scripts/`) - Utility scripts and tools
- **Tests** (`tests/`) - Test suites
- **Docs** (`docs/`) - Documentation

### 2. Keep It Simple
- Flat structure for easy navigation
- No deep nesting (max 2 levels)
- Clear naming conventions
- Single responsibility per file

### 3. Scalability
- Modular design allows easy extension
- Blueprint pattern for API
- SQLAlchemy models auto-detected
- Easy to add new features

## 🔄 Adding New Features

### Add New Model
1. Edit `models/__init__.py`
2. Add new SQLAlchemy model class
3. Run `python scripts/auto_setup_db.py`
4. Table created automatically!

📖 See: `docs/ADD_NEW_MODEL_GUIDE.md`

### Add New API Endpoint
1. Create new file in `api/` (e.g., `api/reports.py`)
2. Import blueprint: `from . import api_bp`
3. Add routes with `@api_bp.route()`
4. Import in `api/__init__.py`

### Add New Page
1. Create HTML template in `templates/`
2. Add route in `app.py`
3. Add navigation link in templates
4. Add translations in `translations.ini`

### Add New Script
1. Create Python file in `scripts/`
2. Add docstring explaining purpose
3. Make it executable: `if __name__ == '__main__':`
4. Update documentation

## 📂 File Organization Rules

### Core Files (Root Level)
- `app.py` - Main application (keep under 600 lines)
- `config.py` - Configuration (Database, JWT, Session, etc.)
- `forms.py` - All WTForms definitions
- `translations.py` - Translation utilities
- `translations.ini` - Translation data

### Models (models/)
- `__init__.py` - All SQLAlchemy models
- Keep models simple and focused
- Use relationships for foreign keys

### API (api/)
- `__init__.py` - Blueprint registration
- `auth.py` - Authentication endpoints
- `overtime.py` - Overtime endpoints
- `meals.py` - Meal endpoints
- One file per resource type

### Scripts (scripts/)
- `setup.py` - Installation wizard
- `auto_setup_db.py` - Auto database setup
- `init_db.py` - Manual initialization
- `update_db_schema.py` - Schema migrations
- `run_tests.py` - Test runner

### Tests (tests/)
- `test_auth.py` - Authentication tests
- `test_models.py` - Model tests
- `test_routes.py` - Route tests
- `test_forms.py` - Form tests
- One test file per module

### Documentation (docs/)
- `README.md` - Main documentation
- `API_DOCUMENTATION.md` - API reference
- `QUICKSTART.md` - Quick start guide
- `AUTO_SETUP_GUIDE.md` - Database setup
- `ADD_NEW_MODEL_GUIDE.md` - Model creation

## 🚫 What NOT to Do

❌ Don't create deep folder nesting  
❌ Don't mix concerns (e.g., API logic in templates)  
❌ Don't put business logic in templates  
❌ Don't create files with multiple responsibilities  
❌ Don't skip documentation for new features  
❌ Don't commit `.env` file (use `.env.example`)  
❌ Don't hardcode credentials in code  

## ✅ Best Practices

✅ Use virtual environment (`.venv/`)  
✅ Keep dependencies updated (`requirements.txt`)  
✅ Write tests for new features  
✅ Document API endpoints  
✅ Use type hints in Python code  
✅ Follow PEP 8 style guide  
✅ Use meaningful variable names  
✅ Add docstrings to functions  
✅ Keep functions small and focused  
✅ Use environment variables for config  

## 📊 Code Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Total Python Files | 15+ | ✅ Good |
| Total Templates | 10+ | ✅ Good |
| Total Tests | 38 | ✅ Good |
| Lines of Code | ~3000+ | ✅ Good |
| API Endpoints | 15+ | ✅ Good |
| Database Tables | 3 | ✅ Good |
| Max File Size | ~500 lines | ✅ Good |
| Test Coverage | ~80% | ✅ Good |

## 🔍 Finding Files

### By Feature
- **Authentication**: `app.py`, `api/auth.py`, `forms.py`, `templates/login.html`
- **Overtime**: `app.py`, `api/overtime.py`, `templates/overtime.html`, `models/__init__.py`
- **Meals**: `app.py`, `api/meals.py`, `templates/meals.html`, `models/__init__.py`
- **Admin**: `app.py`, `templates/admin_dashboard.html`
- **Profile**: `app.py`, `templates/profile.html`, `templates/change_password.html`

### By Type
- **Routes**: `app.py` (web), `api/*.py` (REST API)
- **Models**: `models/__init__.py`
- **Forms**: `forms.py`
- **Config**: `config.py`
- **Utils**: `translations.py`
- **Templates**: `templates/*.html`
- **Tests**: `tests/test_*.py`
- **Scripts**: `scripts/*.py`
- **Docs**: `docs/*.md`

## 📝 Notes

- Keep structure flat for simplicity
- Scripts in separate folder for organization
- Documentation in docs/ folder
- Tests in tests/ folder
- API in api/ folder (Blueprint)
- One feature = one set of files (model, route, template, API)

---

**Last Updated**: 2026-03-05  
**Version**: 2.0.0  
**Maintained by**: OKI VIETNAM IT Team
