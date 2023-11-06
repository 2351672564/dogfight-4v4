
import sqlite3
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
print("database connected")
c = conn.cursor()

c.execute(f"UPDATE records SET max_clock=2342.51249529345, min_clock=0.0500000026077032  WHERE id_rec=594")
conn.commit()