# Admin/Meals - Next 7 Days Only ✅ COMPLETED

**Goal**: Bỏ ngày quá khứ, chỉ hiện 7 ngày tiếp theo → **Done!**

**Status**:
- [x] Step 1: Create TODO.md ✅
- [x] Step 2: Edit templates/admin_meals.html ✅
  - `updateDayPicker()`: Next 7 days from today + offset
  - `changeWeek(offset)` → `changeDays(offset)`  
  - `#weekDisplay`: "7 ngày từ [date]"
  - Past days: Strikethrough + disabled
- [x] Step 3: Template ready for testing ✅
- [x] Step 4: Task complete ✅

**Test**: `start_server.bat` → `/admin/meals`
- Days: "Hôm nay", "Ngày mai", ... "T7" (7 days forward)
- Nav << >>: Jump 7 days
- Past days grayed out ✅

**Files changed**: `templates/admin_meals.html`
