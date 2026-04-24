# 🕐 HƯỚNG DẪN SỬA LỖI TIMEZONE KHI DEPLOY

## ❌ **VẤN ĐỀ**
Khi deploy lên server, ngày giờ bị sai do:
- Server có timezone khác với local (thường là UTC)
- Code sử dụng `datetime.now()` và `datetime.utcnow()` không consistent
- Không có timezone configuration

## 🔍 **NGUYÊN NHÂN**
1. **Server timezone**: Server thường dùng UTC, local dùng Asia/Ho_Chi_Minh
2. **Mixed datetime usage**: 
   - `datetime.now()` → Local time của server (UTC)
   - `datetime.utcnow()` → UTC time
   - `date.today()` → Local date của server
3. **Không có timezone conversion**

## ✅ **GIẢI PHÁP**

### **1. Cài đặt pytz**
```bash
pip install pytz==2023.3
```

### **2. Sử dụng Timezone Utils**
Đã tạo file `utils/timezone_utils.py` với các function:
- `now()` → Current datetime in Vietnam timezone
- `today()` → Current date in Vietnam timezone  
- `utcnow()` → Current UTC datetime (for database)
- `format_local_datetime()` → Format datetime to Vietnam timezone

### **3. Thay thế trong Code**

#### **Trong app.py:**
```python
# ❌ Cũ
from datetime import datetime, timedelta

today = datetime.now().date()
current_time = datetime.now()
utc_time = datetime.utcnow()

# ✅ Mới
from utils.timezone_utils import now, today, utcnow

today_date = today()
current_time = now()
utc_time = utcnow()
```

#### **Các chỗ cần sửa chính:**

**1. Dashboard overtime stats:**
```python
# ❌ Cũ
today = date.today()

# ✅ Mới  
today_date = today()
```

**2. Auto-register meals:**
```python
# ❌ Cũ
today = datetime.now().date()

# ✅ Mới
today_date = today()
```

**3. User activity tracking:**
```python
# ❌ Cũ
user.last_activity = datetime.utcnow()

# ✅ Mới
user.last_activity = utcnow()
```

**4. Admin meals week calculation:**
```python
# ❌ Cũ
today = datetime.now().date()
start_of_week = today - timedelta(days=today.weekday())

# ✅ Mới
today_date = today()
start_of_week = today_date - timedelta(days=today_date.weekday())
```

### **4. Sửa Models (nếu cần)**

#### **Trong models/__init__.py:**
```python
# Thêm import
from utils.timezone_utils import utcnow

# Sửa default values
created_at = db.Column(db.DateTime, default=utcnow)
updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
```

### **5. Template Display**

#### **Hiển thị datetime trong template:**
```python
# Trong route function
from utils.timezone_utils import format_local_datetime

# Format datetime trước khi gửi đến template
formatted_time = format_local_datetime(user.last_activity, '%d/%m/%Y %H:%M')
```

## 🚀 **CÁCH THỰC HIỆN**

### **Bước 1: Cài đặt dependency**
```bash
pip install pytz==2023.3
```

### **Bước 2: Thêm import vào app.py**
```python
# Thêm dòng này sau các import khác
from utils.timezone_utils import now, today, utcnow, format_local_datetime, format_local_date
```

### **Bước 3: Thay thế từng chỗ**
Tìm và thay thế các pattern sau trong `app.py`:

```bash
# Tìm: datetime.now().date()
# Thay: today()

# Tìm: datetime.now()
# Thay: now()

# Tìm: datetime.utcnow()
# Thay: utcnow()

# Tìm: date.today()
# Thay: today()
```

### **Bước 4: Test local trước**
```python
# Test timezone utils
from utils.timezone_utils import now, today, utcnow

print("Local now:", now())
print("Local today:", today())  
print("UTC now:", utcnow())
```

### **Bước 5: Deploy và kiểm tra**
- Deploy code mới lên server
- Kiểm tra log xem thời gian có đúng không
- Test các chức năng liên quan đến ngày giờ

## 🧪 **KIỂM TRA**

### **1. Kiểm tra Auto-register**
```python
# Trong log auto-register, thời gian phải đúng timezone VN
[AUTO REGISTER] Bắt đầu tự động đăng ký 30 ngày (25/04/2026 → 24/05/2026)
```

### **2. Kiểm tra User activity**
```python
# Last activity phải hiển thị đúng giờ VN
user.last_activity = 2026-04-24 15:30:00 (UTC)
# Hiển thị: 24/04/2026 22:30 (VN time)
```

### **3. Kiểm tra Meal registration**
```python
# Ngày đăng ký phải đúng theo VN timezone
today_meal = MealRegistration.query.filter(
    MealRegistration.date == today()  # VN date
)
```

## 📋 **CHECKLIST**

- [ ] Cài đặt pytz
- [ ] Tạo utils/timezone_utils.py
- [ ] Thêm import vào app.py
- [ ] Sửa dashboard overtime stats
- [ ] Sửa auto-register meals
- [ ] Sửa user activity tracking
- [ ] Sửa admin meals calculations
- [ ] Test local
- [ ] Deploy và test production

## ⚠️ **LƯU Ý**

1. **Database**: Vẫn lưu UTC trong database, chỉ convert khi hiển thị
2. **Consistency**: Tất cả datetime operations phải dùng timezone utils
3. **Testing**: Test kỹ trước khi deploy production
4. **Backup**: Backup database trước khi thay đổi

## 🔧 **TROUBLESHOOTING**

### **Lỗi import pytz:**
```bash
pip install pytz==2023.3
```

### **Lỗi timezone not found:**
```python
# Kiểm tra TIMEZONE trong .env
TIMEZONE=Asia/Ho_Chi_Minh
```

### **Thời gian vẫn sai:**
- Kiểm tra server timezone: `date`
- Kiểm tra Python timezone: `import datetime; print(datetime.datetime.now())`
- Restart application sau khi sửa code

---

**Sau khi thực hiện các bước trên, hệ thống sẽ hiển thị đúng giờ Việt Nam (UTC+7) dù deploy ở server nào!**