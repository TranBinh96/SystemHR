# Các Bước Cài Đặt Chi Tiết

## ✅ Đã Hoàn Thành

### 1. Cài Đặt Thư Viện ✅
```bash
pip install -r requirements.txt
```
**Kết quả**: Tất cả thư viện đã được cài đặt thành công!

### 2. App Đã Chạy ✅
```bash
python app.py
```
**Kết quả**: Server đang chạy tại http://127.0.0.1:5000

## 🔄 Bước Tiếp Theo

### 3. Khởi Tạo Database

Mở terminal mới (giữ app đang chạy) và chạy:

```bash
python init_db.py
```

Lệnh này sẽ:
- Tạo tất cả bảng trong database
- Tạo tài khoản admin: `ADMIN` / `admin123`
- Tạo tài khoản user mẫu: `EMP001` / `password123`

### 4. Truy Cập Ứng Dụng

Mở trình duyệt và truy cập:
- **Trang chính**: http://127.0.0.1:5000
- **Admin panel**: http://127.0.0.1:5000/admin

### 5. Đăng Nhập

Sử dụng một trong các tài khoản:

**Admin:**
- Mã nhân viên: `ADMIN`
- Mật khẩu: `admin123`

**User:**
- Mã nhân viên: `EMP001`
- Mật khẩu: `password123`

## 📝 Lưu Ý

### Cảnh Báo Dependency
Có một số cảnh báo về dependency conflicts:
```
grpcio-status requires protobuf>=6.31.1, but you have protobuf 4.21.12
```

**Giải pháp**: Không cần lo lắng, các cảnh báo này không ảnh hưởng đến ứng dụng HR của chúng ta. Chúng liên quan đến các package khác (label-studio, grpcio) không được sử dụng trong project này.

### Nếu Gặp Lỗi Kết Nối Database

Kiểm tra:
1. MySQL server đang chạy
2. Thông tin kết nối trong `.env` đúng:
   ```
   DB_HOST=10.216.28.11
   DB_PORT=3306
   DB_USER=ovnm
   DB_PASSWORD=P@ssw0rd
   DB_NAME=db_hr
   ```
3. Database `db_hr` đã tồn tại

## 🧪 Chạy Tests (Tùy chọn)

Sau khi khởi tạo database, bạn có thể chạy tests:

```bash
python run_tests.py
```

Hoặc:

```bash
python -m pytest tests/
```

## 📊 Cấu Trúc Hoàn Chỉnh

```
SystemHR/
├── app.py                    # ✅ Main application
├── init_db.py               # ⏳ Chạy để tạo database
├── setup.py                 # ✅ Setup script
├── run_tests.py             # Tests runner
├── config.py                # ✅ Configuration
├── forms.py                 # ✅ WTForms
├── database.py              # Legacy (không dùng nữa)
├── models/
│   └── __init__.py         # ✅ SQLAlchemy models
├── controllers/
│   └── auth_controller.py  # Legacy (không dùng nữa)
├── templates/               # ✅ HTML templates
├── static/                  # ✅ Static files (PWA)
├── tests/                   # ✅ Test suite
├── docs/                    # ✅ Documentation
└── .env                     # ⏳ Cần tạo từ .env.example

```

## 🎯 Checklist

- [x] Cài đặt Python 3.11
- [x] Cài đặt dependencies
- [x] App chạy thành công
- [ ] Khởi tạo database (`python init_db.py`)
- [ ] Đăng nhập thành công
- [ ] Test các chức năng
- [ ] Chạy tests (tùy chọn)

## 🚀 Sẵn Sàng Deploy

Sau khi test thành công trên local, bạn có thể deploy lên Railway:

1. Push code lên GitHub
2. Kết nối Railway với repo
3. Thêm environment variables
4. Deploy tự động
5. Chạy `python init_db.py` trên Railway

## 💡 Tips

1. **Development**: Giữ app chạy với `python app.py`, mọi thay đổi code sẽ tự động reload
2. **Database**: Sử dụng Flask-Admin tại `/admin` để quản lý data
3. **Testing**: Chạy tests trước khi commit code
4. **PWA**: Trên mobile, chọn "Add to Home Screen" để cài app

---

**Trạng thái hiện tại**: App đang chạy, cần khởi tạo database!
