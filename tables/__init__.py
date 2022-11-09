from . import drivers
from . import constructors
from . import circuits
from . import races
from . import results
from . import constructor_season
from . import driver_season

def drop_tables(cur):
    commands = ("DROP TABLE IF EXISTS circuits",
            "DROP TABLE IF EXISTS races",
            "DROP TABLE IF EXISTS drivers",
            "DROP TABLE IF EXISTS constructors",
            "DROP TABLE IF EXISTS results",
            "DROP TABLE IF EXISTS seasons",
            "DROP TABLE IF EXISTS constructor_season",
            "DROP TABLE IF EXISTS driver_season",
            "DROP TABLE IF EXISTS driver_standings",
            "DROP TABLE IF EXISTS constructor_standings"
            )

    for command in commands:
        cur.execute(command)
        
def create_tables(cur):
    commands = (
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
                    season INT,
                    round INT,
                    date TEXT
                )
            ''',
            '''
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
                CREATE TABLE results (
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
                CREATE TABLE seasons (
                    year INT PRIMARY KEY
                )
            ''',
            '''
                CREATE TABLE constructor_season (
                    year INT NOT NULL,
                    constructorId INT NOT NULL,
                    position INT,
                    points INT,
                    wins INT,
                    PRIMARY KEY ( year, constructorId)
                )
            ''',
            '''
                CREATE TABLE driver_season (
                    year INT NOT NULL,
                    driverId INT NOT NULL,
                    position INT,
                    points INT,
                    wins INT,
                    PRIMARY KEY ( year, driverId)
                )
            ''',
            '''
                CREATE TABLE driver_standings (
                    year INT,
                    driverId INT,
                    position INT,
                    points INT,
                    wins INT
                )
            ''',
            '''
                CREATE TABLE constructor_standings (
                    year INT,
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
    constructor_season.fill_table(cursor)
    drivers.fill_table(cursor)
    constructors.fill_table(cursor)
    results.fill_table(cursor)
    driver_season.fill_table(cursor)

def create_all(conn):
    cursor = conn.cursor()

    drop_tables(cursor)
    create_tables(cursor)
    fill_tables(cursor)
