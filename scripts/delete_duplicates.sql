-- =====================================================
-- SQL XÓA DUPLICATE MEAL REGISTRATIONS MỘT PHÁT
-- Giữ lại record có ID nhỏ nhất cho mỗi user/ngày
-- =====================================================

-- 1. KIỂM TRA DUPLICATE TRƯỚC KHI XÓA
SELECT 
    user_id, 
    date, 
    COUNT(*) as duplicate_count,
    MIN(id) as keep_id,
    MAX(id) as delete_max_id
FROM meal_registrations 
GROUP BY user_id, date 
HAVING COUNT(*) > 1
ORDER BY user_id, date;

-- 2. XÓA DUPLICATE - GIỮ LẠI ID NHỎ NHẤT
DELETE mr1 FROM meal_registrations mr1
INNER JOIN (
    SELECT 
        user_id, 
        date, 
        MIN(id) as keep_id
    FROM meal_registrations 
    GROUP BY user_id, date 
    HAVING COUNT(*) > 1
) mr2 ON mr1.user_id = mr2.user_id 
    AND mr1.date = mr2.date 
    AND mr1.id > mr2.keep_id;

-- 3. KIỂM TRA SAU KHI XÓA (không nên có kết quả)
SELECT 
    user_id, 
    date, 
    COUNT(*) as count
FROM meal_registrations 
GROUP BY user_id, date 
HAVING COUNT(*) > 1;

-- 4. THỐNG KÊ SAU KHI XÓA
SELECT 
    COUNT(*) as total_registrations,
    COUNT(DISTINCT CONCAT(user_id, '-', date)) as unique_combinations,
    COUNT(*) - COUNT(DISTINCT CONCAT(user_id, '-', date)) as remaining_duplicates
FROM meal_registrations;