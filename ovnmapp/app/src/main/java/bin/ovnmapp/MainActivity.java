package bin.ovnmapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.google.zxing.BarcodeFormat;
import com.google.zxing.ResultPoint;
import com.journeyapps.barcodescanner.BarcodeCallback;
import com.journeyapps.barcodescanner.BarcodeResult;
import com.journeyapps.barcodescanner.DecoratedBarcodeView;
import com.journeyapps.barcodescanner.DefaultDecoderFactory;
import com.journeyapps.barcodescanner.camera.CameraSettings;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private static final int CAMERA_PERMISSION_REQUEST = 100;
    private WebView webView;
    private DecoratedBarcodeView barcodeScanner;
    private ExecutorService executorService;
    private boolean isScanning = false;

    private final BarcodeCallback barcodeCallback = new BarcodeCallback() {
        @Override
        public void barcodeResult(BarcodeResult result) {
            if (result.getText() != null && isScanning) {
                isScanning = false;
                String content = result.getText();
                Log.d("QRScanner", "Scanned: " + content);

                // Dừng camera và ẩn đi
                barcodeScanner.pause();
                runOnUiThread(() -> {
                    barcodeScanner.setVisibility(View.GONE);
                    webView.setBackgroundColor(Color.WHITE);
                    // Gửi kết quả về JS
                    String safe = content.replace("\\", "\\\\").replace("'", "\\'");
                    webView.evaluateJavascript("handleQRScanned('" + safe + "')", null);
                });
            }
        }

        @Override
        public void possibleResultPoints(List<ResultPoint> resultPoints) {}
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        if (getSupportActionBar() != null) getSupportActionBar().hide();

        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );

        setContentView(R.layout.activity_main);

        executorService = Executors.newSingleThreadExecutor();
        webView = findViewById(R.id.webView);
        barcodeScanner = findViewById(R.id.barcodeScanner);

        // Cấu hình ZXing — camera settings sẽ được apply khi startQRScanner()
        barcodeScanner.getBarcodeView().setDecoderFactory(
            new DefaultDecoderFactory(Arrays.asList(BarcodeFormat.QR_CODE))
        );
        barcodeScanner.setStatusText(""); // Ẩn text mặc định của ZXing

        // Cấu hình WebView
        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setLoadWithOverviewMode(true);
        ws.setUseWideViewPort(true);
        ws.setBuiltInZoomControls(false);
        ws.setDisplayZoomControls(false);
        ws.setSupportZoom(false);
        ws.setDefaultTextEncodingName("utf-8");
        ws.setCacheMode(WebSettings.LOAD_DEFAULT);
        ws.setAllowFileAccess(true);
        ws.setAllowContentAccess(true);
        ws.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        webView.addJavascriptInterface(new WebAppInterface(), "AndroidAPI");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage msg) {
                Log.d("WebView", msg.message() + " -- line " + msg.lineNumber());
                return true;
            }
        });

        webView.loadUrl("file:///android_asset/qr-scanner.html");

        // Xử lý nút Back
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (isScanning) {
                    stopQRScanner();
                } else if (webView.canGoBack()) {
                    webView.goBack();
                } else {
                    setEnabled(false);
                    getOnBackPressedDispatcher().onBackPressed();
                }
            }
        });
    }

    // Tìm đúng camera ID của camera trước dùng Camera2 API
    private int getFrontCameraId() {
        try {
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
            String[] ids = manager.getCameraIdList();
            for (String id : ids) {
                CameraCharacteristics chars = manager.getCameraCharacteristics(id);
                Integer facing = chars.get(CameraCharacteristics.LENS_FACING);
                if (facing != null && facing == CameraCharacteristics.LENS_FACING_FRONT) {
                    Log.d("QRScanner", "Front camera found: id=" + id);
                    return Integer.parseInt(id);
                }
            }
        } catch (Exception e) {
            Log.e("QRScanner", "getFrontCameraId error: " + e.getMessage());
        }
        Log.w("QRScanner", "Front camera not found, fallback to id=1");
        return 1;
    }

    // Tạo camera settings dùng camera trước
    private CameraSettings buildCameraSettings() {
        CameraSettings settings = new CameraSettings();
        settings.setRequestedCameraId(getFrontCameraId());
        return settings;
    }

    // Bắt đầu quét — hiện camera lên trên WebView
    private void startQRScanner() {
        isScanning = true;
        runOnUiThread(() -> {
            barcodeScanner.setVisibility(View.VISIBLE);
            webView.setBackgroundColor(Color.TRANSPARENT);
            // Phải pause trước, set settings, rồi mới resume
            barcodeScanner.pause();
            barcodeScanner.getBarcodeView().setCameraSettings(buildCameraSettings());
            barcodeScanner.resume();
            barcodeScanner.decodeContinuous(barcodeCallback);
        });
    }

    // Dừng quét — ẩn camera
    private void stopQRScanner() {
        isScanning = false;
        runOnUiThread(() -> {
            barcodeScanner.pause();
            barcodeScanner.setVisibility(View.GONE);
            webView.setBackgroundColor(Color.WHITE);
            webView.evaluateJavascript("handleQRCancelled()", null);
        });
    }

    public class WebAppInterface {

        @JavascriptInterface
        public void startQRScan() {
            Log.d("QRScanner", "startQRScan called");
            if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA)
                    == PackageManager.PERMISSION_GRANTED) {
                startQRScanner();
            } else {
                ActivityCompat.requestPermissions(
                    MainActivity.this,
                    new String[]{Manifest.permission.CAMERA},
                    CAMERA_PERMISSION_REQUEST
                );
            }
        }

        @JavascriptInterface
        public void stopQRScan() {
            stopQRScanner();
        }

        @JavascriptInterface
        public void fetchMealData() {
            Log.d("WebView", "fetchMealData called");
            executorService.execute(() -> {
                try {
                    // Lấy ngày hôm nay dạng YYYY-MM-DD
                    java.util.Calendar cal = java.util.Calendar.getInstance();
                    String todayStr = String.format("%04d-%02d-%02d",
                        cal.get(java.util.Calendar.YEAR),
                        cal.get(java.util.Calendar.MONTH) + 1,
                        cal.get(java.util.Calendar.DAY_OF_MONTH));
                    String apiUrl = "https://ovnm.up.railway.app/admin/meal-registrations/list"
                        + "?date_from=" + todayStr + "&date_to=" + todayStr;
                    Log.d("WebView", "Fetching: " + apiUrl);
                    URL url = new URL(apiUrl);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("GET");
                    connection.setConnectTimeout(15000);
                    connection.setReadTimeout(15000);
                    connection.setRequestProperty("Accept", "application/json");

                    int responseCode = connection.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        BufferedReader reader = new BufferedReader(
                            new InputStreamReader(connection.getInputStream())
                        );
                        StringBuilder response = new StringBuilder();
                        String line;
                        while ((line = reader.readLine()) != null) response.append(line);
                        reader.close();

                        final String jsonData = response.toString();
                        runOnUiThread(() ->
                            webView.evaluateJavascript("handleMealDataFromAndroid(" + jsonData + ")", null)
                        );
                    } else {
                        sendErrorToWebView("Lỗi HTTP: " + responseCode);
                    }
                    connection.disconnect();
                } catch (Exception e) {
                    Log.e("WebView", "Error", e);
                    sendErrorToWebView("Lỗi: " + e.getMessage());
                }
            });
        }

        @JavascriptInterface
        public void fetchAllMealData() {
            Log.d("WebView", "fetchAllMealData called");
            executorService.execute(() -> {
                try {
                    String apiUrl = "https://ovnm.up.railway.app/admin/meal-registrations/list";
                    Log.d("WebView", "Fetching all: " + apiUrl);
                    URL url = new URL(apiUrl);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("GET");
                    connection.setConnectTimeout(15000);
                    connection.setReadTimeout(15000);
                    connection.setRequestProperty("Accept", "application/json");

                    int responseCode = connection.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        BufferedReader reader = new BufferedReader(
                            new InputStreamReader(connection.getInputStream())
                        );
                        StringBuilder response = new StringBuilder();
                        String line;
                        while ((line = reader.readLine()) != null) response.append(line);
                        reader.close();

                        final String jsonData = response.toString();
                        runOnUiThread(() ->
                            webView.evaluateJavascript("handleMealDataFromAndroid(" + jsonData + ")", null)
                        );
                    } else {
                        sendErrorToWebView("Lỗi HTTP: " + responseCode);
                    }
                    connection.disconnect();
                } catch (Exception e) {
                    Log.e("WebView", "Error", e);
                    sendErrorToWebView("Lỗi: " + e.getMessage());
                }
            });
        }

        private void sendErrorToWebView(String error) {
            runOnUiThread(() -> {
                String safe = error.replace("'", "\\'");
                webView.evaluateJavascript("handleMealDataError('" + safe + "')", null);
            });
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERMISSION_REQUEST
                && grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            startQRScanner();
        } else {
            runOnUiThread(() ->
                webView.evaluateJavascript("handleQRError('Không có quyền camera')", null)
            );
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (isScanning) barcodeScanner.resume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        barcodeScanner.pause();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        // Cho ZXing xử lý volume key (zoom)
        return barcodeScanner.onKeyDown(keyCode, event) || super.onKeyDown(keyCode, event);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            );
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (executorService != null) executorService.shutdown();
    }
}
