-- Fix position levels in positions table
-- Level: 1=highest (Giám đốc), 5=lowest (Công nhân)

-- Update based on position code
UPDATE positions SET level = 1 WHERE code = '0' AND name LIKE '%Giám đốc%';  -- Giám đốc
UPDATE positions SET level = 2 WHERE code = '1';  -- Trưởng Phòng
UPDATE positions SET level = 3 WHERE code = '2';  -- Phó Phòng
UPDATE positions SET level = 3 WHERE code = '5';  -- Giám sát
UPDATE positions SET level = 3 WHERE code = '6';  -- Trưởng nhóm
UPDATE positions SET level = 3 WHERE code = '7';  -- Quản lý
UPDATE positions SET level = 4 WHERE code = '3';  -- Nhân Viên
UPDATE positions SET level = 5 WHERE code = '4';  -- Công Nhân

-- Verify the changes
SELECT code, name, level FROM positions ORDER BY level ASC, code ASC;
