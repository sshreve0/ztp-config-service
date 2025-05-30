import sqlite3

DB_PATH = "../mnt/var/www/firmware/ztp/configs/mac_registry.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_location_by_mac(mac):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM devices WHERE mac = ?", (mac,))
        result = cur.fetchone()

        if result:
            location = result[1]
            return location
        else:
            return None

def set_state(mac,state):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE devices SET state = ? WHERE mac = ?", (state, mac))
