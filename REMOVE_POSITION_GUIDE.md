# Hướng dẫn xóa trường Chức vụ (Position)

## Tổng quan

Hệ thống đã được cập nhật để loại bỏ hoàn toàn trường chức vụ (position). Thay vào đó, hệ thống sử dụng quyền `can_approve` để xác định ai có thể phê duyệt overtime.

## Các thay đổi đã thực hiện

### 1. Models (models/__init__.py)
- ✅ Xóa class `Position`
- ✅ Xóa class `ApprovalHierarchy` 
- ✅ Xóa cột `position_id` trong User model
- ✅ Xóa relationship `pos` trong User model
- ✅ Xóa cột `position` trong OvertimeRequest, LeaveRequest, ExitEntryRequest

### 2. Routes (app.py)
- ✅ Xóa tất cả routes liên quan đến position management:
  - `/admin/positions`
  - `/admin/positions/list`
  - `/admin/positions/add`
  - `/admin/positions/edit`
  - `/admin/positions/delete`
  - `/admin/positions/employee-counts`
- ✅ Cập nhật route `/admin/users` - không còn truyền positions
- ✅ Cập nhật route `/admin/users/list` - không còn trả về position_id, position_name
- ✅ Cập nhật route `/admin/users/add` - không còn yêu cầu position
- ✅ Cập nhật route `/admin/users/edit` - không còn xử lý position
- ✅ Xóa code khởi tạo positions mặc định trong `init_database()`

### 3. Migration Script
- ✅ Tạo script `scripts/remove_position_tables.py` để xóa tables và columns trong database

## Cách chạy Migration

### Bước 1: Backup Database
```bash
# Backup database trước khi chạy migration
mysqldump -u ovnm -p db_hr > backup_before_remove_position.sql
```

### Bước 2: Chạy Migration Script

#### Cách 1: Chạy SQL Script (Khuyến nghị)
```bash
# Chạy trực tiếp SQL script
mysql -u ovnm -p db_hr < scripts/remove_position_tables.sql
```

Script sẽ tự động:
- Xóa foreign key constraints
- Xóa các columns position
- Xóa các tables positions và approval_hierarchy
- Hiển thị kết quả verification

#### Cách 2: Chạy Python Script
```bash
# Kích hoạt virtual environment
.venv\Scripts\activate  # Windows
# hoặc
source .venv/bin/activate  # Linux/Mac

# Chạy migration script
python scripts/remove_position_tables.py
```

Script sẽ hỏi xác nhận trước khi thực hiện. Nhập `yes` để tiếp tục.

### Bước 3: Kiểm tra kết quả
Migration script sẽ:
1. Xóa cột `position_id` từ bảng `users`
2. Xóa cột `position` từ các bảng `overtime_requests`, `leave_requests`, `exit_entry_requests`
3. Xóa bảng `approval_hierarchy`
4. Xóa bảng `positions`

### Bước 4: Khởi động lại ứng dụng
```bash
# Khởi động lại Flask app
python app.py
```

## Hệ thống phê duyệt mới

Sau khi xóa position, hệ thống phê duyệt hoạt động như sau:

### Quyền phê duyệt
- Người dùng có `can_approve = True` có thể phê duyệt overtime
- Người phê duyệt phải cùng phòng ban với người đăng ký

### Cách cấp quyền phê duyệt
1. Vào trang Admin Users (`/admin/users`)
2. Chỉnh sửa user
3. Bật checkbox "Quyền phê duyệt" (can_approve)

### User Model - Các phương thức liên quan
```python
user.can_approve          # Boolean - có quyền phê duyệt không
user.is_manager()         # Kiểm tra xem có phải manager không
user.get_approvers()      # Lấy danh sách người có thể phê duyệt cho user này
user.can_approve_for(u)   # Kiểm tra có thể phê duyệt cho user u không
user.get_subordinates()   # Lấy danh sách nhân viên có thể phê duyệt
```

## Cập nhật Frontend (nếu cần)

Nếu bạn có template HTML sử dụng position, cần cập nhật:

### Cần xóa/cập nhật:
- Form thêm/sửa user: xóa dropdown chọn position
- Bảng danh sách user: xóa cột position
- Trang quản lý positions: xóa hoàn toàn

### Thay thế bằng:
- Checkbox "Quyền phê duyệt" (can_approve)
- Hiển thị badge "Manager" cho user có can_approve = True

## Rollback (nếu cần)

Nếu cần rollback, restore database từ backup:
```bash
mysql -u ovnm -p db_hr < backup_before_remove_position.sql
```

Sau đó checkout lại code cũ từ git.

## Lưu ý

- ⚠️ Migration này không thể undo tự động
- ⚠️ Tất cả dữ liệu position sẽ bị xóa vĩnh viễn
- ⚠️ Cần cập nhật lại quyền `can_approve` cho các manager sau khi migration
- ✅ Hệ thống vẫn hoạt động bình thường với phòng ban (department)

## Hỗ trợ

Nếu gặp lỗi trong quá trình migration, kiểm tra:
1. Database connection trong `.env`
2. Quyền user database có đủ để ALTER TABLE và DROP TABLE không
3. Log lỗi trong console khi chạy migration script
