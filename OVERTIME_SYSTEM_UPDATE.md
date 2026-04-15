# Overtime Permission System - Implementation Complete

## Overview
Implemented a complete overtime permission system where users can register overtime requests, and designated approvers can edit and approve those requests.

## Database Changes (Already Completed)
- Added `users.can_register_overtime` (TINYINT) - Permission to register overtime
- Added `users.overtime_approver_id` (INTEGER, FK to users.id) - Assigned approver
- Added `overtime_requests.number_of_people` (INTEGER) - Number of people registering
- Made `overtime_requests.start_time`, `end_time`, `total_hours` nullable (legacy fields)

## Backend Implementation (Already Completed)

### Routes Updated:
1. **POST `/overtime`** - User registration
   - Checks `can_register_overtime` permission
   - Gets `number_of_people` and `notes` from form
   - Auto-assigns `manager_id` from user's `overtime_approver_id`

2. **GET `/manager/overtime-requests`** - Get requests for approval
   - Returns requests where `manager_id` = current_user.id
   - Returns `number_of_people` instead of hours

3. **POST `/manager/overtime-requests/<id>/update`** - NEW ROUTE
   - Allows approver to edit `number_of_people` and `notes` before approval
   - Only works for pending requests
   - Only accessible by assigned approver or admin

4. **POST `/manager/overtime-requests/<id>/approve`** - Approve request
   - Existing logic maintained

## Frontend Implementation (Just Completed)

### Manager Approval Page (`templates/manager_overtime_approvals.html`)

#### Changes Made:

1. **Mobile Card View:**
   - Removed: Time display (start_time - end_time)
   - Removed: Total hours badge
   - Added: "Số người" (Number of people) badge with group icon
   - Added: "Sửa" (Edit) button before "Duyệt" and "Từ chối" buttons
   - Layout: 3 buttons in a row (Edit, Approve, Reject)

2. **Desktop Table View:**
   - Removed columns: "Thời gian" (Time), "Tổng giờ" (Total hours)
   - Added column: "Số người" (Number of people) with group icon badge
   - Renamed column: "Lý do" → "Ghi chú" (Notes)
   - Added: Edit button (blue) before Approve and Reject buttons

3. **Edit Modal:**
   - New modal for editing overtime requests
   - Fields:
     - "Số người đăng ký" (Number input, min=1, max=999)
     - "Ghi chú cụ thể" (Textarea, 4 rows)
   - Buttons: "Hủy" (Cancel), "Lưu thay đổi" (Save changes)

4. **JavaScript Functions Added:**
   - `openEditModal(requestId, numberOfPeople, notes)` - Opens edit modal with current values
   - `closeEditModal()` - Closes edit modal
   - `saveEdit()` - Saves changes via `/manager/overtime-requests/<id>/update` endpoint

## User Flow

### Registration Flow:
1. User with `can_register_overtime = True` visits `/overtime`
2. User selects date, enters number of people, and notes
3. System auto-assigns approver from `overtime_approver_id`
4. Request created with status = 'pending'

### Approval Flow:
1. Approver visits `/manager/overtime-approvals`
2. Sees list of pending requests with:
   - Employee name and ID
   - Date
   - Number of people
   - Notes
3. Approver can:
   - **Edit**: Click "Sửa" to modify number of people and notes
   - **Approve**: Click "Duyệt" to approve request
   - **Reject**: Click "Từ chối" to reject request

### Edit Flow:
1. Approver clicks "Sửa" (Edit) button
2. Modal opens with current values
3. Approver modifies number of people and/or notes
4. Clicks "Lưu thay đổi" (Save changes)
5. System updates request via `/manager/overtime-requests/<id>/update`
6. Modal closes and list refreshes

## Next Steps (To Be Implemented)

### Admin Users Page:
- Add UI to set `can_register_overtime` permission
- Add UI to assign `overtime_approver_id` (dropdown of users with `can_approve = True`)
- Update user edit form in `templates/admin_users.html`

### Testing:
1. Test user registration with permission check
2. Test auto-assignment of approver
3. Test edit functionality (only pending requests)
4. Test approval after editing
5. Test authorization (only assigned approver can edit)

## Files Modified
- `templates/manager_overtime_approvals.html` - Complete UI overhaul
- `models/__init__.py` - Database schema (already done)
- `app.py` - Backend routes (already done)
- `scripts/update_user_overtime_permissions.py` - Migration script (already executed)

## Technical Notes
- Legacy fields (`start_time`, `end_time`, `total_hours`) kept for backward compatibility
- All existing approval logic maintained
- Edit functionality only available for pending requests
- Authorization checks in place (approver or admin only)
