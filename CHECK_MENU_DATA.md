# Kiểm tra dữ liệu Menu

Có vẻ như cột "Món ăn" đang hiển thị mã nhân viên (100091) thay vì tên món ăn.

## Nguyên nhân có thể:

1. **Dữ liệu Menu bị sai**: Trong database, bảng `menu` có cột `dish_name` đang lưu mã nhân viên thay vì tên món
2. **Mapping sai**: Code đang lấy sai field

## Cách kiểm tra:

### 1. Kiểm tra dữ liệu Menu trong database:
```sql
SELECT id, date, dish_name, is_special, meal_type 
FROM menu 
WHERE date >= CURRENT_DATE 
ORDER BY date DESC 
LIMIT 10;
```

Nếu `dish_name` hiển thị số như "100091" thay vì tên món như "Cơm gà", thì dữ liệu bị sai.

### 2. Kiểm tra API response:
Mở DevTools (F12) → Network → Reload trang → Tìm request `/admin/stats/data` → Xem Response

Kiểm tra xem `meal_name` trong response có đúng không:
```json
{
  "registrations": [
    {
      "meal_name": "Cơm gà xối mỡ",  // Phải là tên món, không phải số
      "employee_id": "100091"
    }
  ]
}
```

### 3. Nếu dữ liệu Menu bị sai:
Cần sửa lại dữ liệu trong bảng `menu` hoặc kiểm tra code tạo menu xem có lỗi gì không.

## Giải pháp tạm thời:
Nếu muốn xem ngay, có thể:
1. Clear cache: Ctrl+Shift+R
2. Kiểm tra dữ liệu menu trong database
3. Sửa lại dữ liệu menu nếu cần
