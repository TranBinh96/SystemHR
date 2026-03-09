# Documentation - OKI Vietnam HR System

## 📚 Tài Liệu Hệ Thống

Thư mục này chứa tất cả tài liệu liên quan đến hệ thống HR OKI Vietnam.

## 📖 Danh Sách Tài Liệu

### 🚀 Quick Start
- **[QUICKSTART.md](QUICKSTART.md)** - Hướng dẫn bắt đầu nhanh (3 bước)
  - Cài đặt nhanh
  - Tài khoản mặc định
  - Các tính năng có sẵn

### 🇻🇳 Tiếng Việt
- **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)** - Hướng dẫn cài đặt chi tiết
  - Các bước cài đặt
  - Cấu hình môi trường
  - Xử lý lỗi
  - Triển khai lên Railway

### 🇬🇧 English
- **[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)** - Complete upgrade guide
  - Flask extensions overview
  - Installation steps
  - Database schema
  - Troubleshooting
  - Next steps

### 📱 Progressive Web App
- **[PWA_SETUP.md](PWA_SETUP.md)** - PWA configuration guide
  - Manifest configuration
  - Service worker setup
  - Install prompt
  - Offline functionality

### 📝 Changelog
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
  - Version 2.0.0 - Flask Extensions Upgrade
  - Completed features
  - Migration guide
  - Statistics

## 🗂️ Cấu Trúc Tài Liệu

```
docs/
├── README.md                  # This file
├── QUICKSTART.md             # Quick start guide
├── HUONG_DAN_CAI_DAT.md      # Vietnamese installation guide
├── UPGRADE_GUIDE.md          # English upgrade guide
├── PWA_SETUP.md              # PWA setup guide
└── CHANGELOG.md              # Version history
```

## 🎯 Chọn Tài Liệu Phù Hợp

### Bạn là người mới?
👉 Bắt đầu với **[QUICKSTART.md](QUICKSTART.md)**

### Cần hướng dẫn chi tiết bằng tiếng Việt?
👉 Đọc **[HUONG_DAN_CAI_DAT.md](HUONG_DAN_CAI_DAT.md)**

### Need English documentation?
👉 Read **[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)**

### Muốn cài đặt PWA?
👉 Xem **[PWA_SETUP.md](PWA_SETUP.md)**

### Muốn biết có gì mới?
👉 Kiểm tra **[CHANGELOG.md](CHANGELOG.md)**

## 📋 Nội Dung Chính

### Cài Đặt
Tất cả tài liệu đều có hướng dẫn cài đặt:
1. Cài đặt dependencies
2. Cấu hình database
3. Khởi tạo database
4. Chạy ứng dụng

### Tính Năng
- ✅ User Authentication (Flask-Login)
- ✅ Database ORM (SQLAlchemy)
- ✅ Admin Panel (Flask-Admin)
- ✅ Form Validation (WTForms)
- ✅ Database Migration (Flask-Migrate)
- ✅ Progressive Web App (PWA)
- ✅ Multi-language Support (VI/EN/JA)

### Database Schema
- **Users**: Employee information
- **OvertimeRequests**: Overtime management
- **MealRegistrations**: Meal registration

### Deployment
- Local development
- Railway deployment
- Environment configuration

## 🔧 Technical Stack

- **Backend**: Flask 3.0.0
- **Database**: MySQL 8.x
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: WTForms
- **Admin**: Flask-Admin
- **Frontend**: HTML, CSS, JavaScript
- **PWA**: Service Worker, Manifest

## 📞 Hỗ Trợ

### Gặp vấn đề?
1. Kiểm tra phần Troubleshooting trong tài liệu
2. Xem CHANGELOG.md để biết các thay đổi gần đây
3. Kiểm tra logs khi chạy ứng dụng

### Cần thêm tính năng?
Xem phần "Next Steps" trong UPGRADE_GUIDE.md hoặc CHANGELOG.md

## 🔄 Cập Nhật Tài Liệu

Khi thêm tính năng mới:
1. Cập nhật CHANGELOG.md
2. Thêm hướng dẫn vào tài liệu phù hợp
3. Cập nhật README.md này nếu cần

## 📊 Version Information

- **Current Version**: 2.0.0
- **Last Updated**: 2026-03-04
- **Status**: ✅ Production Ready

## 🌐 Links

- GitHub Repository: [Your Repo URL]
- Railway Deployment: [Your Railway URL]
- Admin Panel: http://localhost:5000/admin

## 📝 License

[Your License Information]

---

**Lưu ý**: Tất cả tài liệu được viết song ngữ Việt-Anh để phục vụ đa dạng người dùng.
