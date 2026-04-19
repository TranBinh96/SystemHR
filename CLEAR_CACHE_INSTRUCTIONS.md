# Hướng dẫn Clear Cache để thấy thay đổi

## Cách 1: Hard Refresh (Nhanh nhất)
- **Windows/Linux**: `Ctrl + Shift + R` hoặc `Ctrl + F5`
- **Mac**: `Cmd + Shift + R`

## Cách 2: Clear Cache trong Browser
### Chrome/Edge:
1. Nhấn `F12` để mở DevTools
2. Click chuột phải vào nút Refresh (⟳)
3. Chọn "Empty Cache and Hard Reload"

### Firefox:
1. Nhấn `Ctrl + Shift + Delete`
2. Chọn "Cached Web Content"
3. Click "Clear Now"

## Cách 3: Mở Incognito/Private Mode
- **Chrome/Edge**: `Ctrl + Shift + N`
- **Firefox**: `Ctrl + Shift + P`

## Cách 4: Restart Flask Server
```bash
# Stop server (Ctrl + C)
# Then restart:
python app.py
```

## Cách 5: Thêm timestamp vào URL
Thử truy cập: `http://localhost:5002/admin/stats?v=123`

## Kiểm tra xem Fixed đã hoạt động chưa:
1. Mở trang admin/stats
2. Nhấn F12 (DevTools)
3. Click vào phần "Tổng quan"
4. Xem trong tab "Styles" - phải thấy:
   - `position: fixed`
   - `top: 64px` (hoặc `top: 4rem`)
   - `z-index: 30`

Nếu không thấy các style này → Cache chưa clear!
