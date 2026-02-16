import socket
import logging
from typing import Dict

class ServiceAuditor:
    """
    Advanced network tool to identify running services (Banner Grabbing).
    Essential for identifying outdated or vulnerable software versions.
    """
    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    def grab_banner(self, ip: str, port: int) -> str:
        """Connects to a port and attempts to read the service identification string."""
        try:
            with socket.create_connection((ip, port), timeout=self.timeout) as sock:
                # Някои услуги изискват леко 'подбутване', за да си кажат версията
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors='ignore').strip()
                return banner if banner else "No banner received (Service Stealth)"
        except Exception:
            return "Connection Failed"

    def scan_common_services(self, target_ip: str):
        common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
        logging.info(f"[*] Starting Service Audit for {target_ip}...")
        
        for port, name in common_ports.items():
            banner = self.grab_banner(target_ip, port)
            logging.info(f"[PORT {port} | {name}]: {banner[:50]}...")

if __name__ == "__main__":
    auditor = ServiceAuditor()
    auditor.scan_common_services("8.8.8.8")
