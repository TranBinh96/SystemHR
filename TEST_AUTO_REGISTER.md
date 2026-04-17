# Hướng Dẫn Test Chức Năng Tự Động Đăng Ký 30 Ngày

## Đã Thay Đổi Gì?

### TRƯỚC (Cũ)
- Chỉ đăng ký 1 ngày (ngày mai)
- User mới phải đợi đến 16:00 ngày hôm sau
- User được kích hoạt lại không tự động đăng ký
- Phải đợi đến 16:00 mới chạy tự động

### SAU (Mới)
- ✅ Đăng ký 30 ngày tới
- ✅ User mới được đăng ký ngay lập tức
- ✅ User được kích hoạt lại tự động đăng ký
- ✅ Logs chi tiết hơn
- ✅ **Tự động chạy khi vào trang thống kê**
- ✅ **Có nút chạy thủ công bất cứ lúc nào**

---

## Cách Kích Hoạt Auto-Register

### Cách 1: Tự động khi vào trang thống kê (MỚI - DỄ NHẤT)
1. Vào trang: `http://localhost:5000/admin/stats`
2. Hệ thống tự động chạy auto-register 30 ngày
3. Xem console logs để biết chi tiết
4. **Không cần làm gì thêm!**

### Cách 2: Click nút "Chạy Auto 30 ngày" (MỚI)
1. Vào trang: `http://localhost:5000/admin/stats`
2. Click nút **"Chạy Auto 30 ngày"** (nút màu xanh lá)
3. Xác nhận trong popup
4. Đợi thông báo "Đã chạy tự động đăng ký 30 ngày thành công!"
5. Xem console logs để biết chi tiết

### Cách 3: Tự động lúc 16:00 hàng ngày
- Hệ thống vẫn tự động chạy lúc 16:00
- Không cần làm gì

### Cách 4: Khi tạo user mới
- Tạo user mới → Tự động đăng ký 30 ngày

### Cách 5: Khi kích hoạt user
- Kích hoạt user → Tự động đăng ký 30 ngày

---

## Test 0: Test Nhanh Nhất (KHUYẾN NGHỊ)

### Bước 1: Vào trang thống kê
1. Mở trình duyệt
2. Vào: `http://localhost:5000/admin/stats`
3. Xem console (F12 → Console tab)

### Bước 2: Xem logs
Logs sẽ hiển thị:
```
[ADMIN STATS] Tự động chạy auto-register 30 ngày...
=== [AUTO REGISTER] Bắt đầu tự động đăng ký 30 ngày (20/04/2026 → 19/05/2026) ===
[AUTO REGISTER] Tìm thấy 50 user đang hoạt động (mã 10xx, 20xx)
[AUTO REGISTER] Ngày 20/04: Cơm gà xối mỡ | Đã có: 10 | Tự động: 40
...
[AUTO REGISTER] ✓ Hoàn thành!
```

### Bước 3: Click nút "Chạy Auto 30 ngày"
1. Click nút màu xanh lá
2. Xác nhận popup
3. Xem thông báo thành công
4. Xem console logs

### Kết Quả Mong Đợi
- ✅ Tự động chạy khi vào trang
- ✅ Có thể chạy lại bằng nút
- ✅ Logs chi tiết trong console
- ✅ Thông báo thành công

---

## Test 1: Tạo User Mới (KHUYẾN NGHỊ TEST ĐẦU TIÊN)

### Bước 1: Tạo user mới
1. Vào trang: `http://localhost:5000/admin/users`
2. Click "Thêm nhân viên mới"
3. Nhập thông tin:
   - Mã nhân viên: `1099` (hoặc `2099`)
   - Tên: `Test User Auto Register`
   - Phòng ban: Chọn phòng ban bất kỳ
   - Mật khẩu: `123456`
   - Role: `user`
   - Work Status: `working`
   - Active: ✅ (tick vào)
4. Click "Lưu"

### Bước 2: Kiểm tra thông báo
- Thông báo phải hiển thị: **"Đã thêm nhân viên Test User Auto Register và tự động đăng ký X ngày"**
- X là số ngày có menu bình thường (tối đa 30)

### Bước 3: Kiểm tra đăng ký
1. Đăng nhập bằng user mới (mã: 1099, pass: 123456)
2. Vào trang đăng ký suất ăn
3. Kiểm tra xem đã có đăng ký cho các ngày tới chưa
4. Ghi chú phải là: "Tự động đăng ký bởi hệ thống"

### Kết Quả Mong Đợi
- ✅ User được tạo thành công
- ✅ Có thông báo tự động đăng ký
- ✅ User có đăng ký cho 30 ngày tới (hoặc ít hơn nếu không đủ menu)

---

## Test 2: Kích Hoạt User Đã Tắt

### Bước 1: Tắt 1 user
1. Vào `/admin/users`
2. Chọn 1 user có mã 10xx hoặc 20xx
3. Edit user, bỏ tick "Active"
4. Lưu

### Bước 2: Kích hoạt lại user
1. Edit user đó lại
2. Tick vào "Active"
3. Đảm bảo "Work Status" là "working"
4. Lưu

### Bước 3: Kiểm tra thông báo
- Thông báo phải hiển thị: **"Đã cập nhật thông tin [Tên] và tự động đăng ký X ngày"**

### Bước 4: Kiểm tra đăng ký
1. Đăng nhập bằng user đó
2. Vào trang đăng ký suất ăn
3. Kiểm tra có đăng ký mới cho các ngày tới

### Kết Quả Mong Đợi
- ✅ User được kích hoạt
- ✅ Có thông báo tự động đăng ký
- ✅ User có đăng ký cho 30 ngày tới

---

## Test 3: Auto Chạy Hàng Ngày Lúc 16:00

### Cách 1: Đợi đến 16:00
1. Để server chạy
2. Đợi đến 16:00
3. Xem console logs

### Cách 2: Test ngay (Sửa thời gian tạm thời)

#### Bước 1: Sửa thời gian trong app.py
Tìm dòng này (gần cuối file):
```python
scheduler.add_job(
    func=auto_register_meals_for_30_days,
    trigger=CronTrigger(hour=16, minute=0),  # <-- Dòng này
    id='auto_register_meals',
    name='Tự động đăng ký suất ăn 30 ngày',
    replace_existing=True
)
```

Sửa thành thời gian hiện tại + 2 phút. Ví dụ nếu bây giờ là 14:30:
```python
trigger=CronTrigger(hour=14, minute=32),  # 14:32
```

#### Bước 2: Restart server
```bash
# Tắt server (Ctrl+C)
# Chạy lại
python app.py
```

#### Bước 3: Đợi đến thời gian đã set
- Xem console logs
- Phải xuất hiện logs như sau:

```
=== [AUTO REGISTER] Bắt đầu tự động đăng ký 30 ngày (20/04/2026 → 19/05/2026) ===
[AUTO REGISTER] Tìm thấy 50 user đang hoạt động (mã 10xx, 20xx)
[AUTO REGISTER] Ngày 20/04: Cơm gà xối mỡ | Đã có: 10 | Tự động: 40
[AUTO REGISTER] Ngày 21/04: Cơm sườn nướng | Đã có: 15 | Tự động: 35
[AUTO REGISTER] Ngày 22/04: Không có menu bình thường - Bỏ qua
...
[AUTO REGISTER] ✓ Hoàn thành!
[AUTO REGISTER] Tổng: 28 ngày | 50 users | Đã có: 350 | Tự động: 1050
```

#### Bước 4: Sửa lại thời gian về 16:00
```python
trigger=CronTrigger(hour=16, minute=0),
```

### Kết Quả Mong Đợi
- ✅ Logs hiển thị chi tiết từng ngày
- ✅ Tổng số ngày, users, đã có, tự động
- ✅ Database có records mới

---

## Test 4: Kiểm Tra Logic "Không Ghi Đè"

### Bước 1: Tạo user mới (mã 1098)
- User sẽ được tự động đăng ký 30 ngày

### Bước 2: Đăng nhập bằng user đó
- Vào trang đăng ký suất ăn
- Chọn 1 ngày bất kỳ
- Thay đổi từ "Bình thường" → "Cải thiện"
- Lưu

### Bước 3: Chạy lại auto-register
- Chạy script hoặc đợi đến 16:00
- Xem logs

### Kết Quả Mong Đợi
- ✅ Ngày đã thay đổi sang cải thiện **KHÔNG** bị ghi đè
- ✅ Logs hiển thị: "Đã có: X" (bao gồm ngày đã thay đổi)
- ✅ User vẫn giữ được đăng ký cải thiện

---

## Test 5: Kiểm Tra Mã Nhân Viên

### Test với mã KHÔNG phải 10xx, 20xx

#### Bước 1: Tạo user mã 3001
- Mã: `3001`
- Tên: `Test User Wrong Code`
- Active: ✅
- Work Status: `working`

#### Bước 2: Kiểm tra thông báo
- Thông báo chỉ hiển thị: **"Đã thêm nhân viên Test User Wrong Code"**
- KHÔNG có "tự động đăng ký"

#### Bước 3: Kiểm tra đăng ký
- Đăng nhập bằng user 3001
- Vào trang đăng ký suất ăn
- **KHÔNG** có đăng ký tự động

### Kết Quả Mong Đợi
- ✅ User được tạo nhưng KHÔNG tự động đăng ký
- ✅ Chỉ mã 10xx và 20xx mới được tự động đăng ký

---

## Checklist Tổng Hợp

### Chức Năng
- [ ] Tạo user mới (mã 10xx) → Tự động đăng ký 30 ngày
- [ ] Tạo user mới (mã 20xx) → Tự động đăng ký 30 ngày
- [ ] Tạo user mới (mã 30xx) → KHÔNG tự động đăng ký
- [ ] Kích hoạt user → Tự động đăng ký 30 ngày
- [ ] Auto chạy lúc 16:00 → Đăng ký 30 ngày cho tất cả user
- [ ] User tự thay đổi đăng ký → Không bị ghi đè

### Logs
- [ ] Logs hiển thị chi tiết từng ngày
- [ ] Logs hiển thị tổng số users, đã có, tự động
- [ ] Logs hiển thị ngày không có menu

### Thông Báo
- [ ] Tạo user mới → "Đã thêm... và tự động đăng ký X ngày"
- [ ] Kích hoạt user → "Đã cập nhật... và tự động đăng ký X ngày"
- [ ] User mã sai → Chỉ "Đã thêm..." (không có tự động đăng ký)

---

## Lỗi Thường Gặp

### Lỗi 1: Không có menu bình thường
**Triệu chứng**: Logs hiển thị "Không có menu bình thường - Bỏ qua"

**Giải pháp**:
1. Vào trang quản lý menu
2. Tạo menu bình thường cho các ngày tới
3. Đảm bảo:
   - `is_special = False` (không phải cải thiện)
   - `is_active = True`
   - `meal_type = 'lunch'`

### Lỗi 2: Không tự động đăng ký khi tạo user
**Triệu chứng**: Thông báo không có "tự động đăng ký"

**Kiểm tra**:
1. Mã nhân viên có bắt đầu bằng 10 hoặc 20 không?
2. User có `is_active = True` không?
3. User có `work_status = 'working'` không?
4. Console có lỗi không?

### Lỗi 3: Scheduler không chạy
**Triệu chứng**: Đến 16:00 không có logs

**Kiểm tra**:
1. Server có đang chạy không?
2. APScheduler đã cài đặt chưa: `pip install apscheduler`
3. Console có lỗi khi khởi động không?

---

## Kết Luận

Sau khi test xong, bạn sẽ có:
- ✅ User mới tự động có suất ăn 30 ngày
- ✅ User được kích hoạt lại có suất ăn 30 ngày
- ✅ Hệ thống tự động chạy hàng ngày lúc 16:00
- ✅ Không ghi đè đăng ký của user
- ✅ Logs chi tiết và dễ theo dõi

**Test đầu tiên nên làm: Test 1 - Tạo User Mới** (dễ nhất và nhanh nhất)
