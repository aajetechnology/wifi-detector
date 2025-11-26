import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "rogue_aps.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rogue_aps (
            id INTEGER PRIMARY KEY,
            ssid TEXT,
            bssid TEXT UNIQUE,
            risk TEXT
        )
    ''')
    rogues = [
        ("FreeAirportWiFi", "00:14:22:33:44:55", "high"),
        ("Starbucks_Guest", "AA:BB:CC:11:22:33", "high"),
        ("xfinitywifi", "00:11:22:33:44:66", "medium")
    ]
    c.executemany("INSERT OR IGNORE INTO rogue_aps (ssid, bssid, risk) VALUES (?, ?, ?)", rogues)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
