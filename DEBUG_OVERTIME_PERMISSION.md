# Debug: Overtime Permission Update Issue

## Vấn đề
User cập nhật "Quyền đăng ký overtime" và "Người phê duyệt overtime" thành công, nhưng khi mở lại form thì không hiển thị đúng giá trị đã chọn.

## Các bước debug

### 1. Kiểm tra Console Log (Browser)
Mở Developer Tools (F12) → Console tab, sau đó:

1. **Mở form edit user** → Xem log:
   ```
   === populateOvertimeApprovers called ===
   API response: {success: true, users: [...]}
   Found X approvers
   Setting overtime_approver_id to: 8
   Dropdown value after set: 8
   ```

2. **Click "Lưu thay đổi"** → Xem log:
   ```
   === Saving user data ===
   overtime_approver_id value: 8
   Full data: {employee_id: "10009", ..., overtime_approver_id: 8}
   ```

### 2. Kiểm tra Network Tab
1. Mở Developer Tools (F12) → Network tab
2. Click "Lưu thay đổi"
3. Tìm request `/admin/users/8/edit`
4. Xem **Request Payload**:
   ```json
   {
     "employee_id": "10009",
     "name": "Đỗ Mạnh thư",
     "can_register_overtime": true,
     "overtime_approver_id": 8,
     ...
   }
   ```
5. Xem **Response**:
   ```json
   {
     "success": true,
     "message": "Đã cập nhật thông tin Đỗ Mạnh thư"
   }
   ```

### 3. Kiểm tra Database
Chạy script để xem giá trị trong database:

```bash
python scripts/check_user_overtime_permission.py 10009
```

Kết quả mong đợi:
```
can_register_overtime: True
overtime_approver_id: 8
```

### 4. Các vấn đề có thể xảy ra

#### A. Dropdown không được populate
**Triệu chứng**: Console log không có "populateOvertimeApprovers called"

**Nguyên nhân**: Hàm không được gọi trong `openEditModal`

**Giải pháp**: Kiểm tra dòng này trong `openEditModal`:
```javascript
populateOvertimeApprovers(); // Load list of approvers
```

#### B. API không trả về dữ liệu
**Triệu chứng**: Console log có "No users found or API error"

**Nguyên nhân**: Route `/api/users?can_approve=1` không hoạt động

**Giải pháp**: 
1. Kiểm tra route có tồn tại trong `app.py`
2. Kiểm tra có user nào có `can_approve = True` không

#### C. Giá trị không được set vào dropdown
**Triệu chứng**: Console log có "Setting overtime_approver_id to: 8" nhưng "Dropdown value after set: " (empty)

**Nguyên nhân**: Dropdown chưa được populate khi set giá trị

**Giải pháp**: Tăng timeout trong `openEditModal`:
```javascript
setTimeout(() => {
    // Set values here
}, 200); // Tăng từ 100ms lên 200ms
```

#### D. Giá trị không được gửi lên server
**Triệu chứng**: Network tab không thấy `overtime_approver_id` trong request

**Nguyên nhân**: Field không được đọc đúng trong `saveUserEdit`

**Giải pháp**: Kiểm tra ID của dropdown:
```javascript
overtime_approver_id: document.getElementById('editOvertimeApproverId').value || null
```

#### E. Backend không lưu giá trị
**Triệu chứng**: Response success nhưng database không thay đổi

**Nguyên nhân**: Backend route không xử lý field này

**Giải pháp**: Kiểm tra route `/admin/users/<id>/edit` có đoạn:
```python
if 'overtime_approver_id' in data:
    approver_id = data['overtime_approver_id']
    if approver_id and approver_id != '' and approver_id != 'null':
        user.overtime_approver_id = int(approver_id)
    else:
        user.overtime_approver_id = None
```

### 5. Test Case

#### Test 1: Bật quyền đăng ký overtime
```bash
python scripts/enable_overtime_permission.py 10009
```

#### Test 2: Kiểm tra quyền
```bash
python scripts/check_user_overtime_permission.py 10009
```

#### Test 3: Update qua UI
1. Login as admin
2. Vào Admin → Users
3. Click "Sửa" user 10009
4. Chọn "Quyền đăng ký overtime" = "Có quyền đăng ký"
5. Chọn "Người phê duyệt overtime" = "Đỗ Mạnh thư (10009)"
6. Click "Lưu thay đổi"
7. Mở lại form → Kiểm tra giá trị có đúng không

## Kết quả mong đợi

Sau khi cập nhật thành công:
- ✅ `can_register_overtime = True`
- ✅ `overtime_approver_id = 8`
- ✅ Mở lại form → Dropdown hiển thị "Đỗ Mạnh thư (10009)"
- ✅ User 10009 có thể vào `/overtime` để đăng ký

## Lưu ý

- Nếu user chưa có `overtime_approver_id`, họ sẽ không thể đăng ký overtime (bị chặn ở route `/overtime`)
- Nếu user chưa có `can_register_overtime = True`, họ sẽ bị redirect về dashboard
- Console log đã được thêm vào để debug, có thể xóa sau khi fix xong
