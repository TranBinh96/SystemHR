# 📋 Hướng Dẫn Import Thực Đơn Excel - Format Mới

## 🎯 Tổng Quan

**FORMAT MỚI - ĐƠN GIẢN HÓA:**
- ✅ **Bỏ cột "Loại bữa"** - mặc định là TRƯA (lunch)
- ✅ **Ghép 2 loại món trên cùng 1 dòng** - Thường + Cải thiện
- ✅ **1 dòng Excel = 2 món ăn** cho cùng 1 ngày

## 🔽 Dropdown Excel

### Các tùy chọn
```
📊 Excel
├── 📥 Tải template Excel
│   └── "File mẫu để import thực đơn"
├── 📤 Import Excel (1 ngày)  
│   └── "Import thực đơn cho ngày được chọn"
└── 📅 Import Excel (7 ngày)
    └── "Tự động điền từ ngày hiện tại"
```

## 📊 Template Excel Mới

### Cấu trúc File
```
template_thuc_don_v3.xlsx
├── Sheet 1: "Thực đơn" (Import 1 ngày)
├── Sheet 2: "Import 7 ngày" (Import 7 ngày)
└── Sheet 3: "Hướng dẫn" (Chi tiết đầy đủ)
```

### Cột dữ liệu MỚI
| Cột | Mô tả | Bắt buộc | Ví dụ |
|-----|-------|----------|-------|
| **Ngày** | Ngày thực đơn | Có* | 2026-04-15 hoặc IGNORE |
| **Tên món (Thường)** | Món ăn bình thường | Có | Cơm gà xối mỡ |
| **Mô tả (Thường)** | Chi tiết món thường | Không | Gà chiên giòn, cơm trắng |
| **Tên món (Cải thiện)** | Món ăn đặc biệt | Có | Bún bò Huế |
| **Mô tả (Cải thiện)** | Chi tiết món cải thiện | Không | Bún bò đặc biệt |

*Cột Ngày: Bắt buộc với Import 1 ngày, ghi IGNORE với Import 7 ngày

## 🎯 Ví Dụ Excel

### Format Mới (Đơn giản)
```excel
Ngày        | Tên món (Thường) | Mô tả (Thường)      | Tên món (Cải thiện) | Mô tả (Cải thiện)
2026-04-15  | Cơm gà xối mỡ    | Gà chiên giòn       | Bún bò Huế          | Bún bò đặc biệt
2026-04-16  | Cơm sườn nướng   | Sườn nướng BBQ      | Phở bò              | Phở bò tái chín
2026-04-17  | Cơm chiên        | Cơm chiên hải sản   | Mì quảng            | Mì quảng tôm thịt
```

### Kết quả tạo ra
**Từ 1 dòng Excel → 2 món ăn:**
```
Ngày: 2026-04-15, Bữa: TRƯA
├── Món 1: Cơm gà xối mỡ (Thường) - Gà chiên giòn
└── Món 2: Bún bò Huế (Cải thiện) - Bún bò đặc biệt
```

## 🎯 Chế Độ Import

### 1. Import 1 Ngày

**Ví dụ Excel:**
```excel
Ngày        | Tên món (Thường) | Mô tả (Thường)    | Tên món (Cải thiện) | Mô tả (Cải thiện)
2026-04-15  | Cơm gà xối mỡ    | Gà chiên giòn     | Bún bò Huế          | Bún bò đặc biệt
2026-04-16  | Cơm sườn nướng   | Sườn BBQ          | Phở bò              | Phở bò tái chín
```

**Kết quả:**
- **Ngày 15/04**: 2 món (Cơm gà + Bún bò Huế)
- **Ngày 16/04**: 2 món (Cơm sườn + Phở bò)

### 2. Import 7 Ngày ⭐

**Ví dụ Excel:**
```excel
Ngày     | Tên món (Thường) | Mô tả (Thường)    | Tên món (Cải thiện) | Mô tả (Cải thiện)
IGNORE   | Cơm gà nướng     | Gà nướng mật ong  | Phở bò              | Phở bò tái chín
IGNORE   | Cơm sườn nướng   | Sườn BBQ          | Bún chả             | Bún chả Hà Nội
IGNORE   | Cơm chiên        | Cơm chiên hải sản | Mì quảng            | Mì quảng tôm thịt
IGNORE   | Cơm tấm          | Cơm tấm sườn bì   | Bún bò Huế          | Bún bò đặc biệt
IGNORE   | Cơm rang         | Cơm rang thập cẩm | Phở gà              | Phở gà ta
IGNORE   | Cơm gà roti      | Gà roti cà ri     | Bún riêu            | Bún riêu cua
IGNORE   | Cơm thịt nướng   | Thịt nướng BBQ    | Hủ tiếu             | Hủ tiếu Nam Vang
```

**Logic tự động (chọn ngày 15/04/2026 - T2):**
- **Dòng 1 → 15/04 (T2)**: Cơm gà nướng + Phở bò
- **Dòng 2 → 16/04 (T3)**: Cơm sườn nướng + Bún chả
- **Dòng 3 → 17/04 (T4)**: Cơm chiên + Mì quảng
- **Dòng 4 → 18/04 (T5)**: Cơm tấm + Bún bò Huế
- **Dòng 5 → 19/04 (T6)**: Cơm rang + Phở gà
- **Dòng 6 → 20/04 (T7)**: Cơm gà roti + Bún riêu
- **Dòng 7 → 21/04 (CN)**: Cơm thịt nướng + Hủ tiếu

## ⚙️ Tính Năng Đặc Biệt

### 1. Validation Thông Minh
```python
# Kiểm tra từng dòng
- Tên món Thường: BẮT BUỘC
- Tên món Cải thiện: BẮT BUỘC  
- Duplicate check: Không trùng tên món cùng ngày
- Date validation: YYYY-MM-DD hoặc IGNORE
```

### 2. Error Handling
```javascript
// Kết quả import
{
  "success": true,
  "message": "Đã import 14 món cho 7 ngày từ 15/04/2026 (mỗi ngày 2 món: Thường + Cải thiện)",
  "added": 14,  // 7 dòng × 2 món = 14 món
  "skipped": 2,
  "errors": ["Dòng 3: Thiếu tên món Cải thiện", "Dòng 5: Món đã tồn tại"]
}
```

### 3. UI Feedback
- **Progress**: "Đang xử lý file và tạo thực đơn 7 ngày..."
- **Success**: "Đã import 14 món cho 7 ngày (mỗi ngày 2 món)"
- **Calendar update**: Tự động cập nhật màu sắc

## 🚀 Workflow Sử Dụng

### Workflow Mới - Import 7 Ngày
1. **Tải template**: Click "Tải template Excel"
2. **Chọn sheet**: "Import 7 ngày"
3. **Điền dữ liệu**: 
   ```
   Dòng 1: IGNORE | Cơm gà | Gà chiên | Phở bò | Phở đặc biệt
   Dòng 2: IGNORE | Cơm sườn | Sườn BBQ | Bún chả | Bún chả HN
   ...7 dòng
   ```
4. **Chọn ngày**: Click ngày bắt đầu (T2)
5. **Import**: Click "Import Excel (7 ngày)"
6. **Kết quả**: 7 ngày × 2 món = 14 món tự động

## 💡 So Sánh Format

### Format Cũ (Phức tạp)
```excel
Ngày        | Loại bữa | Tên món      | Mô tả        | Cải thiện | Bình thường
2026-04-15  | lunch    | Cơm gà       | Gà chiên     | FALSE     | TRUE
2026-04-15  | lunch    | Bún bò Huế   | Bún đặc biệt | TRUE      | FALSE
```
**→ 2 dòng = 2 món**

### Format Mới (Đơn giản) ⭐
```excel
Ngày        | Tên món (Thường) | Mô tả (Thường) | Tên món (Cải thiện) | Mô tả (Cải thiện)
2026-04-15  | Cơm gà           | Gà chiên       | Bún bò Huế          | Bún đặc biệt
```
**→ 1 dòng = 2 món**

## ⚠️ Lưu Ý Quan Trọng

### Quy tắc mới
- **1 dòng Excel = 2 món ăn** (Thường + Cải thiện)
- **Cả 2 món đều cho bữa TRƯA** (lunch)
- **Cả 2 tên món đều BẮT BUỘC**
- **Mô tả có thể để trống**
- **Import 7 ngày**: 7 dòng = 7 ngày × 2 món = 14 món

### Best Practices
- **Chuẩn bị Excel**: Điền đầy đủ 2 tên món mỗi dòng
- **Test nhỏ**: Import 1-2 dòng trước để test
- **Backup**: Luôn backup trước khi import
- **Kiểm tra**: Xem calendar màu xanh = thành công

---

**🎉 Format mới giúp giảm 50% công việc nhập liệu! 1 dòng = 2 món ăn!**