# Hướng dẫn tối ưu giao diện

## Đã tối ưu:

### 1. **Content Area**
- Padding: 40px → 24px
- Gap: 32px → 24px
- Khi collapsed: 24px → 20px

### 2. **Pickup Stats (Đã lấy / Còn lại)**
- Padding: 10px 20px → 8px 16px
- Gap: 12px → 10px
- Margin-top: 20px → 12px
- Font label: 13px → 12px
- Font value: 28px → 24px

## Cần tối ưu thêm:

### Trong file `app/src/main/assets/qr-scanner.html`, tìm và thay đổi:

1. **Scanner Card** (dòng ~200):
```css
.scanner-card {
    padding: 32px; /* Đổi thành 20px */
}
```

2. **Info Card** (dòng ~400):
```css
.info-card {
    padding: 32px; /* Đổi thành 20px */
}
```

3. **Meal Name** (dòng ~450):
```css
.meal-name {
    font-size: 28px; /* Đổi thành 24px */
    margin-bottom: 8px; /* Đổi thành 6px */
}
```

4. **Meal Image** (dòng ~440):
```css
.meal-image {
    margin-bottom: 24px; /* Đổi thành 12px */
    font-size: 64px; /* Đổi thành 48px */
}
```

5. **Employee Card** (dòng ~500):
```css
.employee-card {
    padding: 24px; /* Đổi thành 16px */
    margin-bottom: 24px; /* Đổi thành 16px */
}
```

6. **Employee Avatar** (dòng ~510):
```css
.employee-avatar {
    width: 56px; /* Đổi thành 48px */
    height: 56px; /* Đổi thành 48px */
}
```

7. **Details Grid** (dòng ~550):
```css
.details-grid {
    gap: 16px; /* Đổi thành 12px */
    margin-bottom: 32px; /* Đổi thành 16px */
}
```

8. **Detail Item** (dòng ~560):
```css
.detail-item {
    padding: 20px; /* Đổi thành 14px */
}
```

9. **Action Buttons** (dòng ~600):
```css
.btn {
    padding: 16px; /* Đổi thành 14px */
    font-size: 15px; /* Đổi thành 14px */
}
```

10. **History Card** (dòng ~650):
```css
.history-card {
    padding: 24px; /* Đổi thành 16px */
}
```

11. **Info Header** (dòng ~420):
```css
.info-header {
    margin-bottom: 32px; /* Đổi thành 16px */
}
```

12. **Meal Info** (dòng ~460):
```css
.meal-info {
    margin-bottom: 32px; /* Đổi thành 16px */
}
```

## Kết quả sau khi tối ưu:

✅ Tất cả thông tin hiển thị vừa 1 màn hình
✅ Không cần scroll
✅ Vẫn giữ được tính thẩm mỹ
✅ Dễ đọc và sử dụng

## Rebuild:
1. Build > Clean Project
2. Build > Rebuild Project
3. Run (▶️)
