# 🔧 HƯỚNG DẪN SỬA LỖI DUPLICATE ĐĂNG KÝ SUẤT ĂN

## ❌ **VẤN ĐỀ**
- Một người dùng xuất hiện nhiều lần trong cùng một ngày với cùng món ăn
- Vi phạm quy tắc: "1 người chỉ đăng ký 1 món 1 ngày duy nhất"
- Gây sai dữ liệu thống kê

## 🔍 **NGUYÊN NHÂN**
1. **Không có UNIQUE constraint** trong database để ngăn chặn duplicate
2. **Auto-register chạy nhiều lần**:
   - Scheduler hàng ngày lúc 16:00
   - Khi admin vào trang thống kê
   - Khi admin nhấn nút "Chạy Auto 30 ngày"
   - Khi tạo/sửa user
3. **Không có xử lý lỗi IntegrityError** khi insert duplicate

## ✅ **GIẢI PHÁP ĐÃ THỰC HIỆN**

### 1. **Thêm UNIQUE Constraint vào Model**
```python
class MealRegistration(db.Model):
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date_meal'),
    )
```

### 2. **Cải thiện Logic Auto-Register**
- Thêm xử lý `IntegrityError` với `db.session.flush()`
- Commit từng ngày thay vì commit toàn bộ
- Thêm logging chi tiết để debug
- Tắt auto-register khi vào trang thống kê

### 3. **Tạo Scripts Hỗ Trợ**
- `cleanup_duplicate_meals.py`: Dọn dẹp duplicate hiện tại
- `add_unique_constraint.py`: Thêm constraint vào database

## 🚀 **CÁCH THỰC HIỆN**

### **Bước 1: Kiểm tra tình trạng hiện tại**
```bash
cd scripts
python cleanup_duplicate_meals.py --stats
```

### **Bước 2: Dọn dẹp duplicate (nếu có)**
```bash
python cleanup_duplicate_meals.py --cleanup
```

### **Bước 3: Thêm UNIQUE constraint**
```bash
python add_unique_constraint.py --add
```

### **Bước 4: Kiểm tra lại**
```bash
python add_unique_constraint.py --check
python cleanup_duplicate_meals.py --stats
```

### **Bước 5: Restart ứng dụng**
```bash
# Restart Flask app để áp dụng model changes
```

## 📋 **KIỂM TRA SAU KHI SỬA**

### 1. **Kiểm tra Database**
```sql
-- Kiểm tra constraint
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'meal_registrations' AND constraint_type = 'UNIQUE';

-- Kiểm tra duplicate
SELECT user_id, date, COUNT(*) as count
FROM meal_registrations 
GROUP BY user_id, date 
HAVING COUNT(*) > 1;
```

### 2. **Test Auto-Register**
- Vào Admin → Thống kê → Nhấn "Chạy Auto 30 ngày"
- Kiểm tra console log xem có lỗi không
- Kiểm tra database xem có duplicate mới không

### 3. **Test Manual Register**
- User thử đăng ký 2 lần cùng 1 ngày
- Hệ thống phải từ chối hoặc update thay vì tạo mới

## 🛡️ **PHÒNG NGỪA TƯƠNG LAI**

### 1. **Database Level**
- ✅ UNIQUE constraint `(user_id, date)`
- ✅ Proper error handling

### 2. **Application Level**
- ✅ Check existing before insert
- ✅ Use `db.session.flush()` để kiểm tra constraint sớm
- ✅ Commit từng batch thay vì toàn bộ

### 3. **Monitoring**
- Thêm logging chi tiết
- Monitor duplicate qua script định kỳ
- Alert khi có lỗi auto-register

## 📊 **EXPECTED RESULTS**

### **Trước khi sửa:**
```
Nguyễn Thị Hồng    20012    Sản xuất    Cơm suốn nướng    Bình Thường
Nguyễn Thị Hồng    20012    Sản xuất    Cơm suốn nướng    Bình Thường  ← DUPLICATE
Nguyễn Thị Hồng    20012    Sản xuất    Cơm suốn nướng    Bình Thường  ← DUPLICATE
```

### **Sau khi sửa:**
```
Nguyễn Thị Hồng    20012    Sản xuất    Cơm suốn nướng    Bình Thường  ← DUY NHẤT
```

## 🔧 **TROUBLESHOOTING**

### **Lỗi khi thêm constraint:**
```
ERROR: Duplicate entry 'xxx-2024-04-23' for key 'unique_user_date_meal'
```
**Giải pháp:** Chạy cleanup trước khi add constraint

### **Auto-register vẫn tạo duplicate:**
**Kiểm tra:**
- Model có `__table_args__` chưa?
- Database có constraint chưa?
- Code có xử lý `IntegrityError` chưa?

### **Performance chậm:**
**Nguyên nhân:** Constraint check mỗi lần insert
**Giải pháp:** Đã tối ưu bằng cách check existing trước khi insert

---

## 📞 **HỖ TRỢ**
Nếu gặp vấn đề, kiểm tra:
1. Console logs khi chạy auto-register
2. Database constraint status
3. Model definition trong `models/__init__.py`