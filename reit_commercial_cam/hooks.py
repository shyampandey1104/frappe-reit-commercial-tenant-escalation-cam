# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "reit_commercial_cam"
app_title = "Frappe Reit Commercial Tenant Escalation Cam"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Reit Commercial Tenant Escalation Cam - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/reit_commercial_cam/css/reit_commercial_cam.bundle.css"
app_include_js = "/assets/reit_commercial_cam/js/reit_commercial_cam.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Reit Commercial Tenant Escalation Cam Entry": {
        "validate": "reit_commercial_cam.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "reit_commercial_cam.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "reit_commercial_cam.tasks.hourly_sync"
    ],
    "daily": [
        "reit_commercial_cam.tasks.daily_reconciliation"
    ],
    "weekly": [
        "reit_commercial_cam.tasks.weekly_digest"
    ]
}
