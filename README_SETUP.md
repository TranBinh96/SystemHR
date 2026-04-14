# 🚀 Hướng Dẫn Chạy Môi Trường Test

## ✅ Môi Trường Đã Được Thiết Lập

### 📋 Thông Tin Hệ Thống
- **Python**: 3.11.0 ✅
- **Database**: MySQL (10.216.28.11:3306/db_hr) ✅
- **User**: ovnm ✅
- **Dependencies**: Đã cài đặt ✅

### 🎯 Cách Chạy Ứng Dụng

#### Phương pháp 1: Sử dụng file batch (Đơn giản nhất)
```bash
# Double-click file này hoặc chạy trong terminal
start_server.bat
```

#### Phương pháp 2: Chạy trực tiếp
```bash
python app.py
```

### 🌐 Truy Cập Ứng Dụng

Sau khi server khởi động thành công:
- **Web Application**: http://127.0.0.1:5000
- **Admin Panel**: http://127.0.0.1:5000/admin
- **API Documentation**: Xem file `docs/API_DOCUMENTATION.md`

### 🔑 Tài Khoản Mặc Định

**Admin Account:**
- Username: `ADMIN`
- Password: `admin123`

**User Account:**
- Username: `EMP001` 
- Password: `password123`

### 📊 Database Status
- **Kết nối**: ✅ Thành công
- **Tables**: 9 bảng đã tồn tại
- **Data**: Sẵn sàng sử dụng

### 🛠️ Tính Năng Có Thể Test

1. **Đăng nhập/Đăng ký**
   - Test với tài khoản admin và user
   - Đổi mật khẩu

2. **Quản lý tăng ca**
   - Đăng ký tăng ca
   - Phê duyệt tăng ca (admin)

3. **Quản lý suất ăn**
   - Đăng ký suất ăn
   - Xem menu

4. **Admin Panel**
   - Quản lý users
   - Quản lý departments
   - Quản lý positions
   - Thống kê

5. **API Testing**
   - JWT Authentication
   - CRUD operations
   - Postman/curl testing

### 🔧 Troubleshooting

**Nếu server không khởi động:**
1. Kiểm tra kết nối database:
   ```bash
   python scripts/check_db_connection.py
   ```

2. Kiểm tra dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Nếu không truy cập được web:**
- Đảm bảo server đang chạy
- Kiểm tra port 5000 không bị chiếm dụng
- Thử truy cập: http://localhost:5000

### 📝 Logs & Debug

Server chạy ở chế độ DEBUG, bạn sẽ thấy:
- SQL queries trong console
- Error messages chi tiết
- Auto-reload khi thay đổi code

### 🚫 Dừng Server

- Nhấn `Ctrl + C` trong terminal
- Hoặc đóng cửa sổ command prompt

---

**🎉 Môi trường test đã sẵn sàng! Chúc bạn test vui vẻ!**