# Đơn giản hóa hệ thống quyền Overtime

## Vấn đề ban đầu
Hệ thống có **3 trường quyền** cho overtime:
1. `can_approve` - Quyền phê duyệt overtime
2. `can_register` - Quyền đăng ký suất ăn
3. `can_register_overtime` - Quyền đăng ký overtime ← **TRÙNG LẶP!**

**Vấn đề**: `can_register_overtime` là không cần thiết vì:
- Nếu user là manager (`can_approve=True`) → Tự phê duyệt
- Nếu user thường → Chỉ cần có `overtime_approver_id`

## Giải pháp: Xóa `can_register_overtime`

### Logic mới (đơn giản hơn):

```
┌─────────────────────────────────────────────────────────┐
│ User đăng ký overtime                                   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Kiểm tra can_approve  │
            └───────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌──────────────┐              ┌──────────────────┐
│ can_approve  │              │ !can_approve     │
│ = True       │              │ (User thường)    │
└──────────────┘              └──────────────────┘
        │                               │
        ▼                               ▼
┌──────────────┐              ┌──────────────────┐
│ TỰ PHÊ DUYỆT│              │ Kiểm tra         │
│ status =     │              │ overtime_        │
│ 'approved'   │              │ approver_id      │
└──────────────┘              └──────────────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        │                             │
                        ▼                             ▼
                ┌──────────────┐            ┌──────────────┐
                │ Có approver  │            │ Không có     │
                │              │            │ approver     │
                └──────────────┘            └──────────────┘
                        │                             │
                        ▼                             ▼
                ┌──────────────┐            ┌──────────────┐
                │ GỬI PHÊ DUYỆT│            │ LỖI: Chưa    │
                │ status =     │            │ chỉ định     │
                │ 'pending'    │            │ người duyệt  │
                └──────────────┘            └──────────────┘
```

## Thay đổi đã thực hiện

### 1. Database
**Xóa column**: `can_register_overtime`
```sql
ALTER TABLE users DROP COLUMN can_register_overtime;
```

### 2. Model (`models/__init__.py`)
**TRƯỚC**:
```python
can_approve = db.Column(db.Boolean, default=False)
can_register = db.Column(db.Boolean, default=True)
can_register_overtime = db.Column(db.Boolean, default=False)  # ← XÓA
overtime_approver_id = db.Column(db.Integer, ...)
```

**SAU**:
```python
can_approve = db.Column(db.Boolean, default=False)  # Manager
can_register = db.Column(db.Boolean, default=True)  # Suất ăn
overtime_approver_id = db.Column(db.Integer, ...)   # Người duyệt
```

### 3. Route `/overtime` (`app.py`)
**TRƯỚC**:
```python
if not current_user.can_register_overtime:
    flash('Bạn không có quyền đăng ký tăng ca')
    return redirect(url_for('dashboard'))

# Tất cả user đều gửi pending
overtime_request.status = 'pending'
overtime_request.manager_id = current_user.overtime_approver_id
```

**SAU**:
```python
if current_user.can_approve:
    # Manager: Tự phê duyệt
    status = 'approved'
    manager_id = current_user.id
    manager_comment = 'Tự phê duyệt (Manager)'
else:
    # User thường: Cần người phê duyệt
    if not current_user.overtime_approver_id:
        flash('Chưa có người phê duyệt')
        return redirect(url_for('overtime'))
    
    status = 'pending'
    manager_id = current_user.overtime_approver_id
```

### 4. Admin Form (`templates/admin_users.html`)
**Xóa trường**: "Quyền đăng ký overtime"

**TRƯỚC** (4 rows):
- Row 3: Quyền phê duyệt | Quyền đăng ký | Quyền (Role)
- Row 4: **Quyền đăng ký overtime** | Trạng thái
- Row 5: Người phê duyệt overtime

**SAU** (3 rows):
- Row 3: Quyền phê duyệt | Quyền đăng ký | Quyền (Role)
- Row 4: **Người phê duyệt overtime** | Trạng thái

### 5. JavaScript
Xóa tất cả tham chiếu đến `can_register_overtime`:
- `openEditModal()` - Bỏ tham số `canRegisterOvertime`
- `checkFormChanges()` - Bỏ tracking field này
- `saveUserEdit()` - Bỏ gửi field này

### 6. Backend Route `/admin/users/<id>/edit`
Xóa xử lý `can_register_overtime`

## Kết quả

### ✅ Lợi ích:
1. **Đơn giản hơn**: Chỉ 2 trường thay vì 3
2. **Logic rõ ràng**: Manager tự phê duyệt, user thường cần approver
3. **Ít lỗi hơn**: Không cần admin phải set thêm quyền
4. **Dễ hiểu hơn**: Không còn confusion về quyền nào làm gì

### 📊 So sánh:

| Trường | Trước | Sau | Ghi chú |
|--------|-------|-----|---------|
| `can_approve` | ✅ | ✅ | Manager có quyền phê duyệt |
| `can_register` | ✅ | ✅ | Quyền đăng ký suất ăn |
| `can_register_overtime` | ✅ | ❌ | **XÓA** - Không cần thiết |
| `overtime_approver_id` | ✅ | ✅ | Người phê duyệt cho user thường |

### 🎯 Use Cases:

**Case 1: Manager đăng ký overtime**
```
User: Đỗ Mạnh thư (can_approve=True)
→ Đăng ký overtime
→ Tự động approved
→ Không cần người phê duyệt
```

**Case 2: User thường đăng ký overtime**
```
User: Trần Thanh Binh (can_approve=False, overtime_approver_id=8)
→ Đăng ký overtime
→ Status = pending
→ Gửi đến user ID 8 (Đỗ Mạnh thư) để phê duyệt
```

**Case 3: User chưa có approver**
```
User: Nguyễn Văn A (can_approve=False, overtime_approver_id=NULL)
→ Đăng ký overtime
→ LỖI: "Chưa có người phê duyệt được chỉ định"
→ Admin cần set overtime_approver_id
```

## Migration

### Script đã chạy:
```bash
python scripts/remove_can_register_overtime_column.py
```

### Kết quả:
```
✅ Successfully removed column 'can_register_overtime'

New logic:
  - Manager (can_approve=True): Tự đăng ký và tự phê duyệt
  - User thường: Cần có overtime_approver_id để đăng ký
```

## Files đã sửa
1. `models/__init__.py` - Xóa column definition
2. `app.py` - Cập nhật route `/overtime` với logic mới
3. `templates/admin_users.html` - Xóa field "Quyền đăng ký overtime"
4. `scripts/remove_can_register_overtime_column.py` - Migration script

## Testing

### Test 1: Manager tự phê duyệt
```bash
1. Login as manager (can_approve=True)
2. Vào /overtime
3. Đăng ký overtime
4. Kiểm tra: status = 'approved', manager_id = current_user.id
```

### Test 2: User thường gửi phê duyệt
```bash
1. Login as user (can_approve=False, overtime_approver_id=8)
2. Vào /overtime
3. Đăng ký overtime
4. Kiểm tra: status = 'pending', manager_id = 8
```

### Test 3: User chưa có approver
```bash
1. Login as user (can_approve=False, overtime_approver_id=NULL)
2. Vào /overtime
3. Thấy lỗi: "Chưa có người phê duyệt được chỉ định"
```

## Kết luận
Hệ thống đã được đơn giản hóa thành công! Không còn field `can_register_overtime` trùng lặp. Logic rõ ràng hơn và dễ maintain hơn. 🎉
