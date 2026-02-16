import socket
from datetime import datetime

class NetworkAuditor:
    def __init__(self, target_host):
        self.target_host = target_host

    def probe_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                return s.connect_ex((self.target_host, port)) == 0
        except:
            return False

    def run_audit(self, ports):
        print(f"[*] Audit started at {datetime.now()}")
        for p in ports:
            if self.probe_port(p):
                print(f"[+] Port {p}: OPEN")

if __name__ == "__main__":
    auditor = NetworkAuditor("127.0.0.1")
    auditor.run_audit([22, 80, 443])
