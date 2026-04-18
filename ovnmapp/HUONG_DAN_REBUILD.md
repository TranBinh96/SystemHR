# HƯỚNG DẪN REBUILD APP ANDROID

## Tình trạng hiện tại
✅ File `qr-scanner.html` đã được tạo với **inline CSS** (không cần internet)
✅ WebView đã được cấu hình đúng trong `MainActivity.java`
✅ AndroidManifest.xml đã có đầy đủ permissions

## Lỗi bạn gặp
Lỗi `java.lang.ExceptionInInitializerError` và `JCEF is not supported` là lỗi của **Android Studio IDE**, KHÔNG PHẢI lỗi app. Bạn có thể bỏ qua.

## Các bước rebuild app trong Android Studio

### Bước 1: Clean Project
1. Mở Android Studio
2. Vào menu: **Build** → **Clean Project**
3. Đợi quá trình clean hoàn tất (xem progress bar ở dưới)

### Bước 2: Rebuild Project
1. Vào menu: **Build** → **Rebuild Project**
2. Đợi quá trình rebuild hoàn tất (có thể mất 1-2 phút)
3. Kiểm tra tab **Build** ở dưới để xem có lỗi không

### Bước 3: Sync Gradle (nếu cần)
1. Nếu thấy thông báo "Gradle files have changed", click **Sync Now**
2. Hoặc vào menu: **File** → **Sync Project with Gradle Files**

### Bước 4: Chạy app
1. Đảm bảo emulator đã chạy hoặc thiết bị thật đã kết nối
2. Click nút **Run** (▶️) màu xanh lá ở thanh toolbar
3. Hoặc vào menu: **Run** → **Run 'app'**
4. Chọn thiết bị để chạy

## Kiểm tra kết quả

App sẽ hiển thị:
- ✅ Sidebar menu bên trái với logo "The Culinary Concierge"
- ✅ Phần quét QR ở giữa với khung màu xanh lá (#27AE60)
- ✅ Thống kê: Tổng xuất ăn: 120, Cải thiện: 10, Thường: 200
- ✅ Thông tin bữa ăn "Cơm gà xối mỡ" bên phải
- ✅ Đã lấy: 8, Còn lại: 3 (hiển thị 2 lần: trong scanner và trong meal info)
- ✅ Tất cả nội dung bằng tiếng Việt
- ✅ Màu xanh lá chủ đạo

## Nếu vẫn thấy màn hình trắng

### Cách 1: Kiểm tra Logcat
1. Mở tab **Logcat** ở dưới Android Studio
2. Tìm các dòng lỗi màu đỏ
3. Gửi lỗi cho tôi để debug

### Cách 2: Xóa cache app
1. Trong emulator/thiết bị: Settings → Apps → Ovnmapp
2. Chọn **Storage** → **Clear Cache** và **Clear Data**
3. Chạy lại app

### Cách 3: Xóa build cache
1. Trong Android Studio: **File** → **Invalidate Caches**
2. Chọn **Invalidate and Restart**
3. Sau khi restart, rebuild lại

## Lưu ý quan trọng

⚠️ **App này chạy OFFLINE** - không cần internet
⚠️ File HTML sử dụng **inline CSS** - không có external dependencies
⚠️ Lỗi JCEF trong IDE không ảnh hưởng đến app

## Nếu cần hỗ trợ

Hãy gửi cho tôi:
1. Screenshot màn hình app (nếu có hiển thị gì)
2. Nội dung tab **Logcat** (filter theo package: bin.ovnmapp)
3. Thông báo lỗi trong tab **Build** (nếu có)
