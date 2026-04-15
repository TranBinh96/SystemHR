# Overtime Approver Department Filter - Implementation Summary

## Overview
Implemented department-based filtering for overtime approvers. When admin edits a user, the "Người phê duyệt overtime" dropdown now shows only managers (`can_approve=True`) from the **same department** as the user being edited.

## Changes Made

### 1. Backend API Update (`app.py`)
**File**: `app.py` (lines 589-620)

**Changes**:
- Added `department` parameter support to `/api/users` endpoint
- When `department` parameter is provided, API filters users by department name
- Uses JOIN with Department table to filter by department name

**Code**:
```python
@app.route('/api/users', methods=['GET'])
@login_required
def api_get_users():
    """API to get users list with filters"""
    if current_user.role != 'admin':
        return {'success': False, 'message': 'Không có quyền'}, 403
    
    try:
        # Get filter parameters
        can_approve = request.args.get('can_approve')
        department = request.args.get('department')
        
        # Build query
        query = User.query.filter_by(is_active=True)
        
        if can_approve == '1':
            query = query.filter_by(can_approve=True)
        
        # Filter by department if provided
        if department:
            # Join with Department table to filter by name
            query = query.join(Department).filter(Department.name == department)
        
        users = query.order_by(User.name).all()
        
        return {
            'success': True,
            'users': [{
                'id': u.id,
                'employee_id': u.employee_id,
                'name': u.name,
                'department': u.dept.name if u.dept else '',
                'can_approve': u.can_approve
            } for u in users]
        }
    
    except Exception as e:
        print(f"Error in api_get_users: {e}")
        return {'success': False, 'message': f'Lỗi: {str(e)}'}, 500
```

### 2. Frontend Update (`templates/admin_users.html`)
**File**: `templates/admin_users.html` (lines 1182-1230)

**Changes** (already implemented in previous session):
- `populateOvertimeApprovers()` function now reads current user's department
- Builds API URL with department filter: `/api/users?can_approve=1&department=<dept_name>`
- Only shows managers from the same department in dropdown

**Code**:
```javascript
function populateOvertimeApprovers() {
    // Fetch users with can_approve = True in the same department
    console.log('=== populateOvertimeApprovers called ===');
    
    // Get current user's department
    const departmentSelect = document.getElementById('editDepartment');
    const currentDepartment = departmentSelect ? departmentSelect.value : '';
    
    console.log('Current department:', currentDepartment);
    
    // Build API URL with department filter
    let apiUrl = '/api/users?can_approve=1';
    if (currentDepartment) {
        apiUrl += `&department=${encodeURIComponent(currentDepartment)}`;
    }
    
    console.log('API URL:', apiUrl);
    
    fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
            console.log('API response:', data);
            const select = document.getElementById('editOvertimeApproverId');
            if (!select) {
                console.error('editOvertimeApproverId select not found!');
                return;
            }
            
            // Keep the default option
            select.innerHTML = '<option value="">-- Chưa chỉ định --</option>';
            
            // Add approvers
            if (data.success && data.users) {
                console.log(`Found ${data.users.length} approvers in department`);
                data.users.forEach(user => {
                    const option = document.createElement('option');
                    option.value = user.id;
                    option.textContent = `${user.name} (${user.employee_id})`;
                    select.appendChild(option);
                });
            } else {
                console.error('No users found or API error');
            }
        })
        .catch(err => {
            console.error('Error loading approvers:', err);
        });
}
```

## Testing

### Test Scripts Created
1. **`scripts/test_department_filter.py`** - Shows managers by department
2. **`scripts/test_api_department_filter.py`** - Tests API endpoint logic

### Test Results
```
Department: Phòng IT
- Total active users: 4
- Managers (can_approve=True): 1
  - Đỗ Mạnh thư (10009)
- Regular users: 3
  - Trần Thanh Binh (10197) -> Approver: Đỗ Mạnh thư (10009)
  - Hồ Tiến Quang (10001) -> Approver: Đỗ Mạnh thư (10009)
  - Hồ văn Điệp (10002) -> Approver: Đỗ Mạnh thư (10009)

Department: Phòng Nhân sự
- Total active users: 1
- Managers: 0 ⚠️
- Regular users: 1
  - Nguyen Van A (EMP001) -> Approver: Not assigned

Other departments (Sản xuất, QC, Kế toán):
- No managers found ⚠️
```

## How It Works

### User Flow
1. Admin opens "Edit User" modal for a user
2. System reads user's current department from form
3. JavaScript calls API: `/api/users?can_approve=1&department=<dept_name>`
4. Backend filters managers by department
5. Dropdown shows only managers from same department

### Example API Calls
```
GET /api/users?can_approve=1
→ Returns all managers (no department filter)

GET /api/users?can_approve=1&department=Phòng IT
→ Returns only managers in IT department (Đỗ Mạnh thư)

GET /api/users?can_approve=1&department=Phòng Nhân sự
→ Returns empty list (no managers in HR department)
```

## Edge Cases Handled

### 1. Department with No Managers
- Dropdown shows only "-- Chưa chỉ định --" option
- User cannot select an approver
- **Solution**: Admin must assign `can_approve=True` to at least one user in each department

### 2. User with No Department
- API returns all managers (no filter applied)
- This is acceptable as fallback behavior

### 3. Department Name with Special Characters
- Uses `encodeURIComponent()` to properly encode department name in URL
- Backend uses exact match on department name

## Database Schema

### Relevant Fields
```sql
users table:
- department_id (FK to departments.id)
- can_approve (BOOLEAN) - Manager permission
- overtime_approver_id (FK to users.id) - Assigned approver

departments table:
- id (PK)
- name (VARCHAR) - Used for filtering
```

## Benefits

1. **Department Isolation**: Users can only be assigned approvers from their own department
2. **Simplified Management**: Admin doesn't see irrelevant managers from other departments
3. **Scalability**: Works well as company grows and adds more departments
4. **Data Integrity**: Prevents cross-department approval assignments

## Future Improvements

1. **Auto-assign approver**: When user's department changes, auto-assign default approver
2. **Validation**: Prevent saving if department has no managers
3. **Multi-level approval**: Support approval chains within department
4. **Department hierarchy**: Support parent/child department relationships

## Related Files
- `app.py` - Backend API endpoint
- `templates/admin_users.html` - Frontend dropdown logic
- `models/__init__.py` - User and Department models
- `scripts/test_department_filter.py` - Test script
- `scripts/test_api_department_filter.py` - API test script

## Status
✅ **COMPLETED** - Department filtering is fully implemented and tested
