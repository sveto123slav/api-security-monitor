import sqlite3
import logging

def check_db_integrity(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        if result[0] == "ok":
            print(f"[SUCCESS] Database {db_path} is healthy.")
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")

if __name__ == "__main__":
    # Just a sample check for a local db
    check_db_integrity("system.db")
