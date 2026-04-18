# Hướng dẫn xóa trường Position trong admin_users.html

File `templates/admin_users.html` còn rất nhiều tham chiếu đến position cần xóa thủ công.

## Các phần cần xóa:

### 1. Xóa cột "Chức vụ" trong table header (dòng ~353)
```html
<!-- XÓA DÒNG NÀY -->
<th class="px-3 py-3 text-left text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">{{ t.position }}</th>
```

### 2. Xóa data-position trong các thẻ <tr> (nhiều chỗ)
```html
<!-- XÓA DÒNG NÀY -->
data-position="{{ user.position_id or '' }}"
```

### 3. Xóa tham số position trong hàm selectUser() và openEditModal()
Tìm tất cả các dòng có:
```javascript
onclick="selectUser(..., '{{ user.position_id or '' }}', ...)"
onclick="openEditModal(..., '{{ user.position_id or '' }}', ...)"
```

Xóa tham số `'{{ user.position_id or '' }}'` và cập nhật lại thứ tự tham số.

### 4. Xóa trường "Cấp bậc" trong Edit Modal (dòng ~710-718)
```html
<!-- XÓA TOÀN BỘ BLOCK NÀY -->
<div>
    <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">
        Cấp bậc
    </label>
    <select id="editPosition" 
            class="w-full px-3 py-2.5 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            onchange="checkFormChanges()">
        <option value="">Chọn cấp bậc</option>
        {% for pos in positions %}
        <option value="{{ pos.id }}">{{ pos.name }}{% if pos.description %}/{{ pos.description }}{% endif %}</option>
        {% endfor %}
    </select>
</div>
```

### 5. Cập nhật hàm openEditModal() trong JavaScript (dòng ~966)
```javascript
// TỪ:
window.openEditModal = function(userId, employeeId, name, department, position, role, isActive, avatarUrl, canApprove, canRegister, workStatus) {

// THÀNH:
window.openEditModal = function(userId, employeeId, name, department, role, isActive, avatarUrl, canApprove, canRegister, workStatus) {
```

Xóa tất cả các dòng liên quan đến position trong hàm này:
- `const posSelect = document.getElementById('editPosition');`
- `posSelect.value = position || '';`
- `position: position || '',` trong originalEditValues
- `position: document.getElementById('editPosition').value,` trong checkFormChanges

### 6. Xóa hàm populatePositionList() (dòng ~1161)
```javascript
// XÓA TOÀN BỘ HÀM NÀY
function populatePositionList() {
    // Position dropdown is now populated from server-side template
    // No need for dynamic population since we use server-side template for positions
}
```

### 7. Xóa hàm populateAddPositionList() (dòng ~1307)
```javascript
// XÓA TOÀN BỘ HÀM NÀY
function populateAddPositionList() {
    // Position dropdown is now populated from server-side template
    // No need for dynamic population since we use server-side template for positions
}
```

### 8. Xóa trường position trong Add Modal
Tìm và xóa:
```html
<div>
    <label>Cấp bậc *</label>
    <select id="addPosition" required>
        <option value="">Chọn cấp bậc</option>
        {% for pos in positions %}
        <option value="{{ pos.id }}">{{ pos.name }}</option>
        {% endfor %}
    </select>
</div>
```

### 9. Xóa trong hàm saveUser() (dòng ~1322)
```javascript
// XÓA DÒNG NÀY
formData.append('position', document.getElementById('addPosition').value);
```

### 10. Xóa trong hàm saveEditUser()
```javascript
// XÓA DÒNG NÀY
formData.append('position', document.getElementById('editPosition').value);
```

## Cách nhanh nhất:

Sử dụng Find & Replace trong editor:

1. **Xóa data-position:**
   - Find: `data-position="[^"]*"\s*`
   - Replace: (để trống)

2. **Xóa tham chiếu position trong onclick:**
   - Tìm thủ công và xóa tham số position

3. **Xóa các block HTML có "Cấp bậc" hoặc "position"**

Sau khi xóa xong, khởi động lại Flask app!
