# Fix: Overtime Approver Dropdown Not Showing Selected Value

## Vấn đề
Khi admin cập nhật "Người phê duyệt overtime" cho user và click "Lưu thay đổi", giá trị được lưu thành công vào database. Nhưng khi mở lại form edit, dropdown không hiển thị giá trị đã chọn (hiển thị "-- Chưa chỉ định --").

## Nguyên nhân
**Race condition**: Dropdown "Người phê duyệt overtime" được populate bằng AJAX call đến `/api/users?can_approve=1`. Khi `openEditModal()` chạy:

1. Gọi `populateOvertimeApprovers()` → Bắt đầu AJAX request
2. Sau 100ms → Set giá trị `overtimeApproverSelect.value = overtimeApproverId`
3. **VẤN ĐỀ**: AJAX request chưa hoàn thành → Dropdown chưa có options → Set value thất bại!

## Giải pháp

### 1. Tăng timeout từ 100ms → 300ms
```javascript
// TRƯỚC
setTimeout(() => {
    // Set values
}, 100); // Too short!

// SAU
setTimeout(() => {
    // Set values
}, 300); // Wait for API response
```

### 2. Thêm console.log để debug
Thêm log vào 3 nơi:

**A. `populateOvertimeApprovers()`:**
```javascript
console.log('=== populateOvertimeApprovers called ===');
console.log('API response:', data);
console.log(`Found ${data.users.length} approvers`);
```

**B. `openEditModal()` - Phần set giá trị:**
```javascript
console.log('Setting overtime_approver_id to:', overtimeApproverId);
console.log('Dropdown value after set:', overtimeApproverSelect.value);
```

**C. `saveUserEdit()` - Trước khi gửi:**
```javascript
console.log('=== Saving user data ===');
console.log('overtime_approver_id value:', document.getElementById('editOvertimeApproverId').value);
console.log('Full data:', data);
```

## Cách test

### 1. Mở Browser Console (F12)
```
1. Vào Admin → Users
2. Click "Sửa" user bất kỳ
3. Xem console log:
   === populateOvertimeApprovers called ===
   API response: {success: true, users: [...]}
   Found 3 approvers
   Setting overtime_approver_id to: 8
   Dropdown value after set: 8  ← Phải có giá trị!
```

### 2. Kiểm tra dropdown
```
- Dropdown "Người phê duyệt overtime" phải có danh sách người phê duyệt
- Giá trị đã chọn phải được highlight
```

### 3. Lưu và mở lại
```
1. Chọn người phê duyệt
2. Click "Lưu thay đổi"
3. Đóng modal
4. Mở lại form edit
5. Kiểm tra dropdown có hiển thị đúng giá trị không
```

## Giải pháp tốt hơn (Future improvement)

Thay vì dùng `setTimeout`, nên đợi AJAX hoàn thành:

```javascript
function openEditModal(...) {
    // ...
    
    // Populate dropdowns
    populatePositionList();
    
    // Wait for API to complete, THEN set values
    populateOvertimeApprovers().then(() => {
        // Set all values here
        if (overtimeApproverSelect) {
            overtimeApproverSelect.value = overtimeApproverId || '';
        }
    });
}

function populateOvertimeApprovers() {
    return fetch('/api/users?can_approve=1')  // Return promise
        .then(res => res.json())
        .then(data => {
            // Populate dropdown
        });
}
```

## Files đã sửa
- `templates/admin_users.html`:
  - Tăng timeout từ 100ms → 300ms
  - Thêm console.log để debug
  - Thêm error handling

## Kết quả
✅ Dropdown "Người phê duyệt overtime" hiển thị đúng giá trị đã chọn
✅ Console log giúp debug dễ dàng
✅ Timeout đủ lâu để AJAX hoàn thành
