# Show Permission Denied Message on Overtime Page - Implementation Summary

## Overview
Changed the overtime permission check to show a clear "Permission Denied" message on the `/overtime` page instead of redirecting to home page with a flash message.

## Problem
**Before**:
- User without permission visits `/overtime`
- Backend redirects to home page
- Shows flash message "Bạn chưa có quyền đăng ký tăng ca..."
- User confused about where they are

**After**:
- User without permission visits `/overtime`
- Page loads normally
- Shows clear permission denied message with icon
- User stays on `/overtime` page
- Better UX - user knows exactly what's wrong

## Changes Made

### 1. Backend Route `/overtime`
**File**: `app.py` (line ~2433)

**Before**:
```python
# Kiểm tra quyền đăng ký overtime
if not current_user.can_approve and not current_user.overtime_approver_id:
    flash('Bạn chưa có quyền đăng ký tăng ca. Vui lòng liên hệ admin để được cấp quyền.', 'error')
    return redirect(url_for('index'))  # Redirect to home
```

**After**:
```python
# Kiểm tra quyền đăng ký overtime
has_permission = current_user.can_approve or current_user.overtime_approver_id is not None

if not has_permission:
    # Render template with permission denied message
    return render_template('overtime.html', has_permission=False)

# ... rest of code ...

# GET request - show form
return render_template('overtime.html', has_permission=True)
```

### 2. Frontend Template `overtime.html`
**File**: `templates/overtime.html` (line ~145-255)

**Added permission check wrapper**:
```html
{% if not has_permission %}
<!-- Permission Denied Message -->
<div class="flex flex-col items-center justify-center py-16 px-4">
    <div class="w-24 h-24 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center mb-6">
        <span class="material-symbols-outlined text-red-600 dark:text-red-400 text-5xl">block</span>
    </div>
    <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-3">
        Bạn không có quyền đăng ký tăng ca
    </h2>
    <p class="text-slate-600 dark:text-slate-400 text-center mb-6 max-w-md">
        Bạn chưa được cấp quyền đăng ký tăng ca. Vui lòng liên hệ với quản trị viên (Admin) 
        hoặc quản lý của bạn để được hỗ trợ.
    </p>
    <div class="flex gap-3">
        <a href="{{ url_for('dashboard') }}" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors flex items-center gap-2">
            <span class="material-symbols-outlined text-sm">arrow_back</span>
            Quay lại trang chủ
        </a>
    </div>
</div>
{% else %}
<!-- Normal overtime form content -->
...
{% endif %}
```

## User Experience

### For Users WITHOUT Permission:
1. Click "Đăng ký tăng ca" in menu
2. Page loads with header and sidebar
3. **See clear message**:
   - 🚫 Red icon
   - "Bạn không có quyền đăng ký tăng ca"
   - Explanation text
   - "Quay lại trang chủ" button
4. No tabs, no form - just the message
5. User understands they need to contact admin

### For Users WITH Permission:
1. Click "Đăng ký tăng ca" in menu
2. Page loads normally
3. See tabs: "Đăng ký tăng ca" | "Yêu cầu của bạn"
4. See date picker and form
5. Can register overtime as usual

## Visual Design

### Permission Denied Screen:
```
┌─────────────────────────────────────┐
│  Header: Đăng ký tăng ca (OT)      │
├─────────────────────────────────────┤
│                                     │
│           🚫 (Red Circle)           │
│                                     │
│   Bạn không có quyền đăng ký tăng ca│
│                                     │
│   Bạn chưa được cấp quyền đăng ký   │
│   tăng ca. Vui lòng liên hệ với     │
│   quản trị viên...                  │
│                                     │
│   [← Quay lại trang chủ]            │
│                                     │
└─────────────────────────────────────┘
```

## Benefits

1. **Clear Communication**: User immediately knows they don't have permission
2. **No Confusion**: User stays on overtime page, not redirected elsewhere
3. **Better UX**: Professional error page instead of flash message
4. **Actionable**: Clear instruction to contact admin
5. **Consistent**: Matches the app's design language

## Permission Logic (Unchanged)

User can access overtime form if:
```python
has_permission = (
    current_user.can_approve == True  # Is manager
    OR
    current_user.overtime_approver_id IS NOT NULL  # Has assigned approver
)
```

## Testing

### Test Case 1: User WITHOUT Permission
1. Login as user EMP001 (Nguyen Van A)
2. Click "Đăng ký tăng ca" in menu
3. **Expected**:
   - ✅ Page loads (not redirected)
   - ✅ See red icon and "Bạn không có quyền" message
   - ✅ See "Quay lại trang chủ" button
   - ❌ NOT see tabs or form

### Test Case 2: User WITH Permission
1. Login as user 10002 (Hồ văn Điệp)
2. Click "Đăng ký tăng ca" in menu
3. **Expected**:
   - ✅ Page loads normally
   - ✅ See tabs and form
   - ✅ Can register overtime

### Test Case 3: Manager
1. Login as user 10009 (Đỗ Mạnh thư)
2. Click "Đăng ký tăng ca" in menu
3. **Expected**:
   - ✅ Page loads normally
   - ✅ See tabs and form
   - ✅ Can register and self-approve

## Related Files
- `app.py` - Backend route with permission check
- `templates/overtime.html` - Frontend template with conditional rendering
- `OVERTIME_PERMISSION_CHECK.md` - Backend permission documentation
- `HIDE_OVERTIME_MENU_FOR_UNAUTHORIZED.md` - Menu hiding documentation

## Status
✅ **COMPLETED** - Permission denied message now shows on overtime page

## Notes
- This is in addition to menu hiding (users without permission don't see menu item)
- This handles edge case where user accesses `/overtime` directly via URL
- Message is user-friendly and actionable
- Design matches the app's overall style
