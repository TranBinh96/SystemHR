# OKI VIETNAM HR System

Hệ thống quản lý nhân sự, tăng ca và suất ăn cho OKI VIETNAM

## Tính năng

- ✅ Đăng nhập / Đăng ký / Quên mật khẩu
- ✅ Dashboard với thống kê
- ✅ Đăng ký tăng ca
- ✅ Đăng ký suất ăn
- ✅ Đa ngôn ngữ (Tiếng Việt, English, 日本語)
- ✅ Dark mode support
- ✅ Responsive design (Mobile + Desktop)

## Công nghệ

- **Backend**: Flask (Python)
- **Frontend**: Tailwind CSS
- **Icons**: Material Symbols
- **Translations**: INI file format

## Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app.py
```

Server sẽ chạy tại: http://127.0.0.1:5000

## Tài khoản demo

- **Admin**: ADMIN / admin123 (Quản trị hệ thống)
- **User 1**: EMP001 / password123
- **User 2**: EMP002 / password456

## Cấu trúc dự án

```
SystemHR/
├── app.py                      # Main Flask application
├── translations.ini            # Đa ngôn ngữ
├── translations.py             # Translation loader
├── requirements.txt            # Python dependencies
├── models/
│   └── user.py                # User model
├── controllers/
│   └── auth_controller.py     # Authentication controller
└── templates/
    ├── login.html             # Trang đăng nhập
    ├── register.html          # Trang đăng ký
    ├── forgot_password.html   # Quên mật khẩu
    ├── dashboard.html         # Dashboard (Desktop + Mobile)
    ├── overtime.html          # Đăng ký tăng ca (Desktop + Mobile)
    └── meals.html             # Đăng ký suất ăn (Desktop + Mobile)
```

## Giao diện

### Mobile
- Bottom navigation bar
- Touch-optimized UI
- Swipeable calendars

### Desktop
- Sidebar navigation
- Stats cards
- Grid layouts
- Hover effects

## Ngôn ngữ

Thay đổi ngôn ngữ qua dropdown ở header:
- 🇻🇳 Tiếng Việt (mặc định)
- 🇬🇧 English
- 🇯🇵 日本語

## License

© 2024 OKI VIETNAM Co., Ltd.
