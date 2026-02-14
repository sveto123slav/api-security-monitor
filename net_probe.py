import socket
import sys
from datetime import datetime

class NetworkAuditor:
    """
    High-performance network socket auditor for infrastructure validation.
    """
    def __init__(self, target_host):
        self.target_host = target_host

    def probe_port(self, port, timeout=1.5):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((self.target_host, port))
                return result == 0
        except socket.error as err:
            return False

    def run_security_scan(self, port_range):
        print(f"[*] Audit started: {self.target_host} at {datetime.now().isoformat()}")
        for port in port_range:
            is_open = self.probe_port(port)
            status = "OPEN" if is_open else "FILTERED"
            if is_open:
                print(f"[+] TCP/{port}: {status}")

if __name__ == "__main__":
    # Internal infrastructure targets
    AUDIT_TARGETS = ["127.0.0.1"]
    CORE_PORTS = [22, 80, 443, 5000, 8080]
    
    for host in AUDIT_TARGETS:
        auditor = NetworkAuditor(host)
        auditor.run_security_scan(CORE_PORTS)
