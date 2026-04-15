# Overtime Permission Check - Implementation Summary

## Overview
Implemented permission check to prevent users without overtime registration rights from accessing the overtime registration page.

## Permission Logic

### Who CAN access `/overtime`:
1. **Managers** (`can_approve = True`): Can self-approve their overtime requests
2. **Regular users** with `overtime_approver_id` assigned: Need approval from assigned manager

### Who CANNOT access `/overtime`:
- **Regular users** without `overtime_approver_id`: No approver assigned

## Changes Made

### 1. Route `/overtime` - Main Page
**File**: `app.py` (line ~2433)

**Added permission check at the beginning**:
```python
@app.route('/overtime', methods=['GET', 'POST'])
@login_required
def overtime():
    # Kiểm tra quyền đăng ký overtime
    if not current_user.can_approve and not current_user.overtime_approver_id:
        flash('Bạn chưa có quyền đăng ký tăng ca. Vui lòng liên hệ admin để được cấp quyền.', 'error')
        return redirect(url_for('index'))
    
    # ... rest of the code
```

**Behavior**:
- If user has no permission → Show error message and redirect to home page
- If user has permission → Show overtime registration form

### 2. Route `/overtime/my-requests` - Get User's Requests
**File**: `app.py` (line ~2516)

**Added permission check**:
```python
@app.route('/overtime/my-requests')
@login_required
def get_my_overtime_requests():
    """Get current user's overtime requests"""
    # Kiểm tra quyền đăng ký overtime
    if not current_user.can_approve and not current_user.overtime_approver_id:
        return {'success': False, 'message': 'Bạn chưa có quyền đăng ký tăng ca'}, 403
    
    # ... rest of the code
```

**Behavior**:
- If user has no permission → Return 403 Forbidden
- If user has permission → Return list of their overtime requests

### 3. Route `/overtime/<id>/cancel` - Cancel Request
**File**: `app.py` (line ~2544)

**Added permission check**:
```python
@app.route('/overtime/<int:request_id>/cancel', methods=['POST'])
@login_required
def cancel_overtime_request(request_id):
    """Cancel overtime request (only if pending)"""
    # Kiểm tra quyền đăng ký overtime
    if not current_user.can_approve and not current_user.overtime_approver_id:
        return {'success': False, 'message': 'Bạn chưa có quyền đăng ký tăng ca'}, 403
    
    # ... rest of the code
```

**Behavior**:
- If user has no permission → Return 403 Forbidden
- If user has permission → Allow canceling their pending requests

## Test Results

### Current Status (from test script)
```
Total active users: 7
Can access: 5 (71%)
Cannot access: 2 (28%)
```

### Users WITH Permission (5 users):
1. **Administrator (ADMIN)** - Manager (self-approve)
2. **Trần Thanh Binh (10197)** - Phòng IT - Has approver (ID: 8)
3. **Hồ Tiến Quang (10001)** - Phòng IT - Has approver (ID: 8)
4. **Hồ văn Điệp (10002)** - Phòng IT - Has approver (ID: 8)
5. **Đỗ Mạnh thư (10009)** - Phòng IT - Manager (self-approve)

### Users WITHOUT Permission (2 users):
1. **Nguyen Van A (EMP001)** - Phòng Nhân sự - No approver assigned
2. **ADMIN (100023)** - Phòng Kế toán - No approver assigned

## User Experience

### For Users WITH Permission:
1. Click "Đăng ký tăng ca" in menu
2. See overtime registration form
3. Can submit overtime requests
4. Can view their request history
5. Can cancel pending requests

### For Users WITHOUT Permission:
1. Click "Đăng ký tăng ca" in menu
2. See error message: "Bạn chưa có quyền đăng ký tăng ca. Vui lòng liên hệ admin để được cấp quyền."
3. Redirected to home page
4. Cannot access any overtime-related APIs

## Admin Actions Required

For users without permission, admin needs to:

### Option 1: Assign Overtime Approver
1. Go to "Quản lý người dùng"
2. Edit user profile
3. Select "Người phê duyệt overtime" from dropdown
4. Save changes

### Option 2: Grant Manager Permission
1. Go to "Quản lý người dùng"
2. Edit user profile
3. Set "Quyền phê duyệt" = "Có" (can_approve = True)
4. Save changes

## Database Fields

### User Table
```sql
can_approve BOOLEAN DEFAULT FALSE
  - True: User is manager, can self-approve
  - False: User is regular employee

overtime_approver_id INT NULL
  - NULL: User cannot register overtime
  - <user_id>: User can register, needs approval from this manager
```

## Security Benefits

1. **Access Control**: Only authorized users can access overtime registration
2. **Data Integrity**: Prevents unauthorized overtime requests
3. **Clear Workflow**: Users know immediately if they don't have permission
4. **Admin Visibility**: Easy to identify users without permission via test script

## Test Scripts

### 1. `scripts/test_overtime_permission.py`
Shows which users can and cannot access overtime registration

**Usage**:
```bash
python scripts/test_overtime_permission.py
```

**Output**:
- List of users with permission
- List of users without permission
- Summary statistics

### 2. `scripts/test_overtime_submission.py`
Tests overtime submission logic for different user types

**Usage**:
```bash
python scripts/test_overtime_submission.py
```

## Related Files
- `app.py` - Routes with permission checks
- `models/__init__.py` - User model with permission fields
- `scripts/test_overtime_permission.py` - Permission test script
- `scripts/test_overtime_submission.py` - Submission test script

## Status
✅ **COMPLETED** - Permission check is fully implemented and tested

## Next Steps (Optional)
1. Add visual indicator in menu to hide "Đăng ký tăng ca" for users without permission
2. Create admin dashboard to show users without overtime permission
3. Add bulk assign approver feature for admin
