-- Xóa tất cả positions cũ
DELETE FROM positions;

-- Thêm positions mới với mã số
INSERT INTO positions (code, name) VALUES
('1', 'Nhân viên'),
('2', 'Công nhân'),
('3', 'Trưởng phòng'),
('4', 'Phó phòng'),
('5', 'Giám sát'),
('6', 'Trưởng nhóm'),
('7', 'Quản lý');
