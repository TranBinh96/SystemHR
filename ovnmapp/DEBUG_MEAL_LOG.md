# HƯỚNG DẪN DEBUG TRANG NHẬT KÝ BỮA ĂN

## ✅ Đã cập nhật

Tôi đã thêm **debug logging chi tiết** vào trang meal-log.html để tìm nguyên nhân lỗi "Failed to fetch".

## 🔍 Cách kiểm tra lỗi

### Bước 1: Rebuild app

```
1. Build → Clean Project
2. Build → Rebuild Project
3. Run ▶️
```

### Bước 2: Mở Logcat trong Android Studio

1. Click tab **Logcat** ở dưới màn hình
2. Trong ô filter, gõ: `WebView`
3. Hoặc filter theo package: `bin.ovnmapp`

### Bước 3: Chạy app và xem logs

1. Mở app
2. Click vào "Nhật ký bữa ăn"
3. Xem các dòng log trong Logcat:

```
Starting to load meal log data...
API URL: https://ovnm.up.railway.app/admin/meal-registrations/list
XHR request sent
ReadyState: 1 Status: 0
ReadyState: 2 Status: 200
ReadyState: 3 Status: 200
ReadyState: 4 Status: 200
XHR onload - Status: 200
Response: {"registrations":[...
Parsed data: {...}
Found 18 registrations
```

### Bước 4: Phân tích lỗi

#### Nếu thấy "Network error - XHR failed":
- **Nguyên nhân**: Không có kết nối internet hoặc bị chặn
- **Giải pháp**: 
  - Kiểm tra emulator có internet không (mở Chrome trong emulator)
  - Kiểm tra firewall/antivirus
  - Thử restart emulator

#### Nếu thấy "HTTP error: 0":
- **Nguyên nhân**: CORS policy hoặc SSL certificate issue
- **Giải pháp**: API server cần cấu hình CORS headers

#### Nếu thấy "HTTP error: 403/404/500":
- **Nguyên nhân**: API endpoint không đúng hoặc server lỗi
- **Giải pháp**: Kiểm tra API URL

#### Nếu thấy "Parse error":
- **Nguyên nhân**: Response không phải JSON hợp lệ
- **Giải pháp**: Kiểm tra response format

## 🧪 Test kết nối internet trong emulator

### Cách 1: Mở Chrome trong emulator
1. Mở Chrome browser trong emulator
2. Truy cập: https://ovnm.up.railway.app/admin/meal-registrations/list
3. Xem có hiển thị JSON không

### Cách 2: Ping từ terminal
```bash
adb shell ping -c 4 ovnm.up.railway.app
```

### Cách 3: Test với curl
```bash
curl https://ovnm.up.railway.app/admin/meal-registrations/list
```

## 🔧 Các giải pháp thay thế

### Giải pháp 1: Sử dụng dữ liệu mẫu (offline)

Nếu không thể kết nối API, tôi có thể tạo phiên bản với dữ liệu mẫu hardcoded để test giao diện.

### Giải pháp 2: Tạo proxy backend

Tạo một backend proxy trong Java/Kotlin để fetch dữ liệu thay vì fetch trực tiếp từ WebView.

### Giải pháp 3: Cấu hình CORS trên server

Thêm headers vào API response:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## 📱 Tính năng mới đã thêm

1. **Debug logging chi tiết**
   - Log mọi bước của XHR request
   - Log status code và response
   - Log errors với thông tin chi tiết

2. **Error messages cải thiện**
   - Hiển thị icon và message rõ ràng
   - Nút "Thử lại" để reload
   - Gợi ý cách khắc phục

3. **Timeout tăng lên**
   - Từ 10s → 15s
   - Tránh timeout khi mạng chậm

## 📋 Checklist debug

- [ ] Rebuild app thành công
- [ ] Mở Logcat và filter "WebView"
- [ ] Click "Nhật ký bữa ăn" trong app
- [ ] Xem logs trong Logcat
- [ ] Chụp screenshot logs và gửi cho tôi
- [ ] Test internet trong emulator (mở Chrome)
- [ ] Thử truy cập API URL trực tiếp trong browser

## 🆘 Gửi thông tin cho tôi

Nếu vẫn lỗi, hãy gửi cho tôi:

1. **Screenshot Logcat** (filter: WebView hoặc bin.ovnmapp)
2. **Screenshot màn hình lỗi** trong app
3. **Kết quả test** khi mở API URL trong Chrome emulator
4. **Thông tin emulator**: Android version, có internet không

## 💡 Lưu ý

- Trang này **BẮT BUỘC** phải có internet
- API phải cho phép CORS từ WebView
- SSL certificate phải hợp lệ
- Nếu không thể fix, tôi sẽ tạo phiên bản offline với dữ liệu mẫu
