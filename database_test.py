import sqlite3

conn = sqlite3.connect('example.db')

cur = conn.cursor()

try:
    # Create a table
    cur.execute('''
    CREATE TABLE `teammt_PulseTouch`.`WatchStatus` (
        `GroupID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `WatchID` INT UNSIGNED NOT NULL,
        `ActivationTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `ActivationEvent` BOOLEAN NOT NULL,
        PRIMARY KEY (`GroupID`)
    ) ENGINE = InnoDB;
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
