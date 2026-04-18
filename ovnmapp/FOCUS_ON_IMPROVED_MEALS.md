# TẬP TRUNG VÀO SUẤT ĂN CẢI THIỆN

## ✅ Thay đổi mới

### 🎯 Logic chính:

1. **Suất Thường** = Tự động đăng ký (không cần quét barcode)
2. **Suất Cải thiện** = Cần quét barcode để xác nhận
3. **Mặc định chỉ hiển thị suất Cải thiện** trong danh sách

### 📊 Header mỗi ngày hiển thị:

```
┌─────────────────────────────────────────────────────────┐
│ 📅 Thứ sáu, 24/4/2026                                   │
│                                                          │
│ 📋 Tổng: 10  ⭐ Cải thiện: 3  📝 Thường: 7              │
│ ✓ Đã xác nhận: 1  ⏳ Chờ xác nhận: 2                   │
└─────────────────────────────────────────────────────────┘
```

**Thống kê mỗi ngày:**
- 📋 **Tổng**: Tổng số đăng ký (Cải thiện + Thường)
- ⭐ **Cải thiện**: Số suất cải thiện (highlight)
- 📝 **Thường**: Số suất thường (đã tự động đăng ký)
- ✓ **Đã xác nhận**: Số suất cải thiện đã quét barcode
- ⏳ **Chờ xác nhận**: Số suất cải thiện chưa quét

### 📋 Danh sách hiển thị:

**CHỈ HIỂN THỊ SUẤT CẢI THIỆN** vì:
- Suất Thường đã tự động đăng ký → Không cần theo dõi
- Suất Cải thiện cần quét barcode → Cần theo dõi trạng thái

Nếu ngày nào không có suất Cải thiện:
```
┌─────────────────────────────────────┐
│            ✓                        │
│  Không có suất cải thiện            │
│  Tất cả 7 suất thường đã được       │
│  tự động đăng ký                    │
└─────────────────────────────────────┘
```

### 🔍 Filter mặc định:

**"Hiển thị: Chỉ Cải thiện"** được chọn sẵn

Options:
- **Chỉ Cải thiện** (mặc định) ← Tập trung vào suất cần xác nhận
- Tất cả
- Chỉ Tự đăng ký

## 🎨 Giao diện mới

### Ví dụ 1: Ngày có suất Cải thiện

```
┌──────────────────────────────────────────────────────┐
│ 📅 Thứ sáu, 24/4/2026                                │
│ 📋 Tổng: 10  ⭐ Cải thiện: 3  📝 Thường: 7           │
│ ✓ Đã xác nhận: 1  ⏳ Chờ xác nhận: 2                │
├──────────────────────────────────────────────────────┤
│ 👤 Nguyễn Văn A                                 ✓   │
│    🏢 Phòng IT • 🍽️ Cơm gà • ⭐ Cải thiện           │
├──────────────────────────────────────────────────────┤
│ 👤 Trần Thị B                                   ⏳   │
│    🏢 Phòng Kế toán • 🍽️ Cơm sườn • ⭐ Cải thiện   │
├──────────────────────────────────────────────────────┤
│ 👤 Lê Văn C                                     ⏳   │
│    🏢 Phòng IT • 🍽️ Cơm gà • ⭐ Cải thiện           │
└──────────────────────────────────────────────────────┘
```

### Ví dụ 2: Ngày không có suất Cải thiện

```
┌──────────────────────────────────────────────────────┐
│ 📅 Thứ năm, 23/4/2026                                │
│ 📋 Tổng: 8  ⭐ Cải thiện: 0  📝 Thường: 8            │
│ ✓ Đã xác nhận: 0  ⏳ Chờ xác nhận: 0                │
├──────────────────────────────────────────────────────┤
│                      ✓                               │
│         Không có suất cải thiện                      │
│    Tất cả 8 suất thường đã được tự động đăng ký     │
└──────────────────────────────────────────────────────┘
```

## 📊 Stats tổng quan (top)

- 📋 **Tổng đăng ký**: Tất cả đăng ký (Cải thiện + Thường)
- ✓ **Đã xác nhận**: Số suất đã xác nhận
- ⏳ **Chờ xác nhận**: Số suất chưa xác nhận
- ⭐ **Cải thiện**: Tổng số suất cải thiện (trong tất cả dữ liệu)

## 🔄 Workflow

### Suất Thường:
1. Nhân viên đăng ký online
2. ✅ Tự động được đánh dấu "đã đăng ký"
3. Không cần quét barcode
4. Không hiển thị trong danh sách (vì đã xong)

### Suất Cải thiện:
1. Nhân viên đăng ký online
2. ⏳ Trạng thái "Chờ xác nhận"
3. **Cần quét barcode** để xác nhận
4. ✓ Sau khi quét → "Đã xác nhận"
5. Hiển thị trong danh sách để theo dõi

## 🚀 Cách test

### Rebuild:
```
1. Build → Clean Project
2. Build → Rebuild Project
3. Run ▶️
```

### Test:
1. Click "Nhật ký bữa ăn"
2. Xem header mỗi ngày có thống kê đầy đủ
3. Danh sách chỉ hiển thị suất Cải thiện
4. Filter mặc định: "Chỉ Cải thiện"
5. Thử đổi filter sang "Tất cả" để xem cả Thường

## 💡 Lợi ích

✅ **Tập trung**: Chỉ hiển thị suất cần theo dõi (Cải thiện)
✅ **Rõ ràng**: Thống kê đầy đủ ở header mỗi ngày
✅ **Hiệu quả**: Không lãng phí thời gian xem suất đã tự động đăng ký
✅ **Trực quan**: Dễ thấy suất nào cần quét barcode

## 🎯 Kết quả mong đợi

Sau khi rebuild:
- ✅ Header mỗi ngày hiển thị: Tổng, Cải thiện, Thường, Đã xác nhận, Chờ xác nhận
- ✅ Danh sách chỉ hiển thị suất Cải thiện (mặc định)
- ✅ Ngày không có suất Cải thiện → Hiển thị thông báo
- ✅ Filter "Chỉ Cải thiện" được chọn sẵn
- ✅ Có thể đổi sang "Tất cả" để xem cả Thường
