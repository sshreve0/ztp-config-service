import sqlite3

DB_PATH = "../mnt/var/www/firmware/ztp/mac_registry.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_location_by_mac(mac):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM devices WHERE mac = ?", (mac,))
        result = cur.fetchone()

        if result:
            print(result)
            location = result[1]
            print(location)
            return location
        else:
            return None