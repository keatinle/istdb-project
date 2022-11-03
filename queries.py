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
def check_data(cur):
    cur.execute('''
        SELECT races.season, constructors.name, COUNT(DISTINCT drivers.Id) as driverCount
        FROM results
        INNER JOIN drivers ON results.driverId = drivers.id
        INNER JOIN constructors ON results.constructorId = constructors.id
        INNER JOIN races ON races.id = results.raceId
        GROUP BY constructors.name, races.season ORDER BY driverCount ASC

        ''')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.execute('''
        SELECT races.season, drivers.forename, drivers.surname, COUNT(DISTINCT constructors.Id) as constructorCount
        FROM results
        INNER JOIN drivers ON results.driverId = drivers.id
        INNER JOIN constructors ON results.constructorId = constructors.id
        INNER JOIN races ON races.id = results.raceId
        GROUP BY drivers.forename, drivers.surname, races.season ORDER BY constructorCount ASC

        ''')
    rows = cur.fetchall()
    for row in rows:
        print(row)

