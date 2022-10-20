import pandas as pd
import sqlite3
import os

def create_tables(cur):
    commands = ('''
            CREATE TABLE drivers (
                id INT PRIMARY KEY,
                forename TEXT,
                surname TEXT,
                dob TEXT,
                nationality TEXT
                )
            ''',
            '''
            CREATE TABLE constructors (
                id INT PRIMARY KEY,
                name TEXT,
                nationality TEXT
                )
            ''',
            '''
            CREATE TABLE circuits (
                id INT PRIMARY KEY,
                name TEXT,
                country TEXT,
                city TEXT,
                altitude INT
            )
            ''',
            '''
            CREATE TABLE races (
                id INT PRIMARY KEY,
                name TEXT,
                circuitId INT,
                round INT,
                season INT,
                date TEXT
            )
            ''',
            '''
            CREATE TABLE results (
                id INT PRIMARY KEY,
                raceId INT,
                driverId INT,
                constructorId INT,
                grid INT,
                position INT,
                points INT,
                fastestLap INT,
                statusId INT
            )
            '''
            )

    for command in commands:
        cur.execute(command)

def create_driver(cur, driver):
    sql = '''
        INSERT INTO drivers (id, forename, surname, dob, nationality)
        VALUES (?,?,?,?,?)
        '''
    cur.execute(sql, driver)

def create_constructor(cur, constructor):
    sql = '''
        INSERT INTO constructors (id, name, nationality)
        VALUES (?, ?, ?)
        '''
    cur.execute(sql, constructor)

def create_circuit(cur, circuit):
    sql = '''
        INSERT INTO circuits (id, name, country, city, altitude)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, circuit)

def create_race(cur, race):
    sql = '''
        INSERT INTO races (id, name, circuitId, round, season, date)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
    cur.execute(sql, race)

def create_result(cur, result):
    sql = '''
        INSERT INTO results (id, raceId, driverId, constructorId, grid, position, points, fastestLap, statusId)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    cur.execute(sql, result)

def fill_constructor_table(cur):
    data = pd.read_csv(r'./data/constructors.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        constructor = (row.constructorId, row.name, row.nationality)
        create_constructor(cur, constructor)

def fill_driver_table(cursor):
    data = pd.read_csv(r'./data/drivers.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        driver = (row.driverId, row.forename, row.surname, row.dob, row.nationality);
        create_driver(cursor, driver)

def fill_circuit_table(cur):
    data = pd.read_csv(r'./data/circuits.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        circuit = (row.circuitId, row.name, row.country, row.location, row.alt)
        create_circuit(cur, circuit)

def fill_race_table(cur):
    data = pd.read_csv(r'./data/races.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        race = (row.raceId, row.name, row.circuitId, row.round, row.year, row.date)
        create_race(cur, race)

def fill_result_table(cur):
    data = pd.read_csv(r'./data/results.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        result = (row.resultId, 
                row.raceId, 
                row.driverId,
                row.constructorId,
                row.grid,
                row.position,
                row.points,
                row.fastestLap,
                row.statusId)
        create_result(cur, result)

def test_queries(cur):
    print("\nSelect drivers named John\n")
    cur.execute("SELECT * FROM drivers WHERE forename = 'John' ")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    print("\n\nSelect constructors name beginning with M and order by name\n")
    cur.execute("SELECT * FROM constructors WHERE name LIKE 'M%' ORDER BY name DESC")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    
    print("\n\nSelect Spanish circuits\n")
    cur.execute("SELECT * FROM circuits WHERE country = 'Spain'")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    print("\n\nSelect all races in the 2021 season, order by round\n")
    cur.execute("SELECT round, date, name FROM races WHERE season = 2021 ORDER BY round")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    print("\n\nSelect all results from the first race of 2022\n")
    cur.execute('''SELECT results.position, drivers.forename, drivers.surname from drivers 
                    INNER JOIN results ON races.id = results.raceId
                    INNER JOIN races ON results.driverId = drivers.id
                    WHERE (races.season = 2022 AND races.round = 1) 
                ''')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    #(too complicated atm)
    print("\n\nSelect driver names for each constructor for the 2022 season, order by constructor name\n")
    cur.execute('''SELECT DISTINCT drivers.forename, drivers.surname, constructors.name from drivers 
                    INNER JOIN results ON results.driverId = drivers.id
                    INNER JOIN constructors ON results.constructorId = constructors.id
                    INNER JOIN races ON results.raceId = races.id
                    WHERE (races.season = 2022) ORDER BY constructors.name DESC
                ''')
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():

    if os.path.exists("test.db"):
        os.remove("test.db")

    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    create_tables(cursor)
    fill_driver_table(cursor)
    fill_constructor_table(cursor)
    fill_circuit_table(cursor)
    fill_race_table(cursor)
    fill_result_table(cursor)

    test_queries(cursor)

    os.remove("test.db")

if __name__ == '__main__':
    main()
