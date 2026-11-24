"""REIT Commercial Real Estate Lease Escalation & Common Area Maintenance (CAM) True-Up Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class CommercialTenantLease:
    lease_id: str
    tenant_name: str
    super_built_up_area_sqft: float
    base_rent_per_sqft_inr: float
    cam_rate_per_sqft_inr: float
    lease_start_date: str
    escalation_frequency_years: int = 3
    escalation_rate_pct: float = 15.0

class REITCommercialCAMEngine:
    def __init__(self, property_name: str, total_property_area_sqft: float):
        self.property_name = property_name
        self.total_area_sqft = total_property_area_sqft
        self.leases: Dict[str, CommercialTenantLease] = {}

    def register_lease(self, lease: CommercialTenantLease):
        self.leases[lease.lease_id] = lease

    def compute_monthly_invoice(self, lease_id: str) -> Dict[str, Any]:
        if lease_id not in self.leases:
            raise ValueError(f"Lease {lease_id} not found.")
        l = self.leases[lease_id]
        
        rent = round(l.super_built_up_area_sqft * l.base_rent_per_sqft_inr, 2)
        cam = round(l.super_built_up_area_sqft * l.cam_rate_per_sqft_inr, 2)
        total = round(rent + cam, 2)

        return {
            "lease_id": lease_id,
            "tenant_name": l.tenant_name,
            "area_sqft": l.super_built_up_area_sqft,
            "base_rent_inr": rent,
            "provisional_cam_inr": cam,
            "total_monthly_invoice_inr": total
        }

    def execute_annual_cam_true_up(self, lease_id: str, actual_annual_cam_opex_total: float) -> Dict[str, Any]:
        if lease_id not in self.leases:
            raise ValueError(f"Lease {lease_id} not found.")
        l = self.leases[lease_id]

        proportional_share_pct = l.super_built_up_area_sqft / self.total_area_sqft
        actual_tenant_cam_share = round(actual_annual_cam_opex_total * proportional_share_pct, 2)
        billed_provisional_cam = round(l.super_built_up_area_sqft * l.cam_rate_per_sqft_inr * 12.0, 2)
        
        cam_variance = round(actual_tenant_cam_share - billed_provisional_cam, 2)
        adjustment_type = "DEBIT_NOTE_RECOVERY_FROM_TENANT" if cam_variance > 0 else "CREDIT_NOTE_REFUND_TO_TENANT"

        return {
            "lease_id": lease_id,
            "actual_tenant_cam_share_inr": actual_tenant_cam_share,
            "provisional_cam_billed_inr": billed_provisional_cam,
            "cam_true_up_variance_inr": abs(cam_variance),
            "adjustment_action": adjustment_type
        }
