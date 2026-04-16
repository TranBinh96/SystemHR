# The Culinary Concierge - QR Scanner App

Ứng dụng Android hiển thị giao diện quét mã QR cho hệ thống quản lý bữa ăn.

## Tính năng

- ✅ Giao diện quét QR với màu cam
- ✅ Hiển thị thông tin bữa ăn
- ✅ Hiển thị thông tin nhân viên
- ✅ Responsive design cho tablet
- ✅ Hiệu ứng animation quét QR

## Cấu trúc dự án

```
app/
├── src/main/
│   ├── assets/
│   │   └── qr-scanner.html          # Giao diện HTML
│   ├── java/bin/ovnmapp/
│   │   └── MainActivity.java        # Activity chính
│   ├── res/
│   │   ├── layout/
│   │   │   └── activity_main.xml    # Layout với WebView
│   │   └── values/
│   │       └── strings.xml          # Tên ứng dụng
│   └── AndroidManifest.xml          # Cấu hình app
```

## Yêu cầu

- Android Studio Arctic Fox trở lên
- Android SDK 24+ (Android 7.0)
- Target SDK 36
- Java 11

## Cách chạy

### 1. Mở dự án trong Android Studio
```bash
# Mở Android Studio và chọn "Open an Existing Project"
# Chọn thư mục ovnmapp
```

### 2. Sync Gradle
- Android Studio sẽ tự động sync Gradle
- Hoặc click vào "Sync Project with Gradle Files"

### 3. Chạy ứng dụng
- Kết nối thiết bị Android hoặc khởi động emulator
- Click nút "Run" (▶️) hoặc nhấn Shift+F10
- Chọn thiết bị và chờ ứng dụng cài đặt

### 4. Build APK
```bash
# Trong terminal của Android Studio
./gradlew assembleDebug

# APK sẽ được tạo tại:
# app/build/outputs/apk/debug/app-debug.apk
```

## Cấu hình quan trọng

### AndroidManifest.xml
- ✅ Quyền INTERNET để load CDN (Tailwind, Google Fonts)
- ✅ Quyền ACCESS_NETWORK_STATE
- ✅ usesCleartextTraffic="true" để load HTTP content
- ✅ screenOrientation="landscape" cho tablet

### MainActivity.java
- ✅ JavaScript enabled
- ✅ DOM Storage enabled
- ✅ Wide viewport support
- ✅ Back button navigation

## Giao diện

Giao diện được thiết kế với:
- **Tailwind CSS** - Framework CSS
- **Google Fonts** - Plus Jakarta Sans
- **Material Symbols** - Icons
- **Màu chủ đạo**: Cam (#ff8c00)

## Tính năng WebView

- Load file HTML từ assets
- Hỗ trợ JavaScript
- Responsive cho nhiều kích thước màn hình
- Animation CSS mượt mà
- Back button navigation

## Troubleshooting

### Lỗi: "Cleartext HTTP traffic not permitted"
✅ Đã fix: Thêm `android:usesCleartextTraffic="true"` trong manifest

### Lỗi: "Web page not available"
✅ Đã fix: Thêm quyền INTERNET trong manifest

### Lỗi: Giao diện không hiển thị đúng
✅ Đã fix: Enable JavaScript và DOM Storage trong WebView

### Lỗi: Font không load
✅ Đã fix: Cho phép truy cập internet để load Google Fonts

## Phát triển tiếp

Để thêm tính năng quét QR thật:
1. Thêm thư viện ZXing hoặc ML Kit
2. Tạo CameraX activity
3. Kết nối với backend API
4. Xử lý dữ liệu QR code

## License

Copyright © 2026 The Culinary Concierge
