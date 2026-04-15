package binhtt.ovnm.ui.scanner

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class QRScannerViewModel : ViewModel() {

    private val _mealName = MutableLiveData<String>().apply {
        value = "Cơm gà xối mỡ"
    }
    val mealName: LiveData<String> = _mealName

    private val _mealDescription = MutableLiveData<String>().apply {
        value = "Đặc Sản Bữa Trưa • Bếp Số 1"
    }
    val mealDescription: LiveData<String> = _mealDescription

    private val _employeeName = MutableLiveData<String>().apply {
        value = "Nguyễn Văn Anh"
    }
    val employeeName: LiveData<String> = _employeeName

    private val _department = MutableLiveData<String>().apply {
        value = "Thiết Kế Sáng Tạo"
    }
    val department: LiveData<String> = _department

    private val _mealCredit = MutableLiveData<String>().apply {
        value = "-1 Số Dư"
    }
    val mealCredit: LiveData<String> = _mealCredit

    fun onQRCodeScanned(qrData: String) {
        // TODO: Parse QR code data and update LiveData
        // Example: Parse employee info, meal info, etc.
    }
}
