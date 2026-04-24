# 🚂 SỬA LỖI TIMEZONE TRÊN RAILWAY.COM

## 🔍 **ĐẶC ĐIỂM RAILWAY**

Railway.com có những đặc điểm sau về timezone:
- **Server timezone**: UTC (GMT+0)
- **Container timezone**: UTC 
- **Database timezone**: UTC
- **Giải pháp**: Sử dụng timezone utils và environment variables

## ❌ **VẤN ĐỀ HIỆN TẠI**

```python
# Code cũ sử dụng:
datetime.now()        # → UTC time (sai 7 tiếng)
datetime.utcnow()     # → UTC time  
date.today()          # → UTC date (có thể sai ngày)

# Kết quả:
# VN: 24/04/2026 22:30 (tối)
# Railway: 24/04/2026 15:30 (chiều) ← SAI!
```

## ✅ **GIẢI PHÁP CHO RAILWAY**

### **1. Environment Variables**

Thêm vào Railway Environment Variables:
```bash
TIMEZONE=Asia/Ho_Chi_Minh
TZ=Asia/Ho_Chi_Minh
```

**Cách thêm:**
1. Vào Railway Dashboard → Your Project
2. Click **Variables** tab
3. Thêm:
   - `TIMEZONE` = `Asia/Ho_Chi_Minh`
   - `TZ` = `Asia/Ho_Chi_Minh`

### **2. Code Changes - ĐÃ HOÀN THÀNH**

#### **✅ Đã sửa trong app.py:**
```python
# ✅ Import timezone utilities
from utils.timezone_utils import now, today, utcnow, format_local_datetime, format_local_date

# ✅ Scheduler sử dụng múi giờ VN
scheduler.add_job(
    func=auto_register_meals_for_30_days,
    trigger=CronTrigger(hour=16, minute=0, timezone='Asia/Ho_Chi_Minh'),  # 16:00 VN time
    id='auto_register_meals'
)

# ✅ Tất cả datetime.now() → now()
# ✅ Tất cả datetime.now().date() → today()
# ✅ Tất cả date.today() → today()
```

### **3. Timezone Utils**

File `utils/timezone_utils.py` cung cấp:
```python
now()     # Thời gian hiện tại VN (UTC+7)
today()   # Ngày hiện tại VN
utcnow()  # UTC time cho database
```

## 🚀 **DEPLOY STEPS CHO RAILWAY**

### **Bước 1: Cập nhật Environment Variables**
```bash
# Trong Railway Dashboard → Variables
TIMEZONE=Asia/Ho_Chi_Minh
TZ=Asia/Ho_Chi_Minh
```

### **Bước 2: Commit và Push Code**
```bash
git add .
git commit -m "Fix timezone for Railway deployment - use Asia/Ho_Chi_Minh"
git push origin main
```

### **Bước 3: Railway sẽ tự động deploy**
- Railway detect changes và redeploy
- Kiểm tra deployment logs

### **Bước 4: Kiểm tra**
```python
# Test trong Railway console hoặc logs
from utils.timezone_utils import now, today
print(f"VN time: {now()}")  # 2026-04-24 16:00:00+07:00
print(f"VN date: {today()}")  # 2026-04-24
```

## 🧪 **TESTING TRÊN RAILWAY**

### **1. Kiểm tra Auto-register**
Xem logs lúc 16:00 VN:
```
[AUTO REGISTER] Bắt đầu tự động đăng ký 30 ngày (25/04/2026 → 24/05/2026)
```

### **2. Kiểm tra User Login**
```python
# Last activity hiển thị đúng giờ VN
# VN: 24/04/2026 22:30
# DB: 2026-04-24 15:30:00 UTC (tự động convert)
```

### **3. Kiểm tra Meal Registration**
```python
# Đăng ký suất ăn theo ngày VN
# VN 00:01 → Ngày mới
# Scheduler 16:00 VN → Auto register
```

## 📋 **RAILWAY-SPECIFIC COMMANDS**

### **Xem logs:**
```bash
railway logs
```

### **Connect to database:**
```bash
railway connect
```

### **Run command:**
```bash
railway run python -c "from utils.timezone_utils import now; print(now())"
```

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **1. Database Timezone**
- Railway MySQL/PostgreSQL luôn dùng UTC
- **KHÔNG** thay đổi database timezone
- Timezone utils tự động convert khi lưu/đọc

### **2. Scheduler**
```python
# APScheduler trên Railway
scheduler.add_job(
    func=auto_register_meals_for_30_days,
    trigger=CronTrigger(hour=16, minute=0, timezone='Asia/Ho_Chi_Minh'),  # 16:00 VN
    id='auto_register_meals'
)
```

### **3. Environment Variables Priority**
Railway environment variables override local .env:
```
Railway Variables > .env file > default values
```

## 📊 **EXPECTED RESULTS**

### **Trước khi sửa (Railway UTC):**
```
Auto-register: 09:00 UTC ❌ Sai giờ VN
User activity: 15:30 UTC hiển thị 15:30 ❌ Sai 7 tiếng
Meal date: 2026-04-24 UTC có thể sai ngày ❌
```

### **Sau khi sửa (Railway + Timezone Utils):**
```
Auto-register: 16:00 VN ✅ Đúng giờ VN
User activity: 15:30 UTC hiển thị 22:30 VN ✅ Đúng
Meal date: 2026-04-25 VN ✅ Đúng ngày
```

---

## 🎯 **HOÀN THÀNH**

✅ **Code đã được sửa hoàn toàn**
✅ **Timezone utils đã implement**  
✅ **Scheduler sử dụng múi giờ VN**
✅ **Tất cả datetime calls đã được thay thế**

**Chỉ cần:**
1. **Thêm Environment Variables** trong Railway Dashboard
2. **Deploy** code lên Railway
3. **Kiểm tra** logs sau khi deploy

**Railway sẽ tự động redeploy khi detect code changes!**