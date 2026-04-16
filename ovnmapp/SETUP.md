# Hướng dẫn cài đặt môi trường

## Bước 1: Cài đặt Java JDK 11

### Windows:

**Cách 1: Tải từ Oracle**
1. Truy cập: https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html
2. Tải "Windows x64 Installer"
3. Chạy file cài đặt
4. Thiết lập JAVA_HOME:
   - Mở "Environment Variables"
   - Thêm biến mới: `JAVA_HOME` = `C:\Program Files\Java\jdk-11`
   - Thêm vào PATH: `%JAVA_HOME%\bin`

**Cách 2: Dùng Chocolatey**
```powershell
choco install openjdk11
```

**Cách 3: Dùng Scoop**
```powershell
scoop install openjdk11
```

### Kiểm tra cài đặt:
```bash
java -version
# Kết quả mong đợi: java version "11.x.x"
```

## Bước 2: Cài đặt Android Studio

1. Tải Android Studio: https://developer.android.com/studio
2. Chạy file cài đặt
3. Trong quá trình cài đặt, chọn:
   - ✅ Android SDK
   - ✅ Android SDK Platform
   - ✅ Android Virtual Device

## Bước 3: Cấu hình Android SDK

1. Mở Android Studio
2. Vào **File > Settings > Appearance & Behavior > System Settings > Android SDK**
3. Trong tab **SDK Platforms**, chọn:
   - ✅ Android 14.0 (API 36) hoặc cao hơn
   - ✅ Android 7.0 (API 24) - minimum
4. Trong tab **SDK Tools**, chọn:
   - ✅ Android SDK Build-Tools
   - ✅ Android SDK Platform-Tools
   - ✅ Android Emulator
5. Click **Apply** và đợi tải về

## Bước 4: Mở dự án

1. Mở Android Studio
2. Chọn **File > Open**
3. Chọn thư mục `ovnmapp`
4. Đợi Gradle sync (có thể mất vài phút lần đầu)

## Bước 5: Tạo Virtual Device (Emulator)

1. Trong Android Studio, click **Device Manager** (icon điện thoại)
2. Click **Create Device**
3. Chọn **Tablet** > **Pixel Tablet** (hoặc tablet khác)
4. Chọn **System Image**: API 36 (Android 14.0)
5. Click **Next** > **Finish**

## Bước 6: Chạy ứng dụng

### Cách 1: Dùng Emulator
1. Khởi động emulator từ Device Manager
2. Click nút **Run** (▶️) trong Android Studio
3. Chọn emulator đã khởi động
4. Đợi ứng dụng cài đặt và chạy

### Cách 2: Dùng thiết bị thật
1. Bật **Developer Options** trên thiết bị:
   - Vào **Settings > About Phone**
   - Nhấn 7 lần vào **Build Number**
2. Bật **USB Debugging**:
   - Vào **Settings > Developer Options**
   - Bật **USB Debugging**
3. Kết nối thiết bị qua USB
4. Click **Run** trong Android Studio
5. Chọn thiết bị của bạn

## Bước 7: Build APK để cài đặt

### Build Debug APK:
```bash
# Trong terminal của Android Studio
./gradlew assembleDebug
```

APK sẽ được tạo tại: `app/build/outputs/apk/debug/app-debug.apk`

### Build Release APK:
```bash
./gradlew assembleRelease
```

## Xử lý lỗi thường gặp

### Lỗi: "JAVA_HOME is not set"
**Giải pháp:**
```powershell
# Kiểm tra Java đã cài chưa
java -version

# Nếu chưa có, cài Java JDK 11
# Sau đó thiết lập JAVA_HOME trong Environment Variables
```

### Lỗi: "SDK location not found"
**Giải pháp:**
1. Tạo file `local.properties` trong thư mục gốc
2. Thêm dòng:
```properties
sdk.dir=C\:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk
```
(Thay `YourUsername` bằng tên user của bạn)

### Lỗi: "Gradle sync failed"
**Giải pháp:**
1. Click **File > Invalidate Caches / Restart**
2. Chọn **Invalidate and Restart**
3. Đợi Android Studio khởi động lại

### Lỗi: "Unable to resolve dependency"
**Giải pháp:**
1. Kiểm tra kết nối internet
2. Trong Android Studio: **File > Settings > Build > Gradle**
3. Bật **Offline mode** rồi tắt lại
4. Click **Sync Project with Gradle Files**

## Kiểm tra cài đặt thành công

Chạy các lệnh sau trong terminal:

```bash
# Kiểm tra Java
java -version

# Kiểm tra Gradle
./gradlew --version

# Kiểm tra Android SDK
adb version
```

Nếu tất cả lệnh đều chạy thành công, bạn đã sẵn sàng phát triển!

## Tài liệu tham khảo

- Android Developer: https://developer.android.com/
- Gradle: https://gradle.org/
- Java JDK: https://www.oracle.com/java/
