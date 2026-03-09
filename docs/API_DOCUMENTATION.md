# API Documentation - OKI Vietnam HR System

## Base URL
```
http://localhost:5000/api
```

## Authentication

Hệ thống sử dụng JWT (JSON Web Token) Bearer authentication.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Authentication Endpoints

### 1. Login
**POST** `/api/auth/login`

Đăng nhập và nhận JWT tokens.

**Request Body:**
```json
{
  "employee_id": "EMP001",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "user": {
    "id": 1,
    "employee_id": "EMP001",
    "name": "Nguyen Van A",
    "email": "nguyenvana@okivietnam.com",
    "department": "production",
    "role": "user"
  }
}
```

**Error Responses:**
- `400`: Missing employee_id or password
- `401`: Invalid credentials
- `403`: Account is disabled

---

### 2. Refresh Token
**POST** `/api/auth/refresh`

Làm mới access token bằng refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

---

### 3. Get Current User
**GET** `/api/auth/me`

Lấy thông tin user hiện tại từ token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "employee_id": "EMP001",
  "name": "Nguyen Van A",
  "email": "nguyenvana@okivietnam.com",
  "department": "production",
  "role": "user",
  "is_active": true,
  "created_at": "2026-03-04T15:39:42.276657"
}
```

---

### 4. Register
**POST** `/api/auth/register`

Đăng ký tài khoản mới.

**Request Body:**
```json
{
  "employee_id": "EMP002",
  "name": "Tran Thi B",
  "email": "tranthib@okivietnam.com",
  "password": "password123",
  "department": "hr"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 2,
    "employee_id": "EMP002",
    "name": "Tran Thi B",
    "email": "tranthib@okivietnam.com",
    "department": "hr",
    "role": "user"
  }
}
```

**Error Responses:**
- `400`: Missing required fields
- `409`: Employee ID or email already exists

---

### 5. Change Password
**POST** `/api/auth/change-password`

Đổi mật khẩu cho user đã đăng nhập.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400`: Missing current_password or new_password
- `401`: Current password is incorrect

---

### 6. Logout
**POST** `/api/auth/logout`

Đăng xuất (client nên xóa tokens).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## Overtime Endpoints

### 1. Get Overtime Requests
**GET** `/api/overtime`

Lấy danh sách yêu cầu tăng ca của user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status` (optional): pending, approved, rejected
- `date_from` (optional): YYYY-MM-DD
- `date_to` (optional): YYYY-MM-DD

**Response (200 OK):**
```json
{
  "requests": [
    {
      "id": 1,
      "date": "2026-03-10",
      "start_time": "18:00",
      "end_time": "21:00",
      "reason": "Project deadline",
      "status": "pending",
      "created_at": "2026-03-04T15:39:42.276657",
      "approved_at": null
    }
  ]
}
```

---

### 2. Create Overtime Request
**POST** `/api/overtime`

Tạo yêu cầu tăng ca mới.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "date": "2026-03-10",
  "start_time": "18:00",
  "end_time": "21:00",
  "reason": "Need to complete urgent project tasks"
}
```

**Response (201 Created):**
```json
{
  "message": "Overtime request created successfully",
  "request": {
    "id": 1,
    "date": "2026-03-10",
    "start_time": "18:00",
    "end_time": "21:00",
    "reason": "Need to complete urgent project tasks",
    "status": "pending"
  }
}
```

---

### 3. Update Overtime Request
**PUT** `/api/overtime/<request_id>`

Cập nhật yêu cầu tăng ca (chỉ pending).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "date": "2026-03-11",
  "start_time": "19:00",
  "end_time": "22:00",
  "reason": "Updated reason"
}
```

**Response (200 OK):**
```json
{
  "message": "Overtime request updated successfully",
  "request": {
    "id": 1,
    "date": "2026-03-11",
    "start_time": "19:00",
    "end_time": "22:00",
    "reason": "Updated reason",
    "status": "pending"
  }
}
```

**Error Responses:**
- `404`: Request not found
- `400`: Can only update pending requests

---

### 4. Delete Overtime Request
**DELETE** `/api/overtime/<request_id>`

Xóa yêu cầu tăng ca (chỉ pending).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Overtime request deleted successfully"
}
```

---

### 5. Approve Overtime Request (Admin Only)
**POST** `/api/overtime/<request_id>/approve`

Phê duyệt yêu cầu tăng ca.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Overtime request approved",
  "request": {
    "id": 1,
    "status": "approved",
    "approved_at": "2026-03-04T16:00:00.000000"
  }
}
```

**Error Responses:**
- `403`: Admin access required
- `404`: Request not found
- `400`: Request is not pending

---

### 6. Reject Overtime Request (Admin Only)
**POST** `/api/overtime/<request_id>/reject`

Từ chối yêu cầu tăng ca.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Overtime request rejected",
  "request": {
    "id": 1,
    "status": "rejected",
    "approved_at": "2026-03-04T16:00:00.000000"
  }
}
```

---

## Meal Registration Endpoints

### 1. Get Meal Registrations
**GET** `/api/meals`

Lấy danh sách đăng ký suất ăn.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `date_from` (optional): YYYY-MM-DD
- `date_to` (optional): YYYY-MM-DD

**Response (200 OK):**
```json
{
  "registrations": [
    {
      "id": 1,
      "date": "2026-03-10",
      "meal_type": "lunch",
      "has_meal": true,
      "notes": "Vegetarian option",
      "created_at": "2026-03-04T15:39:42.276657"
    }
  ]
}
```

---

### 2. Create/Update Meal Registration
**POST** `/api/meals`

Tạo hoặc cập nhật đăng ký suất ăn.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "date": "2026-03-10",
  "has_meal": true,
  "meal_type": "lunch",
  "notes": "Vegetarian option"
}
```

**Response (201 Created or 200 OK):**
```json
{
  "message": "Meal registration created",
  "registration": {
    "id": 1,
    "date": "2026-03-10",
    "has_meal": true,
    "meal_type": "lunch",
    "notes": "Vegetarian option"
  }
}
```

---

### 3. Delete Meal Registration
**DELETE** `/api/meals/<registration_id>`

Xóa đăng ký suất ăn.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Meal registration deleted successfully"
}
```

---

## Error Responses

### Common Error Codes

- **400 Bad Request**: Thiếu hoặc sai format dữ liệu
- **401 Unauthorized**: Token không hợp lệ hoặc hết hạn
- **403 Forbidden**: Không có quyền truy cập
- **404 Not Found**: Resource không tồn tại
- **409 Conflict**: Dữ liệu trùng lặp

### Error Response Format
```json
{
  "error": "Error message description"
}
```

---

## Token Expiration

- **Access Token**: 1 hour (3600 seconds)
- **Refresh Token**: 30 days (2592000 seconds)

Khi access token hết hạn, sử dụng refresh token để lấy access token mới.

---

## Example Usage (cURL)

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"EMP001","password":"password123"}'
```

### Get Overtime Requests
```bash
curl -X GET http://localhost:5000/api/overtime \
  -H "Authorization: Bearer <your_access_token>"
```

### Create Overtime Request
```bash
curl -X POST http://localhost:5000/api/overtime \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date":"2026-03-10",
    "start_time":"18:00",
    "end_time":"21:00",
    "reason":"Project deadline"
  }'
```

---

## Testing with Postman

1. Import collection từ file `postman_collection.json`
2. Set environment variable `base_url` = `http://localhost:5000`
3. Login để lấy `access_token`
4. Set environment variable `access_token`
5. Test các endpoints khác

---

## Security Notes

- Luôn sử dụng HTTPS trong production
- Không share access token
- Store tokens securely (không lưu trong localStorage nếu có thể)
- Implement token blacklist cho logout trong production
- Rate limiting nên được implement
- CORS configuration cần được setup đúng

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-04
