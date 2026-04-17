# Báo Cáo Kiểm Tra Chức Năng Tự Động Đăng Ký Suất Ăn (CẬP NHẬT)

## Tổng Quan
Hệ thống có 3 cách để tự động đăng ký suất ăn:
1. **Tự động chạy hàng ngày** - Đăng ký 30 ngày cho tất cả user đủ điều kiện
2. **Tự động khi tạo user mới** - Đăng ký 30 ngày ngay khi tạo user
3. **Tự động khi kích hoạt user** - Đăng ký 30 ngày khi chuyển user từ inactive → active
4. **Chạy thủ công qua script** - Dùng khi cần thiết

---

## 1. Tự Động Chạy Hàng Ngày (NÂNG CẤP: 30 NGÀY)

### Cấu Hình
- **Thời gian chạy**: 16:00 (4 giờ chiều) mỗi ngày
- **Số ngày đăng ký**: 30 ngày tới (từ ngày mai)
- **Scheduler**: APScheduler với BackgroundScheduler
- **Function**: `auto_register_meals_for_30_days()`

### Điều Kiện Áp Dụng
Chỉ tự động đăng ký cho nhân viên thỏa mãn TẤT CẢ các điều kiện sau:
- ✅ `is_active = True` (tài khoản đang hoạt động)
- ✅ `work_status = 'working'` (đang làm việc)
- ✅ Mã nhân viên bắt đầu bằng **10** hoặc **20**

### Quy Trình Hoạt Động
1. Lấy danh sách user đủ điều kiện
2. Lặp qua 30 ngày (từ ngày mai đến 30 ngày sau)
3. Với mỗi ngày:
   - Tìm menu bình thường (không phải cải thiện)
   - Nếu không có menu → Bỏ qua ngày này
   - Nếu có menu → Kiểm tra từng user:
     - Đã có đăng ký (dù bình thường hay cải thiện) → Bỏ qua
     - Chưa có đăng ký → Tự động đăng ký suất ăn bình thường
4. Lưu vào database với ghi chú: "Tự động đăng ký bởi hệ thống"

### Logs Mới
```
[AUTO REGISTER] Bắt đầu tự động đăng ký 30 ngày (20/04/2026 → 19/05/2026)
[AUTO REGISTER] Tìm thấy 50 user đang hoạt động (mã 10xx, 20xx)
[AUTO REGISTER] Ngày 20/04: Cơm gà xối mỡ | Đã có: 10 | Tự động: 40
[AUTO REGISTER] Ngày 21/04: Cơm sườn nướng | Đã có: 15 | Tự động: 35
[AUTO REGISTER] Ngày 22/04: Không có menu bình thường - Bỏ qua
...
[AUTO REGISTER] ✓ Hoàn thành!
[AUTO REGISTER] Tổng: 28 ngày | 50 users | Đã có: 350 | Tự động: 1050
```

---

## 2. Tự Động Khi Tạo User Mới (MỚI)

### Khi Nào Chạy
- Khi admin tạo user mới qua trang `/admin/users`
- Ngay sau khi user được tạo thành công

### Điều Kiện
- User phải có `is_active = True` (mặc định khi tạo mới)
- User phải có `work_status = 'working'` (mặc định)
- Mã nhân viên phải bắt đầu bằng **10** hoặc **20**

### Quy Trình
1. Admin tạo user mới
2. User được lưu vào database
3. Hệ thống tự động gọi `auto_register_meals_for_user(user_id, days=30)`
4. Đăng ký 30 ngày tới cho user mới
5. Hiển thị thông báo: "Đã thêm nhân viên [Tên] và tự động đăng ký X ngày"

### Ví Dụ
```
Admin tạo user mới:
- Mã: 1099
- Tên: Nguyễn Văn A
- Ngày tạo: 20/04/2026

Kết quả:
✅ User được tạo thành công
✅ Tự động đăng ký 28 ngày (21/04 → 19/05)
✅ Thông báo: "Đã thêm nhân viên Nguyễn Văn A và tự động đăng ký 28 ngày"
```

---

## 3. Tự Động Khi Kích Hoạt User (MỚI)

### Khi Nào Chạy
- Khi admin chuyển user từ `is_active = False` → `is_active = True`
- Qua trang edit user `/admin/users/<id>/edit`

### Điều Kiện
- User vừa được kích hoạt (từ inactive → active)
- User phải có `work_status = 'working'`
- Mã nhân viên phải bắt đầu bằng **10** hoặc **20**

### Quy Trình
1. Admin edit user và tick vào "Active"
2. Hệ thống phát hiện user vừa được kích hoạt
3. Tự động gọi `auto_register_meals_for_user(user_id, days=30)`
4. Đăng ký 30 ngày tới cho user
5. Hiển thị thông báo: "Đã cập nhật thông tin [Tên] và tự động đăng ký X ngày"

### Ví Dụ
```
User nghỉ việc trước đó (is_active = False)
Admin kích hoạt lại user vào ngày 20/04/2026

Kết quả:
✅ User được kích hoạt
✅ Tự động đăng ký 28 ngày (21/04 → 19/05)
✅ Thông báo: "Đã cập nhật thông tin Nguyễn Văn A và tự động đăng ký 28 ngày"
```

---

## 4. Helper Function: auto_register_meals_for_user()

### Mục Đích
Function dùng chung cho cả tạo user mới và kích hoạt user

### Parameters
- `user_id`: ID của user cần đăng ký
- `days`: Số ngày cần đăng ký (mặc định 30)

### Returns
```python
{
    'success': True/False,
    'registered': 28,  # Số ngày đã đăng ký
    'skipped': 2,      # Số ngày bỏ qua (đã có hoặc không có menu)
    'message': 'Đã đăng ký 28 ngày, bỏ qua 2 ngày'
}
```

### Logic
1. Kiểm tra user tồn tại
2. Kiểm tra điều kiện (active, working, mã 10xx/20xx)
3. Lặp qua số ngày cần đăng ký
4. Với mỗi ngày:
   - Kiểm tra đã có đăng ký chưa → Bỏ qua
   - Tìm menu bình thường → Nếu không có → Bỏ qua
   - Tạo đăng ký mới
5. Commit và trả về kết quả

---

## 5. Xử Lý User Đăng Ký Sau

### Trường Hợp
User đã được tự động đăng ký suất ăn bình thường, sau đó user tự đăng ký cải thiện

### Xử Lý
- User có thể tự update/thay đổi đăng ký
- Hệ thống cho phép thay đổi từ bình thường → cải thiện
- Hoặc hủy đăng ký nếu muốn

### Lần Chạy Tự Động Tiếp Theo
- Kiểm tra: User đã có đăng ký (dù tự động hay thủ công) → **BỎ QUA**
- Không ghi đè lên đăng ký hiện tại
- Chỉ đăng ký cho ngày chưa có đăng ký

---

## 6. Lưu Ý Quan Trọng

### ⚠️ Điều kiện để tự động đăng ký hoạt động:
1. **Phải có menu bình thường** (`is_special = False`) cho ngày đó
2. **Menu phải active** (`is_active = True`)
3. **Menu phải là lunch** (`meal_type = 'lunch'`)
4. **Server phải đang chạy** (app.py đang chạy) - chỉ cho auto hàng ngày

### ⚠️ Nhân viên nào được tự động đăng ký?
- Chỉ mã bắt đầu bằng **10** hoặc **20** (ví dụ: 1001, 2005)
- Phải `is_active = True` và `work_status = 'working'`

### ⚠️ Nếu không hoạt động:
1. Kiểm tra có menu bình thường cho các ngày tới chưa
2. Kiểm tra console có lỗi không
3. Kiểm tra APScheduler đã được cài đặt chưa: `pip install apscheduler`
4. Kiểm tra mã nhân viên có đúng format không (10xx, 20xx)

---

## 7. So Sánh Trước và Sau

### TRƯỚC (Cũ)
- ❌ Chỉ đăng ký 1 ngày (ngày mai)
- ❌ User mới phải đợi đến 16:00 ngày hôm sau
- ❌ User được kích hoạt lại không tự động đăng ký

### SAU (Mới)
- ✅ Đăng ký 30 ngày tới
- ✅ User mới được đăng ký ngay lập tức
- ✅ User được kích hoạt lại tự động đăng ký
- ✅ Logs chi tiết hơn (hiển thị từng ngày)
- ✅ Xử lý lỗi tốt hơn (bỏ qua ngày không có menu)

---

## 8. Test Thử

### Test 1: Tạo user mới
1. Vào `/admin/users`
2. Tạo user mới với mã 1099
3. Kiểm tra thông báo có hiển thị "tự động đăng ký X ngày"
4. Vào trang đăng ký suất ăn của user → Kiểm tra đã có đăng ký 30 ngày

### Test 2: Kích hoạt user
1. Chọn 1 user inactive
2. Edit và tick "Active"
3. Kiểm tra thông báo có hiển thị "tự động đăng ký X ngày"
4. Vào trang đăng ký suất ăn của user → Kiểm tra đã có đăng ký 30 ngày

### Test 3: Auto hàng ngày
1. Đợi đến 16:00
2. Kiểm tra console logs
3. Xem có hiển thị "[AUTO REGISTER]" không
4. Kiểm tra database có records mới không

---

## Kết Luận

✅ **Đã nâng cấp thành công**
- Từ 1 ngày → 30 ngày
- Thêm tự động khi tạo user mới
- Thêm tự động khi kích hoạt user
- Logs chi tiết và dễ theo dõi

✅ **User mới không bị thiếu suất ăn**
- Được đăng ký ngay khi tạo
- Không phải đợi đến 16:00 ngày hôm sau

✅ **Linh hoạt và an toàn**
- Không ghi đè đăng ký hiện tại
- Cho phép user tự thay đổi sau
- Xử lý lỗi tốt (bỏ qua ngày không có menu)
