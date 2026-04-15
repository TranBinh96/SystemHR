# Admin Users - Overtime Permissions Update

## Vấn đề ban đầu
Trong form "Thông tin nhân viên" có **trùng lặp trường "Quyền"**:
- Row 3: "Quyền phê duyệt", "Quyền đăng ký", **"Quyền"** (Role: User/Admin)
- Row 4: **"Quyền"** (Role: User/Admin - TRÙNG), "Trạng thái"
- Cả 2 trường "Quyền" đều có **cùng ID "editRole"** → Lỗi HTML
- Thiếu trường **"Quyền đăng ký overtime"** và **"Người phê duyệt overtime"**

## Giải pháp đã thực hiện

### 1. Frontend - Form Edit User (`templates/admin_users.html`)

#### A. Cấu trúc form mới:
- **Row 3**: "Quyền phê duyệt" | "Quyền đăng ký" | "Quyền" (Role)
- **Row 4**: "Quyền đăng ký overtime" | "Trạng thái"
- **Row 5**: "Người phê duyệt overtime" (dropdown, full width)

#### B. Các trường đã thêm:
```html
<!-- Row 4 -->
<select id="editCanRegisterOvertime">
    <option value="1">Có quyền đăng ký</option>
    <option value="0">Không có quyền đăng ký</option>
</select>

<!-- Row 5 -->
<select id="editOvertimeApproverId">
    <option value="">-- Chưa chỉ định --</option>
    <!-- Populated by JavaScript -->
</select>
```

#### C. JavaScript Functions Updated:

**1. `openEditModal()` - Cập nhật signature:**
```javascript
function openEditModal(userId, employeeId, name, department, position, role, 
                      isActive, avatarUrl, canApprove, canRegister, workStatus, 
                      canRegisterOvertime, overtimeApproverId)
```

**2. `populateOvertimeApprovers()` - Hàm mới:**
```javascript
function populateOvertimeApprovers() {
    fetch('/api/users?can_approve=1')
        .then(res => res.json())
        .then(data => {
            // Populate dropdown with users who have can_approve = True
        });
}
```

**3. `checkFormChanges()` - Thêm tracking 2 trường mới:**
```javascript
canRegisterOvertime: document.getElementById('editCanRegisterOvertime').value,
overtimeApproverId: document.getElementById('editOvertimeApproverId').value,
```

**4. `saveUserEdit()` - Gửi 2 trường mới:**
```javascript
// FormData
formData.append('can_register_overtime', ...);
formData.append('overtime_approver_id', ...);

// JSON
data.can_register_overtime = ...;
data.overtime_approver_id = ...;
```

**5. Nơi gọi `openEditModal()` - Thêm 2 tham số:**
```html
onclick="openEditModal(..., {{ user.can_register_overtime|int }}, {{ user.overtime_approver_id or 'null' }})"
```

### 2. Backend - API Routes (`app.py`)

#### A. Route `/admin/users/<id>/edit` - Cập nhật:
```python
# Handle permission fields
if 'can_register_overtime' in data:
    user.can_register_overtime = data['can_register_overtime'] in ['true', 'True', True, 1, '1']

if 'overtime_approver_id' in data:
    approver_id = data['overtime_approver_id']
    if approver_id and approver_id != '' and approver_id != 'null':
        user.overtime_approver_id = int(approver_id)
    else:
        user.overtime_approver_id = None
```

#### B. Route `/api/users` - MỚI:
```python
@app.route('/api/users', methods=['GET'])
@login_required
def api_get_users():
    """API to get users list with filters"""
    can_approve = request.args.get('can_approve')
    
    query = User.query.filter_by(is_active=True)
    if can_approve == '1':
        query = query.filter_by(can_approve=True)
    
    users = query.order_by(User.name).all()
    
    return {
        'success': True,
        'users': [{
            'id': u.id,
            'employee_id': u.employee_id,
            'name': u.name,
            'department': u.dept.name if u.dept else '',
            'can_approve': u.can_approve
        } for u in users]
    }
```

## Luồng hoạt động

### Khi Admin mở form edit user:
1. Click nút "Sửa" → gọi `openEditModal()` với đầy đủ tham số
2. `openEditModal()` gọi `populateOvertimeApprovers()` để load danh sách approvers
3. `populateOvertimeApprovers()` gọi API `/api/users?can_approve=1`
4. API trả về danh sách users có `can_approve = True`
5. Dropdown "Người phê duyệt overtime" được populate
6. Form hiển thị với giá trị hiện tại của user

### Khi Admin lưu thay đổi:
1. Click "Lưu thay đổi" → gọi `saveUserEdit()`
2. `saveUserEdit()` gửi dữ liệu (FormData hoặc JSON) lên server
3. Route `/admin/users/<id>/edit` nhận và xử lý:
   - Cập nhật `can_register_overtime`
   - Cập nhật `overtime_approver_id`
4. Database được cập nhật
5. Page reload để hiển thị dữ liệu mới

## Các trường quyền trong User model

Sau khi cập nhật, User model có **4 trường quyền**:

1. **`role`** (String) - Vai trò: "user" hoặc "admin"
2. **`can_approve`** (Boolean) - Quyền phê duyệt overtime (người quản lý)
3. **`can_register`** (Boolean) - Quyền đăng ký suất ăn
4. **`can_register_overtime`** (Boolean) - Quyền đăng ký overtime

Và **1 trường quan hệ**:
5. **`overtime_approver_id`** (Integer, FK) - ID của người phê duyệt overtime

## Kết quả

✅ Xóa trường "Quyền" trùng lặp ở Row 4
✅ Thêm trường "Quyền đăng ký overtime"
✅ Thêm trường "Người phê duyệt overtime" với dropdown động
✅ Cập nhật JavaScript để load và lưu 2 trường mới
✅ Tạo API `/api/users?can_approve=1` để load danh sách approvers
✅ Cập nhật backend route để lưu 2 trường mới vào database

## Files đã sửa
- `templates/admin_users.html` - Form UI và JavaScript
- `app.py` - Backend routes (edit user + API users)

## Testing checklist
- [ ] Mở form edit user → kiểm tra hiển thị đúng 4 trường quyền
- [ ] Dropdown "Người phê duyệt overtime" load đúng danh sách
- [ ] Thay đổi "Quyền đăng ký overtime" → lưu thành công
- [ ] Chọn "Người phê duyệt overtime" → lưu thành công
- [ ] Kiểm tra database: `can_register_overtime` và `overtime_approver_id` được cập nhật
- [ ] User đăng ký overtime → request được gửi đến đúng approver
