package bin.ovnmapp;

import android.Manifest;
import android.content.pm.PackageManager;
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
                runOnUiThread(() -> {
                    barcodeScanner.pause();
                    barcodeScanner.setVisibility(View.GONE);
                    webView.setVisibility(View.VISIBLE);
                    String safe = content.replace("\\", "\\\\").replace("'", "\\'");
                    webView.evaluateJavascript("handleQRScanned('" + safe + "')", null);
                    // Tự quét lại sau 4 giây
                    webView.postDelayed(() -> startQRScanner(), 4000);
                });            }
        }

        @Override
        public void possibleResultPoints(List<ResultPoint> resultPoints) {}
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Force landscape
        setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);

        // Giữ màn hình luôn sáng, không khóa
        getWindow().addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON |
            WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON |
            WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD
        );

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

        // Cấu hình ZXing — hỗ trợ QR_CODE và các barcode phổ biến
        barcodeScanner.getBarcodeView().setDecoderFactory(
            new DefaultDecoderFactory(Arrays.asList(
                BarcodeFormat.QR_CODE,
                BarcodeFormat.CODE_128,
                BarcodeFormat.CODE_39,
                BarcodeFormat.EAN_13
            ))
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

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                Log.d("WebView", "Page: " + url);
                if (!url.contains("qr-scanner")) {
                    // Tắt camera khi chuyển sang trang khác
                    stopQRScanner();
                }
                // Nếu về lại qr-scanner thì JS sẽ tự gọi initCamera()
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

    // Tọa độ scanner-frame (dp) do JS báo về
    private int camX, camY, camW, camH;

    // Camera vừa khít với scanner-frame trong HTML
    private void startQRScanner() {
        if (isScanning) return;
        isScanning = true;
        runOnUiThread(() -> {
            float d = getResources().getDisplayMetrics().density;
            if (camW > 0 && camH > 0) {
                // Đặt barcodeScanner đúng vị trí scanner-frame
                android.widget.FrameLayout.LayoutParams lp =
                    new android.widget.FrameLayout.LayoutParams(
                        (int)(camW * d), (int)(camH * d));
                lp.leftMargin = (int)(camX * d);
                lp.topMargin  = (int)(camY * d);
                barcodeScanner.setLayoutParams(lp);
                barcodeScanner.setVisibility(View.VISIBLE);
                Log.d("QRScanner", "Camera in frame: "+camX+","+camY+" "+camW+"x"+camH);
            } else {
                // Fallback fullscreen
                barcodeScanner.setLayoutParams(new android.widget.FrameLayout.LayoutParams(
                    android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
                    android.widget.FrameLayout.LayoutParams.MATCH_PARENT));
                barcodeScanner.setVisibility(View.VISIBLE);
                Log.d("QRScanner", "Camera fullscreen fallback");
            }
            CameraSettings settings = new CameraSettings();
            settings.setRequestedCameraId(1); // front camera
            barcodeScanner.pause();
            barcodeScanner.getBarcodeView().setCameraSettings(settings);
            barcodeScanner.resume();
            barcodeScanner.decodeContinuous(barcodeCallback);
        });
    }
    // Dừng quét
    private void stopQRScanner() {
        isScanning = false;
        runOnUiThread(() -> {
            barcodeScanner.pause();
            barcodeScanner.setVisibility(View.GONE);
            webView.setVisibility(View.VISIBLE);
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
        public void initCamera(int x, int y, int w, int h) {
            Log.d("QRScanner", "initCamera: " + x + "," + y + " " + w + "x" + h);
            camX = x; camY = y; camW = w; camH = h;
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
        public void confirmRegistration(int registrationId) {
            Log.d("WebView", "confirmRegistration called: id=" + registrationId);
            executorService.execute(() -> {
                try {
                    String apiUrl = "https://ovnm.up.railway.app/admin/meal-registrations/" + registrationId + "/confirm";
                    Log.d("WebView", "POST confirm: " + apiUrl);
                    URL url = new URL(apiUrl);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("POST");
                    connection.setConnectTimeout(15000);
                    connection.setReadTimeout(15000);
                    connection.setRequestProperty("Content-Type", "application/json");
                    connection.setRequestProperty("Accept", "application/json");
                    connection.setDoOutput(true);
                    connection.getOutputStream().write("{}".getBytes());

                    int responseCode = connection.getResponseCode();
                    Log.d("WebView", "Confirm response code: " + responseCode);

                    BufferedReader reader = new BufferedReader(
                        new InputStreamReader(
                            responseCode == HttpURLConnection.HTTP_OK
                                ? connection.getInputStream()
                                : connection.getErrorStream()
                        )
                    );
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) response.append(line);
                    reader.close();
                    connection.disconnect();

                    final String jsonData = response.toString();
                    final boolean success = responseCode == HttpURLConnection.HTTP_OK;
                    Log.d("WebView", "Confirm result: " + jsonData);

                    runOnUiThread(() ->
                        webView.evaluateJavascript(
                            "handleConfirmResult(" + success + ", " + registrationId + ", " + jsonData + ")", null
                        )
                    );
                } catch (Exception e) {
                    Log.e("WebView", "confirmRegistration error", e);
                    runOnUiThread(() ->
                        webView.evaluateJavascript(
                            "handleConfirmResult(false, " + registrationId + ", {\"success\":false,\"message\":\"" + e.getMessage() + "\"})", null
                        )
                    );
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
