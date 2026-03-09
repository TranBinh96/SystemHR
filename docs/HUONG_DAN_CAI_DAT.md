# Hướng Dẫn Cài Đặt - Hệ Thống HR OKI Vietnam

## Những Gì Đã Được Nâng Cấp

Ứng dụng đã được nâng cấp với các Flask extensions:

- **Flask-SQLAlchemy**: ORM để thao tác database
- **Flask-Login**: Quản lý phiên đăng nhập
- **Flask-Admin**: Trang quản trị database
- **Flask-WTF**: Xử lý form với bảo mật CSRF
- **Flask-Migrate**: Công cụ migration database

## Các Bước Cài Đặt

### Cách 1: Sử dụng Script Tự Động (Khuyến nghị)

```bash
python setup.py
```

Script này sẽ tự động:
- Kiểm tra phiên bản Python
- Cài đặt các thư viện cần thiết
- Tạo file .env
- Khởi tạo database (nếu bạn chọn)

### Cách 2: Cài Đặt Thủ Công

#### 1. Cài Đặt Thư Viện

```bash
pip install -r requirements.txt
```

#### 2. Cấu Hình Môi Trường

Tạo file `.env` từ `.env.example`:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
FLASK_ENV=development

# Database Configuration
DB_HOST=10.216.28.11
DB_PORT=3306
DB_USER=ovnm
DB_PASSWORD=P@ssw0rd
DB_NAME=db_hr

# Application Settings
APP_NAME=OKI VIETNAM HR
DEFAULT_LANGUAGE=vi
TIMEZONE=Asia/Ho_Chi_Minh
```

#### 3. Khởi Tạo Database

```bash
python init_db.py
```

Lệnh này sẽ tạo:
- Tất cả các bảng trong database
- Tài khoản admin: `ADMIN` / `admin123`
- Tài khoản mẫu: `EMP001` / `password123`

#### 4. Chạy Ứng Dụng

```bash
python app.py
```

Truy cập: http://localhost:5000

## Tài Khoản Mặc Định

Sau khi chạy `init_db.py`, bạn có thể đăng nhập với:

- **Admin**: 
  - Mã nhân viên: `ADMIN`
  - Mật khẩu: `admin123`
  
- **Nhân viên mẫu**:
  - Mã nhân viên: `EMP001`
  - Mật khẩu: `password123`

## Các Tính Năng Mới

### 1. Xác Thực Người Dùng
- Sử dụng Flask-Login để quản lý phiên
- Tất cả trang được bảo vệ bằng `@login_required`
- Truy cập thông tin user qua `current_user`

### 2. Quản Lý Database
- Models SQLAlchemy trong `models/__init__.py`
- Không còn dùng raw SQL queries
- Sử dụng `db.session.add()`, `db.session.commit()`

### 3. Form Validation
- WTForms với validation tích hợp
- Bảo mật CSRF tự động
- Các form class trong `forms.py`

### 4. Trang Quản Trị
- Truy cập tại `/admin`
- Quản lý users, overtime requests, meal registrations
- Chỉ admin mới truy cập được

## Cấu Trúc Database

### Bảng Users (Người dùng)
- Thông tin nhân viên
- Mật khẩu được mã hóa
- Phân quyền: 'user' hoặc 'admin'

### Bảng Overtime Requests (Yêu cầu tăng ca)
- Thông tin đăng ký tăng ca
- Trạng thái: 'pending', 'approved', 'rejected'
- Lưu người phê duyệt và thời gian

### Bảng Meal Registrations (Đăng ký suất ăn)
- Đăng ký suất ăn theo ngày
- Ghi chú bổ sung

## Triển Khai Lên Railway

1. Push code lên GitHub
2. Kết nối Railway với GitHub repo
3. Thêm biến môi trường trong Railway dashboard
4. Sau khi deploy, chạy: `python init_db.py`

## Xử Lý Lỗi

### Lỗi Kết Nối Database
- Kiểm tra MySQL server đang chạy
- Xác nhận thông tin trong file `.env`
- Đảm bảo database `db_hr` đã tồn tại

### Lỗi Import
- Chạy `pip install -r requirements.txt`
- Kích hoạt virtual environment

### Lỗi Migration
- Xóa thư mục `migrations` và khởi tạo lại
- Hoặc dùng `init_db.py` để tạo bảng trực tiếp

## Các Bước Tiếp Theo

1. ✅ Cập nhật app.py với Flask-Login và SQLAlchemy
2. ✅ Tạo models cho User, OvertimeRequest, MealRegistration
3. ✅ Tạo forms với WTForms
4. ✅ Thêm Flask-Admin panel
5. ⏳ Cập nhật templates để dùng WTForms
6. ⏳ Implement workflow phê duyệt tăng ca
7. ⏳ Thêm email notifications
8. ⏳ Implement chức năng quên mật khẩu

## Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. File `UPGRADE_GUIDE.md` (tiếng Anh)
2. Logs khi chạy ứng dụng
3. Cấu hình trong file `.env`
