import unittest
from reit_commercial_cam.engine import CommercialTenantLease, REITCommercialCAMEngine

class TestREITCommercialCAMEngine(unittest.TestCase):
    def setUp(self):
        self.engine = REITCommercialCAMEngine("CyberCity Tech Park Gurgaon", total_property_area_sqft=500000.0)
        self.lease = CommercialTenantLease(
            lease_id="LEASE-CYBER-091", tenant_name="Google India LLP",
            super_built_up_area_sqft=50000.0, # 10% of total park
            base_rent_per_sqft_inr=110.0, cam_rate_per_sqft_inr=15.0,
            lease_start_date="2026-01-01"
        )
        self.engine.register_lease(self.lease)

    def test_monthly_billing(self):
        bill = self.engine.compute_monthly_invoice("LEASE-CYBER-091")
        self.assertEqual(bill["base_rent_inr"], 5500000.0)
        self.assertEqual(bill["provisional_cam_inr"], 750000.0)
        self.assertEqual(bill["total_monthly_invoice_inr"], 6250000.0)

    def test_cam_true_up_debit_recovery(self):
        # Actual annual opex was 100,000,000 INR -> Google's 10% share = 10,000,000 INR
        # Google was billed 50,000 sqft * 15 * 12 = 9,000,000 INR
        res = self.engine.execute_annual_cam_true_up("LEASE-CYBER-091", actual_annual_cam_opex_total=100000000.0)
        self.assertEqual(res["adjustment_action"], "DEBIT_NOTE_RECOVERY_FROM_TENANT")
        self.assertEqual(res["cam_true_up_variance_inr"], 1000000.0)

if __name__ == "__main__":
    unittest.main()
