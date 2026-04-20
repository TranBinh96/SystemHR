# Fix Import User từ Excel - Lỗi 400

## Vấn đề
Khi import user từ file Excel, hệ thống báo lỗi 400 (Bad Request) với message "Không có file được tải lên".

## Nguyên nhân chính
1. **CSRF Protection không được khởi tạo** - Flask-WTF không được import và khởi tạo
2. **CSRF Token không được gửi** - Request không chứa CSRF token
3. **File object bị mất** - File object không được giữ đúng cách sau khi đọc preview
4. **Error handling không đầy đủ** - Endpoint không trả về response khi exception
5. **Response handling không kiểm tra status** - JavaScript không xử lý lỗi HTTP đúng cách

## Các sửa chữa

### 1. app.py - Khởi tạo CSRF Protection
```python
# Thêm import
from flask_wtf.csrf import CSRFProtect

# Khởi tạo CSRF (sau khi khởi tạo app)
csrf = CSRFProtect(app)
```

### 2. app.py - Cải thiện endpoint import
```python
@app.route('/admin/users/import', methods=['POST', 'OPTIONS'])
@login_required
def import_users_excel():
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return '', 204
    
    # Thêm logging chi tiết
    print(f"\n=== IMPORT REQUEST DEBUG ===")
    print(f"Request method: {request.method}")
    print(f"Request content type: {request.content_type}")
    print(f"Request files keys: {list(request.files.keys())}")
    print(f"Request data: {request.data[:100] if request.data else 'No data'}")
    
    # ... rest of code
```

### 3. templates/admin_users.html - Thêm CSRF Token Meta Tag
```html
<!-- Thêm vào <head> -->
<meta name="csrf-token" content="{{ csrf_token() }}">
```

### 4. templates/admin_users.html - Sửa hàm handleImportFile()
```javascript
async function handleImportFile(input) {
    const file = input.files[0];
    if (!file) return;

    // Store file FIRST - before reading
    importFileData = file;
    console.log('File stored:', file.name, file.size, 'bytes');

    // Then read for preview...
}
```

### 5. templates/admin_users.html - Sửa hàm confirmImport()
```javascript
async function confirmImport() {
    // Get file from input element directly as backup
    const fileInput = document.getElementById('importFileInput');
    const fileToUpload = importFileData || (fileInput && fileInput.files[0]);
    
    if (!fileToUpload) {
        showNotification('Không tìm thấy file để import', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileToUpload);
    
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    
    // Add logging
    console.log('Import debug:');
    console.log('  - File:', fileToUpload.name, fileToUpload.size, 'bytes');
    console.log('  - CSRF token:', csrfToken ? csrfToken.substring(0, 20) + '...' : 'NOT FOUND');
    
    const response = await fetch('{{ url_for("import_users_excel") }}', {
        method: 'POST',
        body: formData,
        headers: csrfToken ? {'X-CSRFToken': csrfToken} : {}
    });
    
    // Check response and handle errors...
}
```

## Cách test
1. Mở trang Admin Users
2. Mở Developer Console (F12) để xem logs
3. Click "Import Excel"
4. Chọn file Excel
5. Xem preview và confirm
6. Kiểm tra console để xem:
   - File được lưu đúng (name, size)
   - CSRF token được gửi
   - FormData entries chứa file
   - Server response

## Debug checklist
Nếu vẫn gặp lỗi 400, kiểm tra:
- [ ] Console log có hiển thị file name và size không?
- [ ] CSRF token có được tìm thấy không?
- [ ] FormData entries có chứa file không?
- [ ] Server log có hiển thị "Request files keys" không?
- [ ] Server log có hiển thị file name không?

## Lưu ý
- CSRF token được tự động generate bởi Flask-WTF
- File object phải được lưu TRƯỚC khi đọc với FileReader
- FormData tự động set Content-Type header
- Không cần thêm csrf_token vào FormData (chỉ cần header)

## Files thay đổi
- ✅ `app.py` - Khởi tạo CSRF, cải thiện error handling, thêm OPTIONS method
- ✅ `templates/admin_users.html` - Thêm CSRF token, sửa handleImportFile(), sửa confirmImport()
