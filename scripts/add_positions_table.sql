-- Create positions table
CREATE TABLE IF NOT EXISTS positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Add position_id column to users table
ALTER TABLE users ADD COLUMN position_id INT NULL;
ALTER TABLE users ADD FOREIGN KEY (position_id) REFERENCES positions(id);

-- Insert default positions
INSERT INTO positions (code, name) VALUES
('NV', 'Nhân viên'),
('CN', 'Công nhân'),
('TP', 'Trưởng phòng'),
('PP', 'Phó phòng'),
('GS', 'Giám sát'),
('TN', 'Trưởng nhóm'),
('QL', 'Quản lý')
ON DUPLICATE KEY UPDATE name=VALUES(name);
