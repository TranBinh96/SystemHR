# Remove "Quyền đăng ký" Field from Edit Form - Implementation Summary

## Overview
Removed the "Quyền đăng ký" (can_register) field from the user edit form in admin panel. This field is no longer relevant for overtime registration permissions.

## Reason for Removal
- **Old logic**: `can_register` controlled both meal AND overtime registration
- **New logic**: 
  - Meal registration: Still uses `can_register` field (kept in database)
  - Overtime registration: Uses `can_approve` OR `overtime_approver_id`
- **Result**: `can_register` field in edit form was confusing and unnecessary

## Changes Made

### 1. Removed HTML Field from Edit Modal
**File**: `templates/admin_users.html` (line ~726-751)

**Before** (3 columns):
```html
<!-- Row 3: Quyền phê duyệt + Quyền đăng ký + Quyền -->
<div class="grid grid-cols-3 gap-4">
    <div><!-- Quyền phê duyệt --></div>
    <div><!-- Quyền đăng ký --></div>  ← REMOVED
    <div><!-- Quyền --></div>
</div>
```

**After** (2 columns):
```html
<!-- Row 3: Quyền phê duyệt + Quyền -->
<div class="grid grid-cols-2 gap-4">
    <div><!-- Quyền phê duyệt --></div>
    <div><!-- Quyền --></div>
</div>
```

### 2. Removed JavaScript References

#### 2.1 In `openEditModal()` Function
**Removed**:
```javascript
const canRegisterSelect = document.getElementById('editCanRegister');

if (canRegisterSelect) {
    canRegisterSelect.value = canRegister ? '1' : '0';
}
```

#### 2.2 In `originalEditValues` Object
**Removed**:
```javascript
window.originalEditValues = {
    // ...
    canRegister: canRegister ? '1' : '0',  ← REMOVED
    // ...
};
```

#### 2.3 In `checkFormChanges()` Function
**Removed**:
```javascript
const currentValues = {
    // ...
    canRegister: document.getElementById('editCanRegister').value,  ← REMOVED
    // ...
};

const hasChanges = 
    // ...
    currentValues.canRegister !== window.originalEditValues.canRegister ||  ← REMOVED
    // ...
```

#### 2.4 In `saveUserEdit()` Function - FormData
**Removed**:
```javascript
formData.append('can_register', document.getElementById('editCanRegister').value === '1');
```

#### 2.5 In `saveUserEdit()` Function - JSON Data
**Removed**:
```javascript
const data = {
    // ...
    can_register: document.getElementById('editCanRegister').value === '1',  ← REMOVED
    // ...
};
```

## Database Field Status
**IMPORTANT**: The `can_register` field is **NOT removed from database**. It is still used for:
- Meal registration permissions
- Backend logic in `/meals` route

Only the UI field in admin edit form was removed.

## Current Edit Form Layout

### Row 1: Mã nhân viên + Họ và tên
### Row 2: Phòng ban + Cấp bậc
### Row 3: Quyền phê duyệt + Quyền (2 columns)
- **Quyền phê duyệt**: Manager permission (can_approve)
- **Quyền**: User role (user/admin)

### Row 4: Người phê duyệt overtime + Trạng thái (2 columns)
- **Người phê duyệt overtime**: Assigned approver for overtime
- **Trạng thái**: Work status (working/resigned/etc)

### Row 5: Mật khẩu
### Row 6: Ảnh đại diện

## Benefits

1. **Cleaner UI**: Removed confusing field that wasn't used for overtime
2. **Less Confusion**: Admins won't accidentally change meal permissions when managing overtime
3. **Better Layout**: Form now has consistent 2-column layout
4. **Focused Permissions**: Only show overtime-related permissions in edit form

## Overtime Permission Logic (Unchanged)

User can register overtime if:
```python
can_register_overtime = (
    user.can_approve == True  # Is manager
    OR
    user.overtime_approver_id IS NOT NULL  # Has assigned approver
)
```

## Meal Permission Logic (Unchanged)

User can register meals if:
```python
can_register_meals = user.can_register == True
```

## Testing

To verify the changes:

1. Login as admin
2. Go to "Quản lý người dùng"
3. Click edit on any user
4. **Expected**: 
   - ✅ See "Quyền phê duyệt" field
   - ✅ See "Quyền" field
   - ❌ NOT see "Quyền đăng ký" field
   - ✅ See "Người phê duyệt overtime" field
5. Form should have clean 2-column layout

## Related Files
- `templates/admin_users.html` - Edit form UI
- `app.py` - Backend routes (unchanged)
- `models/__init__.py` - Database models (unchanged)

## Status
✅ **COMPLETED** - "Quyền đăng ký" field removed from edit form

## Notes
- Field removed from UI only, not from database
- `can_register` still used for meal registration
- Overtime permissions controlled by `can_approve` and `overtime_approver_id`
- No backend changes required
