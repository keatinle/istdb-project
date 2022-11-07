import pandas as pd
import psycopg2
import os
import tables
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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

    db_config = dict(
        user = "postgres",
        password = "leonel",
        host = "localhost",
        port = "5432",
        database = "f1"
    )
    #try:
    # Connect to the postgreSQL server with username, and password credentials
    con = psycopg2.connect(**db_config)
    
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("Connected Successfully to PostgreSQL server!!")

    cursor = con.cursor()

    tables.create_all(con)
    cursor = con.cursor()

    # fulltables = ("races", "results", "driver_season")
    # test_tables(cursor, fulltables)
    test_driver_season(cursor)


if __name__ == '__main__':
    main()
