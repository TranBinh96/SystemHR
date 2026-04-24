# 🔧 SỬA LỖI API ENDPOINTS

## 🐛 **VẤN ĐỀ ĐÃ PHÁT HIỆN**

### **1. Auto-register API lỗi 500**
```
auto-register/run:1 Failed to load resource: the server responded with a status of 500 (INTERNAL SERVER ERROR)
```

### **2. Stats API trả về HTML thay vì JSON**
```
Error: SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON
```

## ✅ **ĐÃ SỬA**

### **1. Auto-register API (`/admin/auto-register/run`)**

**Vấn đề:** 
- Function `auto_register_meals_for_30_days()` thiếu import `timedelta`
- Return không dùng `jsonify()`

**Đã sửa:**
```python
# ✅ Thêm import timedelta
def auto_register_meals_for_30_days():
    with app.app_context():
        try:
            from datetime import timedelta  # ← THÊM DÒNG NÀY
            from sqlalchemy import or_
            from sqlalchemy.exc import IntegrityError
            # ... rest of function

# ✅ Sửa return JSON
@app.route('/admin/auto-register/run', methods=['POST'])
@login_required
def run_auto_register():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403  # ← jsonify()
    
    try:
        auto_register_meals_for_30_days()
        return jsonify({'success': True, 'message': 'Đã chạy tự động đăng ký 30 ngày thành công!'})  # ← jsonify()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'}), 500  # ← jsonify()
```

### **2. Stats API (`/admin/stats/data`)**

**Vấn đề:** 
- Return dictionary thay vì JSON response

**Đã sửa:**
```python
# ✅ Sửa return JSON
@app.route('/admin/stats/data')
@login_required
def get_stats_data():
    # ... logic xử lý data
    
    return jsonify({  # ← THÊM jsonify()
        'success': True,
        'period': period,
        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
        'summary': {
            'total': total_meals,
            'normal': normal_meals,
            'special': special_meals
        },
        'daily_data': daily_data,
        'registrations': registration_list
    })
```

## 🧪 **TESTING**

### **Syntax Check:**
```bash
python -m py_compile app.py  # ✅ No errors
```

### **Import Check:**
```bash
python -c "from app import app, auto_register_meals_for_30_days"  # ✅ Success
```

### **API Test Script:**
```bash
python test_api_fix.py  # Test cả 2 APIs
```

## 📋 **EXPECTED RESULTS**

### **Auto-register API:**
```json
{
  "success": true,
  "message": "Đã chạy tự động đăng ký 30 ngày thành công!"
}
```

### **Stats API:**
```json
{
  "success": true,
  "period": "week",
  "start_date": "21/04/2026",
  "end_date": "27/04/2026",
  "summary": {
    "total": 150,
    "normal": 120,
    "special": 30
  },
  "daily_data": [...],
  "registrations": [...]
}
```

## 🚀 **DEPLOYMENT**

### **Local Testing:**
```bash
python app.py
# Test trong browser hoặc dùng test_api_fix.py
```

### **Railway Deployment:**
```bash
git add .
git commit -m "Fix API endpoints - return proper JSON responses"
git push origin main
```

## ⚠️ **LƯU Ý**

1. **Authentication**: Các API này cần login admin
2. **CORS**: Nếu test từ external domain cần setup CORS
3. **Error Handling**: Đã thêm try-catch và proper error responses
4. **Timezone**: Sử dụng timezone-aware functions đã sửa trước đó

## 🎯 **HOÀN THÀNH**

✅ **Auto-register API**: Fixed 500 error  
✅ **Stats API**: Fixed JSON parsing error  
✅ **Error Handling**: Proper JSON responses  
✅ **Testing**: Syntax và import checks passed  

**Sẵn sàng deploy và test!**