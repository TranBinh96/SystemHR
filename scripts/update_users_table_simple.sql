-- Script cập nhật bảng users cho server chính (MySQL compatible)
-- Chạy từng câu lệnh, bỏ qua lỗi nếu cột đã tồn tại

USE db_hr;

-- Thêm các cột (nếu lỗi "Duplicate column name" thì cột đã tồn tại, bỏ qua)
ALTER TABLE users ADD COLUMN department_id INT NULL;
ALTER TABLE users ADD COLUMN position_id INT NULL;
ALTER TABLE users ADD COLUMN work_status VARCHAR(20) NULL DEFAULT 'working';
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(255) NULL;
ALTER TABLE users ADD COLUMN role VARCHAR(20) NULL DEFAULT 'user';
ALTER TABLE users ADD COLUMN is_active TINYINT(1) NULL DEFAULT 1;
ALTER TABLE users ADD COLUMN can_approve TINYINT(1) NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN can_register TINYINT(1) NULL DEFAULT 1;
ALTER TABLE users ADD COLUMN created_at DATETIME NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN last_activity DATETIME NULL;

-- Thêm foreign keys (nếu lỗi thì đã tồn tại, bỏ qua)
ALTER TABLE users ADD CONSTRAINT users_ibfk_1 FOREIGN KEY (department_id) REFERENCES departments(id);
ALTER TABLE users ADD CONSTRAINT users_ibfk_2 FOREIGN KEY (position_id) REFERENCES positions(id);

-- Tạo indexes (nếu lỗi thì đã tồn tại, bỏ qua)
CREATE INDEX department_id ON users(department_id);
CREATE INDEX position_id ON users(position_id);

-- Cập nhật giá trị mặc định cho các bản ghi hiện có
UPDATE users SET is_active = 1 WHERE is_active IS NULL;
UPDATE users SET can_register = 1 WHERE can_register IS NULL;
UPDATE users SET can_approve = 0 WHERE can_approve IS NULL;
UPDATE users SET role = 'user' WHERE role IS NULL;
UPDATE users SET work_status = 'working' WHERE work_status IS NULL;
UPDATE users SET created_at = NOW() WHERE created_at IS NULL;

-- Hiển thị cấu trúc bảng sau khi cập nhật
DESCRIBE users;

-- Đếm số lượng users
SELECT COUNT(*) as total_users FROM users;

SELECT 'Cập nhật bảng users hoàn tất!' as status;
