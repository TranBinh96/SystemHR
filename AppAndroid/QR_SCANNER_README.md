# QR Scanner Layout - The Culinary Concierge

## 📱 Giao Diện Đã Tạo

Layout QR Scanner cho tablet Android được thiết kế dựa trên giao diện web "The Culinary Concierge".

### ✨ Tính Năng

**Cột Trái - Live Scanner:**
- Camera preview với gradient background đẹp mắt
- Scanner frame với 4 góc bo tròn màu xanh lá (#75F39C)
- Scanning line có thể animate
- Status badge "SYSTEM ACTIVE" với pulse animation
- 2 nút điều khiển: Flash và Switch Camera

**Cột Phải - Meal Information:**
- Status badge "ĐÃ XÁC NHẬN" 
- Ảnh món ăn với placeholder gradient
- Thông tin món ăn: tên, mô tả
- Employee card với avatar placeholder
- Department và Meal Credit cards
- Action buttons: Report Issue và Complete
- Recent Activity card

### 🎨 Resources Đã Tạo

**Colors (colors_culinary.xml):**
- Bộ màu Material Design 3 hoàn chỉnh
- Primary: #006E37 (xanh lá)
- Tertiary: #596432 (vàng olive)

**Drawables:**
- ✅ bg_camera_preview.xml - Gradient cho camera
- ✅ bg_avatar_placeholder.xml - Avatar placeholder
- ✅ bg_meal_placeholder.xml - Meal image placeholder
- ✅ scanner_corner_*.xml - 4 góc scanner frame
- ✅ bg_status_active.xml - Badge "SYSTEM ACTIVE"
- ✅ bg_confirmed_badge.xml - Badge "ĐÃ XÁC NHẬN"
- ✅ Icons: flashlight, flip_camera, check_circle, done_all, history, chevron_right

**Animations:**
- ✅ pulse_animation.xml - Cho status dot
- ✅ scanner_animation.xml - Cho scanning line

### 🚀 Cách Sử Dụng

1. **Build project** - Tất cả resources đã sẵn sàng

2. **Thay thế placeholder images** (tùy chọn):
   - Thêm ảnh thật vào `drawable/` nếu muốn
   - Hoặc giữ nguyên placeholder gradient đẹp mắt

3. **Tạo Fragment Kotlin**:
```kotlin
class QRScannerFragment : Fragment() {
    private var _binding: FragmentQrScannerBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentQrScannerBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        // Start animations
        binding.scanningLine.startAnimation(
            AnimationUtils.loadAnimation(context, R.anim.scanner_animation)
        )
        
        // Setup button listeners
        binding.btnFlash.setOnClickListener {
            // Toggle flash
        }
        
        binding.btnSwitchCamera.setOnClickListener {
            // Switch camera
        }
        
        binding.btnComplete.setOnClickListener {
            // Complete action
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

4. **Thêm vào Navigation Graph**:
```xml
<fragment
    android:id="@+id/nav_qr_scanner"
    android:name="binhtt.ovnm.ui.scanner.QRScannerFragment"
    android:label="QR Scanner"
    tools:layout="@layout/fragment_qr_scanner" />
```

### 📦 Tích Hợp QR Scanner

Để thêm chức năng quét QR thực tế, sử dụng một trong các thư viện:

**Option 1: ML Kit (Google)**
```gradle
implementation 'com.google.mlkit:barcode-scanning:17.2.0'
```

**Option 2: ZXing**
```gradle
implementation 'com.journeyapps:zxing-android-embedded:4.3.0'
```

### 🎯 Responsive Design

Layout này được tối ưu cho:
- ✅ Tablet (600dp+)
- ✅ Landscape orientation
- ✅ 2-column layout
- ✅ Material Design 3

### 🎨 Customization

**Thay đổi màu sắc:**
Chỉnh sửa `colors_culinary.xml` để thay đổi theme

**Thay đổi kích thước scanner frame:**
Trong layout, tìm:
```xml
<FrameLayout
    android:layout_width="280dp"
    android:layout_height="280dp"
    ...>
```

**Thêm animation cho pulse dot:**
```kotlin
val pulseAnimation = AnimationUtils.loadAnimation(context, R.anim.pulse_animation)
binding.pulseDot.startAnimation(pulseAnimation)
```

### 📝 Notes

- Layout chỉ hiển thị trên tablet (w600dp+)
- Cần tạo layout cho phone nếu muốn hỗ trợ
- Placeholder images sử dụng gradient đẹp mắt
- Có thể thay thế bằng ảnh thật bất cứ lúc nào

### 🐛 Troubleshooting

**Lỗi "resource not found":**
- Đảm bảo đã sync Gradle
- Clean và Rebuild project

**Layout không hiển thị:**
- Kiểm tra device có width >= 600dp
- Thử trên tablet emulator

**Animation không chạy:**
- Gọi `startAnimation()` trong `onViewCreated()`
- Kiểm tra animation files trong `res/anim/`

---

Made with ❤️ for The Culinary Concierge
