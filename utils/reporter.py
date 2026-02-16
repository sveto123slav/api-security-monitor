import json
from datetime import datetime

def generate_security_report(findings: dict):
    """
    Compiles audit findings into a structured JSON report.
    This is what project managers and security leads actually read.
    """
    report = {
        "report_id": f"SR-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "timestamp": datetime.now().isoformat(),
        "status": "COMPLETED",
        "critical_vulnerabilities": findings.get("critical", 0),
        "details": findings
    }
    
    filename = f"reports/audit_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
    print(f"[SUCCESS] Executive report generated: {filename}")
