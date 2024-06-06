import sqlite3

conn = sqlite3.connect('example.db')

cur = conn.cursor()

try:
    # Create a table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
    ''')

    # Insert a row of data
    cur.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
    ''', ('Alice', 30))

    # Commit the transaction
    conn.commit()

    # Query the database
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    conn.rollback()
    print(f"Transaction failed: {e}")
finally:
    conn.close()
