# Hướng dẫn test Import User

## Bước 1: Khởi động server
```bash
python app.py
```

## Bước 2: Mở browser và login
1. Mở http://localhost:5000
2. Login với tài khoản admin
3. Vào trang Admin Users

## Bước 3: Mở Developer Console
1. Nhấn F12 để mở Developer Tools
2. Chuyển sang tab Console
3. Giữ console mở trong suốt quá trình test

## Bước 4: Test import
1. Click nút "Thêm người dùng" → "Import Excel"
2. Chọn file Excel (hoặc tải template trước)
3. **Kiểm tra console log:**
   - Phải thấy: `File stored: [filename] [size] bytes`
   - Nếu không thấy → File không được lưu đúng

4. Xem preview và click "Xác nhận import"
5. **Kiểm tra console log:**
   ```
   Import debug:
     - File: [filename] [size] bytes
     - CSRF token: [token]...
     - FormData entries: [["file", "[filename]"]]
   ```

6. **Kiểm tra server log (terminal):**
   ```
   === IMPORT REQUEST DEBUG ===
   Request method: POST
   Request content type: multipart/form-data; boundary=...
   Request files keys: ['file']
   File received: [filename]
   File validation passed, starting import...
   ```

## Các lỗi thường gặp

### Lỗi: "Không có file được tải lên"
**Console log:**
- Không thấy "File stored" → File không được lưu
- Không thấy file trong FormData entries → File không được thêm vào FormData

**Server log:**
- `Request files keys: []` → File không được gửi

**Giải pháp:**
- Kiểm tra file input có value không
- Kiểm tra importFileData có giá trị không
- Thử reload trang và test lại

### Lỗi: CSRF token not found
**Console log:**
- `CSRF token: NOT FOUND`

**Giải pháp:**
- Kiểm tra meta tag có trong HTML không: `<meta name="csrf-token" content="...">`
- Reload trang để generate token mới

### Lỗi: 400 Bad Request
**Server log:**
- Xem message cụ thể trong log
- Kiểm tra file có đúng format không (.xlsx, .xls)

## File Excel mẫu

Tạo file Excel với cấu trúc:

| Mã nhân viên | Họ và tên | Phòng ban | Mật khẩu | Quyền | Trạng thái | Phê duyệt | Đăng ký |
|--------------|-----------|-----------|----------|-------|------------|-----------|---------|
| NV001        | Nguyễn Văn A | IT     | 123456   | user  | working    | false     | false   |
| NV002        | Trần Thị B   | HR     | 123456   | user  | working    | true      | true    |

Hoặc tải template từ nút "Tải Template Excel".

## Kết quả mong đợi

**Thành công:**
- Console: Không có lỗi
- Server log: "File validation passed, starting import..."
- Notification: "Import thành công X user"
- Table refresh với user mới

**Thất bại:**
- Console: Error message chi tiết
- Server log: Error message
- Notification: Error message
