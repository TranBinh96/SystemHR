# CẬP NHẬT TRANG NHẬT KÝ BỮA ĂN

## ✅ Các thay đổi đã thực hiện

### 1. **Giao diện Timeline thay vì Table**
- ❌ Xóa: Table layout phức tạp
- ✅ Thêm: Timeline/Card layout đơn giản, dễ đọc

### 2. **Group theo ngày**
- Mỗi ngày là một card riêng
- Header hiển thị: Ngày + Thứ + Số lượng đăng ký
- Ví dụ: "📅 Thứ hai, 24/4/2026 - 2 đăng ký"

### 3. **Chỉ hiển thị 5 ngày gần nhất**
- Sắp xếp theo ngày mới nhất trước
- Chỉ lấy 5 ngày đầu tiên
- Giảm thông tin hiển thị, tập trung vào dữ liệu gần đây

### 4. **Logic Cải thiện vs Tự đăng ký**
- ✅ **Cải thiện**: Nếu `meal_type` chứa chữ "Cải" → Hiển thị "⭐ Cải thiện"
- ✅ **Tự đăng ký**: Các trường hợp còn lại → Hiển thị "📝 Tự đăng ký"

### 5. **Hiển thị ít thông tin hơn**
Mỗi meal item chỉ hiển thị:
- 👤 Avatar
- Tên nhân viên (lớn, bold)
- 🏢 Phòng ban
- 🍽️ Mã bữa ăn
- ⭐/📝 Loại (Cải thiện / Tự đăng ký)
- ✓/⏳ Trạng thái (icon)

**Đã xóa:**
- ❌ Employee ID
- ❌ Ghi chú
- ❌ Thông tin chi tiết khác

### 6. **Filters đơn giản hơn**
- ❌ Xóa: Filter theo ngày (vì chỉ hiển thị 5 ngày)
- ✅ Giữ: Loại (Cải thiện/Tự đăng ký), Phòng ban, Trạng thái, Search

### 7. **Stats cập nhật**
- Tổng đăng ký
- Đã xác nhận
- Chờ xác nhận
- **Cải thiện** (thay vì "Đặc biệt")

## 🎨 Giao diện mới

### Timeline Card:
```
┌─────────────────────────────────────────────┐
│ 📅 Thứ hai, 24/4/2026        2 đăng ký     │ ← Header (xanh lá)
├─────────────────────────────────────────────┤
│ 👤  Trần Thanh Binh                    ✓   │
│     🏢 Phòng IT • 🍽️ 10002 • 📝 Tự đăng ký │
├─────────────────────────────────────────────┤
│ 👤  ADMIN                              ✓   │
│     🏢 Phòng Kế toán • 🍽️ 10002 • 📝 Tự đăng ký │
└─────────────────────────────────────────────┘
```

## 📊 Logic phân loại

```javascript
// Kiểm tra meal_type
if (meal_type.includes('Cải')) {
    → "⭐ Cải thiện" (màu xanh dương)
} else {
    → "📝 Tự đăng ký" (màu xám)
}
```

## 🔍 Filters

1. **Loại**
   - Tất cả
   - Cải thiện
   - Tự đăng ký

2. **Phòng ban**
   - Tất cả
   - Phòng IT
   - Phòng Kế toán
   - ...

3. **Trạng thái**
   - Tất cả
   - Đã xác nhận
   - Chờ xác nhận

4. **Search**
   - Tìm theo tên nhân viên

## 🚀 Cách test

### Rebuild app:
```
1. Build → Clean Project
2. Build → Rebuild Project
3. Run ▶️
```

### Test trong app:
1. Click "Nhật ký bữa ăn"
2. Xem timeline với 5 ngày gần nhất
3. Mỗi ngày được group riêng
4. Thử filters: Loại, Phòng ban, Trạng thái
5. Thử search theo tên

## 📱 Kết quả mong đợi

✅ Hiển thị 5 ngày gần nhất (mới nhất trước)
✅ Mỗi ngày là một card riêng
✅ Thông tin gọn gàng, dễ đọc
✅ "Cải thiện" vs "Tự đăng ký" rõ ràng
✅ Hover effect mượt mà
✅ Responsive và đẹp

## 🎯 Ví dụ dữ liệu

Từ API:
```json
{
  "meal_type": "Cải Thiện",
  "user_name": "Trần Thanh Binh"
}
```

Hiển thị:
```
👤 Trần Thanh Binh
🏢 Phòng IT • 🍽️ 10002 • ⭐ Cải thiện
```

---

Từ API:
```json
{
  "meal_type": "Bình Thường",
  "user_name": "ADMIN"
}
```

Hiển thị:
```
👤 ADMIN
🏢 Phòng Kế toán • 🍽️ 10002 • 📝 Tự đăng ký
```

## 💡 Lưu ý

- Timeline scroll được nếu có nhiều dữ liệu
- Hover vào meal item sẽ có hiệu ứng slide nhẹ
- Màu sắc: Xanh lá (header), Xanh dương (Cải thiện), Xám (Tự đăng ký)
- Icons giúp dễ nhận diện thông tin
