import hashlib
import json
import os
import logging
from datetime import datetime

class IntegrityVault:
    """
    Professional-grade File Integrity Monitor (FIM).
    Detects unauthorized changes in the infrastructure configuration.
    """
    def __init__(self, target_files: list):
        self.target_files = target_files
        self.state_db = "system_state.json"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | [SECURITY] | %(message)s')

    def _calculate_hash(self, filepath):
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except FileNotFoundError:
            return None

    def scan_for_breaches(self):
        """Compares current file hashes with the saved secure baseline."""
        if not os.path.exists(self.state_db):
            logging.info("Baseline not found. Generating initial security state...")
            self.update_baseline()
            return

        with open(self.state_db, 'r') as f:
            baseline = json.load(f)

        for path in self.target_files:
            current_hash = self._calculate_hash(path)
            if current_hash != baseline.get(path):
                logging.warning(f"!!! SECURITY ALERT !!! File {path} has been tampered with!")
            else:
                logging.info(f"Integrity confirmed: {path}")

    def update_baseline(self):
        new_baseline = {path: self._calculate_hash(path) for path in self.target_files if os.path.exists(path)}
        with open(self.state_db, 'w') as f:
            json.dump(new_baseline, f, indent=4)
        logging.info("Security baseline updated successfully.")

if __name__ == "__main__":
    # Тестване със собствените ни файлове
    audit = IntegrityVault(["core/integrity_vault.py", "README.md"])
    audit.scan_for_breaches()
