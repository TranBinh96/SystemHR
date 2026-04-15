-- Script cập nhật bảng users cho server chính
-- Chạy script này để thêm các cột còn thiếu vào bảng users đã tồn tại

USE db_hr;

-- Thêm cột department_id nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS department_id INT NULL,
ADD CONSTRAINT users_ibfk_1 FOREIGN KEY (department_id) REFERENCES departments(id);

-- Thêm cột position_id nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS position_id INT NULL,
ADD CONSTRAINT users_ibfk_2 FOREIGN KEY (position_id) REFERENCES positions(id);

-- Thêm cột work_status nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS work_status VARCHAR(20) NULL DEFAULT 'working';

-- Thêm cột avatar_url nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(255) NULL;

-- Thêm cột role nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS role VARCHAR(20) NULL DEFAULT 'user';

-- Thêm cột is_active nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS is_active TINYINT(1) NULL DEFAULT 1;

-- Thêm cột can_approve nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS can_approve TINYINT(1) NULL DEFAULT 0;

-- Thêm cột can_register nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS can_register TINYINT(1) NULL DEFAULT 1;

-- Thêm cột created_at nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS created_at DATETIME NULL DEFAULT CURRENT_TIMESTAMP;

-- Thêm cột last_activity nếu chưa có
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS last_activity DATETIME NULL;

-- Tạo index cho department_id nếu chưa có
CREATE INDEX IF NOT EXISTS department_id ON users(department_id);

-- Tạo index cho position_id nếu chưa có
CREATE INDEX IF NOT EXISTS position_id ON users(position_id);

-- Cập nhật giá trị mặc định cho các bản ghi hiện có
UPDATE users SET is_active = 1 WHERE is_active IS NULL;
UPDATE users SET can_register = 1 WHERE can_register IS NULL;
UPDATE users SET can_approve = 0 WHERE can_approve IS NULL;
UPDATE users SET role = 'user' WHERE role IS NULL;
UPDATE users SET work_status = 'working' WHERE work_status IS NULL;
UPDATE users SET created_at = NOW() WHERE created_at IS NULL;

-- Hiển thị cấu trúc bảng sau khi cập nhật
DESCRIBE users;

SELECT 'Cập nhật bảng users thành công!' as status;
