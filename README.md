# OKI VIETNAM HR System

Hệ thống quản lý nhân sự, tăng ca và suất ăn cho OKI VIETNAM

## ✨ Tính năng

### Web Application (Session-based)
- ✅ Đăng nhập / Đăng ký / Quên mật khẩu
- ✅ Dashboard với thống kê
- ✅ Đăng ký tăng ca (với phê duyệt)
- ✅ Đăng ký suất ăn theo tuần
- ✅ Quản lý profile và đổi mật khẩu
- ✅ Admin dashboard với Flask-Admin
- ✅ Tự động logout sau 3 tuần không hoạt động

### REST API (JWT Bearer Token)
- ✅ JWT Authentication (access + refresh tokens)
- ✅ CRUD Overtime requests
- ✅ CRUD Meal registrations
- ✅ Role-based access control (admin/user)
- ✅ API documentation tại `docs/API_DOCUMENTATION.md`

### Progressive Web App (PWA)
- ✅ Cài đặt như ứng dụng native trên mobile
- ✅ Offline support với service worker
- ✅ App manifest và icon

### Đa ngôn ngữ
- ✅ Tiếng Việt (mặc định)
- ✅ English
- ✅ 日本語 (Japanese)

### UI/UX
- ✅ Responsive design (Mobile + Desktop)
- ✅ Dark mode support
- ✅ Material Design icons
- ✅ Tailwind CSS styling

## 🚀 Cài đặt nhanh

### 1. Clone repository
```bash
git clone <repository-url>
cd SystemHR
```

### 2. Tạo virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường
```bash
# Copy file .env.example thành .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Chỉnh sửa .env với thông tin MySQL của bạn
```

### 5. Tự động tạo database và tables
```bash
python scripts/auto_setup_db.py
```

### 6. Chạy ứng dụng
```bash
python app.py
```

Server sẽ chạy tại: http://127.0.0.1:5000

## 🔑 Tài khoản mặc định

- **Admin**: `ADMIN` / `admin123` (Quản trị hệ thống)
- **User**: `EMP001` / `password123` (Nhân viên thường)

⚠️ **Lưu ý**: Đổi mật khẩu ngay sau lần đăng nhập đầu tiên!

## 📁 Cấu trúc dự án

```
SystemHR/
├── 📱 Core Application
│   ├── app.py                      # Main Flask application (500+ lines)
│   ├── config.py                   # Configuration (Database, JWT, Session)
│   ├── forms.py                    # WTForms (Login, Register, Overtime, etc.)
│   ├── translations.py             # Translation utilities
│   └── translations.ini            # Translation data (vi/en/ja)
│
├── 🗄️ Database
│   └── models/
│       └── __init__.py             # SQLAlchemy models (User, Overtime, Meal)
│
├── 🌐 API (JWT Bearer Token)
│   └── api/
│       ├── __init__.py             # API Blueprint
│       ├── auth.py                 # JWT authentication endpoints
│       ├── overtime.py             # Overtime API endpoints
│       └── meals.py                # Meal API endpoints
│
├── 🎨 Frontend
│   ├── templates/                  # HTML templates (10+ files)
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── admin_dashboard.html
│   │   ├── overtime.html
│   │   ├── meals.html
│   │   ├── profile.html
│   │   └── ...
│   └── static/                     # Static files
│       ├── manifest.json           # PWA manifest
│       ├── service-worker.js       # PWA service worker
│       └── icon.svg                # App icon
│
├── 🔧 Scripts (Utilities)
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
│   └── ADD_NEW_MODEL_GUIDE.md      # Model creation guide
│
└── ⚙️ Configuration
    ├── .env                        # Environment variables (not in git)
    ├── .env.example                # Environment template
    ├── requirements.txt            # Python dependencies
    ├── runtime.txt                 # Python version (for Railway)
    ├── Procfile                    # Railway deployment config
    └── .gitignore                  # Git ignore rules
```

## 🛠️ Công nghệ sử dụng

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Session management
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Admin** - Admin panel
- **Flask-WTF** - Form validation
- **Flask-Migrate** - Database migrations
- **MySQL Connector** - Database driver

### Frontend
- **Tailwind CSS** - Styling
- **Material Symbols** - Icons
- **Vanilla JavaScript** - Interactivity

### Database
- **MySQL** - Production database

## 📖 Hướng dẫn sử dụng

### Chạy ứng dụng
```bash
# Development
python app.py

# Production (với Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Quản lý database
```bash
# Tự động tạo database và tables
python scripts/auto_setup_db.py

# Khởi tạo database thủ công
python scripts/init_db.py

# Cập nhật schema (thêm cột mới)
python scripts/update_db_schema.py
```

### Chạy tests
```bash
# Chạy tất cả tests
python scripts/run_tests.py

# Hoặc dùng pytest trực tiếp
pytest tests/ -v
```

### Truy cập Admin Panel
```bash
# Đăng nhập với tài khoản admin
# Truy cập: http://127.0.0.1:5000/admin
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - Login và nhận JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Lấy thông tin user hiện tại
- `POST /api/auth/register` - Đăng ký user mới
- `POST /api/auth/change-password` - Đổi mật khẩu

### Overtime
- `GET /api/overtime` - Lấy danh sách overtime requests
- `POST /api/overtime` - Tạo overtime request mới
- `GET /api/overtime/<id>` - Lấy chi tiết overtime request
- `PUT /api/overtime/<id>` - Cập nhật overtime request
- `DELETE /api/overtime/<id>` - Xóa overtime request
- `POST /api/overtime/<id>/approve` - Phê duyệt (admin only)
- `POST /api/overtime/<id>/reject` - Từ chối (admin only)

### Meals
- `GET /api/meals` - Lấy danh sách meal registrations
- `POST /api/meals` - Tạo meal registration mới
- `GET /api/meals/<id>` - Lấy chi tiết meal registration
- `PUT /api/meals/<id>` - Cập nhật meal registration
- `DELETE /api/meals/<id>` - Xóa meal registration

📄 Chi tiết API: `docs/API_DOCUMENTATION.md`

## 🔐 Bảo mật

- ✅ Password hashing với Werkzeug
- ✅ JWT Bearer token authentication
- ✅ CSRF protection với Flask-WTF
- ✅ Session security (HttpOnly, Secure, SameSite)
- ✅ Auto logout sau 3 tuần không hoạt động
- ✅ Role-based access control (admin/user)

## 🚢 Deploy lên Railway

```bash
# 1. Đẩy code lên Git
git add .
git commit -m "Deploy to Railway"
git push

# 2. Railway sẽ tự động deploy dựa trên:
#    - Procfile (gunicorn config)
#    - runtime.txt (Python version)
#    - requirements.txt (dependencies)

# 3. Cấu hình environment variables trên Railway:
#    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
#    - SECRET_KEY, JWT_SECRET_KEY
```

## 📱 PWA (Progressive Web App)

Ứng dụng hỗ trợ cài đặt như app native trên mobile:

1. Truy cập website trên mobile (cần HTTPS)
2. Nhấn "Add to Home Screen"
3. Sử dụng như ứng dụng thông thường

⚠️ **Lưu ý**: PWA chỉ hoạt động với HTTPS (hoặc localhost)

## 🌍 Đa ngôn ngữ

Thay đổi ngôn ngữ qua dropdown ở header:
- 🇻🇳 Tiếng Việt (mặc định)
- 🇬🇧 English
- 🇯🇵 日本語

Thêm ngôn ngữ mới: Chỉnh sửa file `translations.ini`

## 🧪 Testing

```bash
# Chạy tất cả tests
python scripts/run_tests.py

# Chạy test cụ thể
pytest tests/test_auth.py -v
pytest tests/test_models.py -v
pytest tests/test_routes.py -v
pytest tests/test_forms.py -v
```

## 📊 Thống kê

- **Total Python Files**: 15+
- **Total Templates**: 10+
- **Total Tests**: 38 test cases
- **Lines of Code**: ~3000+
- **API Endpoints**: 15+
- **Database Tables**: 3 (users, overtime_requests, meal_registrations)

## 🤝 Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

© 2024-2026 OKI VIETNAM Co., Ltd. All rights reserved.

## 📞 Liên hệ

- **Company**: OKI VIETNAM Co., Ltd.
- **Email**: admin@okivietnam.com
- **Website**: https://okivietnam.com

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-05
