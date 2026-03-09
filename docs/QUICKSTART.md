# Quick Start Guide - OKI VIETNAM HR System

## 🚀 Bắt đầu nhanh trong 5 phút

### Bước 1: Clone và cài đặt
```bash
# Clone repository
git clone <repository-url>
cd SystemHR

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Cấu hình database
```bash
# Copy file .env.example thành .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Chỉnh sửa .env với thông tin MySQL của bạn
# DB_HOST=10.216.28.11
# DB_PORT=3306
# DB_USER=ovnm
# DB_PASSWORD=P@ssw0rd
# DB_NAME=db_hr
```

### Bước 3: Tự động tạo database
```bash
# Script này sẽ:
# - Tạo database nếu chưa có
# - Tạo tất cả tables tự động
# - Tạo tài khoản admin và user mẫu
python scripts/auto_setup_db.py
```

### Bước 4: Chạy ứng dụng
```bash
python app.py
```

### Bước 5: Truy cập
Mở trình duyệt: **http://localhost:5000**

## 🔑 Tài khoản mặc định

**Admin Account (Quản trị viên):**
- Employee ID: `ADMIN`
- Password: `admin123`
- Quyền: Quản lý toàn bộ hệ thống, phê duyệt overtime

**Test User (Nhân viên):**
- Employee ID: `EMP001`
- Password: `password123`
- Quyền: Đăng ký overtime, đăng ký suất ăn

⚠️ **Quan trọng**: Đổi mật khẩu ngay sau lần đăng nhập đầu tiên!

## 📱 Tính năng chính

### Web Application (Session-based)
✅ Đăng nhập / Đăng ký / Quên mật khẩu  
✅ Dashboard với thống kê  
✅ Đăng ký tăng ca (với 2 tab: Đăng ký & Phê duyệt)  
✅ Đăng ký suất ăn theo tuần  
✅ Quản lý profile và đổi mật khẩu  
✅ Admin panel tại `/admin`  
✅ Tự động logout sau 3 tuần không hoạt động  

### REST API (JWT Bearer Token)
✅ JWT Authentication (access + refresh tokens)  
✅ CRUD Overtime requests  
✅ CRUD Meal registrations  
✅ Role-based access control  
✅ API docs tại `docs/API_DOCUMENTATION.md`  

### UI/UX
✅ Responsive design (Mobile + Desktop)  
✅ Đa ngôn ngữ (VI/EN/JA)  
✅ Progressive Web App (PWA)  
✅ Material Design icons  
✅ Tailwind CSS styling  

## 🔧 Cài đặt thủ công (nếu auto_setup_db.py không hoạt động)

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Tạo file .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 3. Chỉnh sửa .env với thông tin database

# 4. Khởi tạo database thủ công
python scripts/init_db.py

# 5. Chạy ứng dụng
python app.py
```

## 📚 Tài liệu chi tiết

- **README.md** - Tổng quan dự án
- **docs/API_DOCUMENTATION.md** - API reference với JWT
- **docs/AUTO_SETUP_GUIDE.md** - Hướng dẫn auto setup database
- **docs/ADD_NEW_MODEL_GUIDE.md** - Hướng dẫn thêm model mới
- **docs/INSTALLATION_STEPS.md** - Hướng dẫn cài đặt chi tiết
- **docs/CHANGELOG.md** - Lịch sử thay đổi
- **PROJECT_STRUCTURE.md** - Cấu trúc dự án

## 🌐 Sử dụng API

### 1. Login và lấy JWT token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"ADMIN","password":"admin123"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "user": {...}
}
```

### 2. Sử dụng token để gọi API
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

📄 Chi tiết API: `docs/API_DOCUMENTATION.md`

## ⚡ Deploy lên Railway

```bash
# 1. Đẩy code lên GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Kết nối Railway với GitHub repository

# 3. Cấu hình environment variables trên Railway:
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=db_hr
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# 4. Railway tự động deploy dựa trên:
# - Procfile (gunicorn config)
# - runtime.txt (Python 3.11.9)
# - requirements.txt (dependencies)
```

## 🧪 Chạy Tests

```bash
# Chạy tất cả tests
python scripts/run_tests.py

# Hoặc dùng pytest trực tiếp
pytest tests/ -v

# Chạy test cụ thể
pytest tests/test_auth.py -v
pytest tests/test_models.py -v
```

## 🆘 Xử lý sự cố

### Không kết nối được database?
```bash
# Kiểm tra MySQL đang chạy
mysql -h 10.216.28.11 -u ovnm -p

# Kiểm tra thông tin trong .env
cat .env  # Linux/Mac
type .env  # Windows
```

### Import errors?
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt --force-reinstall

# Kiểm tra virtual environment đã activate chưa
which python  # Linux/Mac
where python  # Windows
```

### Tables không tồn tại?
```bash
# Chạy lại auto setup
python scripts/auto_setup_db.py

# Hoặc khởi tạo thủ công
python scripts/init_db.py
```

### Module not found errors?
```bash
# Đảm bảo đang ở trong virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Port 5000 đã được sử dụng?
```bash
# Thay đổi port trong app.py (dòng cuối)
# app.run(debug=True, host='0.0.0.0', port=8000)

# Hoặc kill process đang dùng port 5000
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000
```

## 📱 Cài đặt PWA trên Mobile

1. Truy cập website trên mobile (cần HTTPS hoặc localhost)
2. Nhấn menu trình duyệt
3. Chọn "Add to Home Screen" / "Thêm vào màn hình chính"
4. Sử dụng như ứng dụng native

⚠️ **Lưu ý**: PWA chỉ hoạt động với HTTPS (hoặc localhost)

## 🌍 Thay đổi ngôn ngữ

Click vào dropdown ngôn ngữ ở header:
- 🇻🇳 Tiếng Việt (mặc định)
- 🇬🇧 English
- 🇯🇵 日本語

## 🔐 Bảo mật

- ✅ Password hashing với Werkzeug
- ✅ JWT Bearer token authentication
- ✅ CSRF protection
- ✅ Session security (HttpOnly, Secure, SameSite)
- ✅ Auto logout sau 3 tuần không hoạt động
- ✅ Role-based access control

## 📞 Hỗ trợ

- **Email**: admin@okivietnam.com
- **Documentation**: Xem thư mục `docs/`
- **Issues**: Tạo issue trên GitHub

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-05  
**Company**: OKI VIETNAM Co., Ltd.
