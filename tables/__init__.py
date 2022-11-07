from . import drivers
from . import constructors
from . import circuits
from . import races
from . import results
from . import constructor_season
from . import driver_season

__all__ = ["drivers"]

def create_tables(cur):
    commands = (
            '''
                CREATE TABLE IF NOT EXISTS circuits (
                    id INT PRIMARY KEY,
                    name TEXT,
                    country TEXT,
                    city TEXT,
                    altitude INT
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS races (
                    id INT PRIMARY KEY,
                    name TEXT,
                    circuitId INT,
                    season INT,
                    round INT,
                    date TEXT
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS drivers (
                    id INT PRIMARY KEY,
                    forename TEXT,
                    surname TEXT,
                    dob TEXT,
                    nationality TEXT
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS constructors (
                    id INT PRIMARY KEY,
                    name TEXT,
                    nationality TEXT    
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS results (
                    id INT PRIMARY KEY,
                    raceId INT,
                    driverId INT,
                    constructorId INT,
                    grid INT,
                    position INT,
                    points INT,
                    fastestLap INT,
                    status TEXT
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS seasons (
                    year INT PRIMARY KEY
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS constructor_season (
                    year INT NOT NULL,
                    constructorId INT NOT NULL,
                    position INT,
                    points INT,
                    wins INT,
                    PRIMARY KEY ( year, constructorId)
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS driver_season (
                    year INT NOT NULL,
                    driverId INT NOT NULL,
                    position INT,
                    points INT,
                    wins INT,
                    PRIMARY KEY ( year, driverId)
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS driver_standings (
                    raceId INT,
                    driverId INT,
                    position INT,
                    points INT,
                    wins INT
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS constructor_standings (
                    raceId INT,
                    constructorId INT,
                    position INT,
                    points INT,
                    wins INT
                )
            '''
            )

    for command in commands:
        cur.execute(command)

def fill_tables(cursor):
    circuits.fill_table(cursor)
    races.fill_table(cursor)
    drivers.fill_table(cursor)
    constructors.fill_table(cursor)
    results.fill_table(cursor)
    constructor_season.fill_table(cursor)
    driver_season.fill_table(cursor)

def create_all(conn):
    cursor = conn.cursor()
    create_tables(cursor)

    fill_tables(cursor)
