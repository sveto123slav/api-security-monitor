import hashlib
import os
import logging
import json
from datetime import datetime

class IntegrityMonitor:
    """
    Professional File Integrity Monitoring (FIM) system.
    Tracks cryptographic hashes of sensitive infrastructure files.
    """
    def __init__(self, watch_list: list):
        self.watch_list = watch_list
        self.db_file = "integrity_db.json"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | [INTEGRITY] | %(message)s')

    def generate_baseline(self):
        """Creates an initial state of the files to compare against later."""
        baseline = {}
        for path in self.watch_list:
            if os.path.exists(path):
                hash_val = self._calculate_sha256(path)
                baseline[path] = hash_val
        
        with open(self.db_file, "w") as f:
            json.dump(baseline, f)
        logging.info("System baseline generated successfully.")

    def check_integrity(self):
        """Compares current file states with the baseline."""
        if not os.path.exists(self.db_file):
            logging.error("No baseline found. Run generate_baseline() first.")
            return

        with open(self.db_file, "r") as f:
            baseline = json.load(f)

        for path, old_hash in baseline.items():
            if not os.path.exists(path):
                logging.warning(f"CRITICAL: File {path} has been DELETED!")
                continue
            
            current_hash = self._calculate_sha256(path)
            if current_hash != old_hash:
                logging.warning(f"SECURITY ALERT: File {path} has been MODIFIED!")
            else:
                logging.info(f"Integrity verified for {path}.")

    def _calculate_sha256(self, filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

if __name__ == "__main__":
    # Списък с файлове за наблюдение (примерни системни файлове)
    monitor = IntegrityMonitor(["config.json", "main_engine.py"])
    # При първо стартиране: monitor.generate_baseline()
    monitor.check_integrity()
