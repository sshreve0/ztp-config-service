import sqlite3
from pathlib import Path

# Paths
CONFIGS_ROOT = Path("../mnt/ztp/configs").resolve()
DB_PATH = "../mnt/ztp/configs/mac_registry.sqlite"


conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Recreate the table without path
cur.execute("""
CREATE TABLE IF NOT EXISTS devices (
    mac TEXT PRIMARY KEY,
    location TEXT NOT NULL,
    state TEXT NOT NULL
)
""")

# Track current MACs from filesystem
filesystem_macs = set()

for location_dir in CONFIGS_ROOT.iterdir():
    if location_dir.is_dir():
        location = location_dir.name
        for mac_dir in location_dir.iterdir():
            if mac_dir.is_dir():
                mac = mac_dir.name
                cur.execute("SELECT * FROM devices WHERE mac = ?", (mac,))
                exists = cur.fetchone()

                if not exists:
                    cur.execute("INSERT OR REPLACE INTO devices VALUES (?, ?, ?)", (mac, location, "unmatched"))

                filesystem_macs.add(mac)

# Cleanup stale MACs
cur.execute("SELECT mac FROM devices")
db_macs = {row[0] for row in cur.fetchall()}
stale_macs = db_macs - filesystem_macs
for mac in stale_macs:
    cur.execute("DELETE FROM devices WHERE mac = ?", (mac,))

conn.commit()
conn.close()