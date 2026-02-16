import json
from datetime import datetime

def create_executive_report(scan_results: dict):
    """Generates a professional JSON report for the security operations center (SOC)."""
    report = {
        "report_id": f"AUDIT-{datetime.now().strftime('%Y%m%d%H%M')}",
        "timestamp": datetime.now().isoformat(),
        "summary": "Infrastructure Audit Completed",
        "data": scan_results
    }
    
    filename = f"audit_report_{datetime.now().strftime('%H%M')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"[*] Report saved: {filename}")
