package binhtt.ovnm

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupWithNavController
import binhtt.ovnm.databinding.ActivityMainBinding
import com.google.android.material.bottomnavigation.BottomNavigationView

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            binding = ActivityMainBinding.inflate(layoutInflater)
            setContentView(binding.root)

            // Get NavController
            val navHostFragment =
                supportFragmentManager.findFragmentById(R.id.nav_host_fragment_content_main) as? NavHostFragment
            val navController = navHostFragment?.navController

            if (navController == null) {
                // If navController is null, something is wrong with the layout
                return
            }

            // Check if this is tablet or phone layout
            val isTabletLayout = findViewById<View>(R.id.nav_qr_scanner) != null

            if (isTabletLayout) {
                // Tablet layout - hide action bar and setup custom navigation
                supportActionBar?.hide()
                setupTabletNavigation()
            } else {
                // Phone layout - setup bottom navigation
                val bottomNavView = findViewById<BottomNavigationView>(R.id.bottom_nav_view)
                bottomNavView?.setupWithNavController(navController)
                
                // Show action bar for phone
                supportActionBar?.show()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun setupTabletNavigation() {
        // Check if we have the custom navigation views (tablet layout)
        val navQrScanner = findViewById<View>(R.id.nav_qr_scanner)
        val navSettings = findViewById<View>(R.id.nav_settings_item)
        val navDashboard = findViewById<View>(R.id.nav_dashboard)
        val navMealLogs = findViewById<View>(R.id.nav_meal_logs)

        if (navQrScanner != null) {
            // Tablet layout - setup custom navigation
            val navHostFragment =
                supportFragmentManager.findFragmentById(R.id.nav_host_fragment_content_main) as? NavHostFragment
            val navController = navHostFragment?.navController

            navQrScanner.setOnClickListener {
                navController?.navigate(R.id.nav_reflow)
            }

            navSettings?.setOnClickListener {
                navController?.navigate(R.id.nav_settings)
            }

            navDashboard?.setOnClickListener {
                navController?.navigate(R.id.nav_transform)
            }

            navMealLogs?.setOnClickListener {
                navController?.navigate(R.id.nav_slideshow)
            }
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        val navHostFragment =
            supportFragmentManager.findFragmentById(R.id.nav_host_fragment_content_main) as? NavHostFragment
        return navHostFragment?.navController?.navigateUp() ?: false || super.onSupportNavigateUp()
    }
}
