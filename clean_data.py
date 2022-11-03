import pandas as pd
import sqlite3
import os
import tables

def test_tables(cur, tables):
    for table in tables:
        cur.execute('''SELECT * FROM ''' + table)
        rows = cur.fetchall()
        for row in rows:
            print(row)


def test_driver_season(cur):
    
    cur.execute('''
        SELECT drivers.forename, drivers.surname, position from driver_season
        INNER JOIN drivers ON  drivers.id = driver_season.driverId
        WHERE year = 2021
        ORDER BY position DESC
        ''')
    
    for row in cur.fetchall():
        print(row)


def main():

    if os.path.exists("test.db"):
        os.remove("test.db")

    conn = sqlite3.connect("test.db")

    tables.create_all(conn)
    cursor = conn.cursor()

    # fulltables = ("races", "results", "driver_season")
    # test_tables(cursor, fulltables)
    test_driver_season(cursor)


if __name__ == '__main__':
    main()
