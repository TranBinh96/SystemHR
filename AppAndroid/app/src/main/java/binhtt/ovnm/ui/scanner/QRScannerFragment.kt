package binhtt.ovnm.ui.scanner

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.AnimationUtils
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import binhtt.ovnm.R
import binhtt.ovnm.databinding.FragmentQrScannerBinding

class QRScannerFragment : Fragment() {

    private var _binding: FragmentQrScannerBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentQrScannerBinding.inflate(inflater, container, false)
        val root: View = binding.root

        // Only setup views that exist in the layout (tablet only)
        setupTabletViews()

        return root
    }

    private fun setupTabletViews() {
        try {
            val qrScannerViewModel =
                ViewModelProvider(this).get(QRScannerViewModel::class.java)

            // Check if this is tablet layout by checking if scanning line exists
            val scanningLine = binding.root.findViewById<View?>(R.id.scanning_line)
            
            if (scanningLine != null) {
                // This is tablet layout - setup all tablet features
                val scanAnimation = AnimationUtils.loadAnimation(context, R.anim.scanner_animation)
                scanningLine.startAnimation(scanAnimation)

                // Setup button listeners
                binding.root.findViewById<View?>(R.id.btn_flash)?.setOnClickListener {
                    // TODO: Toggle flash
                }

                binding.root.findViewById<View?>(R.id.btn_switch_camera)?.setOnClickListener {
                    // TODO: Switch camera
                }

                binding.root.findViewById<View?>(R.id.btn_report_issue)?.setOnClickListener {
                    // TODO: Report issue
                }

                binding.root.findViewById<View?>(R.id.btn_complete)?.setOnClickListener {
                    // TODO: Complete action
                }

                // Observe ViewModel data
                qrScannerViewModel.mealName.observe(viewLifecycleOwner) { mealName ->
                    binding.root.findViewById<android.widget.TextView?>(R.id.tv_meal_name)?.text = mealName
                }

                qrScannerViewModel.employeeName.observe(viewLifecycleOwner) { employeeName ->
                    binding.root.findViewById<android.widget.TextView?>(R.id.tv_employee_name)?.text = employeeName
                }

                qrScannerViewModel.department.observe(viewLifecycleOwner) { department ->
                    binding.root.findViewById<android.widget.TextView?>(R.id.tv_department)?.text = department
                }

                qrScannerViewModel.mealCredit.observe(viewLifecycleOwner) { mealCredit ->
                    binding.root.findViewById<android.widget.TextView?>(R.id.tv_meal_credit)?.text = mealCredit
                }
            }
            // If scanningLine is null, this is phone layout - do nothing, just show the simple layout
        } catch (e: Exception) {
            e.printStackTrace()
            // Views don't exist in phone layout, that's OK
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
