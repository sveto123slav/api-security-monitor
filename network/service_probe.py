import socket
import logging

class ServiceProbe:
    """
    Advanced network utility to identify service banners and versions.
    Essential for vulnerability assessment in remote access environments.
    """
    def __init__(self, timeout: float = 2.5):
        self.timeout = timeout
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    def identify_service(self, ip: str, port: int) -> str:
        try:
            with socket.create_connection((ip, port), timeout=self.timeout) as sock:
                # Изпращаме стандартна заявка, за да предизвикаме отговор
                sock.sendall(b"GET / HTTP/1.1\r\nHost: pangolin.org\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner if banner else "Service detected but no banner provided."
        except Exception as e:
            return f"Service unreachable: {str(e)}"

    def audit_common_ports(self, host: str):
        ports = [22, 80, 443, 3306]
        logging.info(f"[*] Starting Deep Service Probe on {host}...")
        for p in ports:
            info = self.identify_service(host, p)
            logging.info(f"[PORT {p}]: {info[:60]}...")

if __name__ == "__main__":
    probe = ServiceProbe()
    probe.audit_common_ports("8.8.8.8") # Примерно сканиране на Google DNS
