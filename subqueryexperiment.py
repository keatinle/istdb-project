import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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


    # cursor.execute('''
    # SELECT cs.constructorId, races.season, cs.points
    # FROM constructor_standings AS cs
    # INNER JOIN races ON races.id = cs.raceId 
    # WHERE races.season = 2022 
    # GROUP BY cs.constructorId, races.season, cs.points
    # HAVING constructorId, points IN  (
        
    #     SELECT constructorId, MAX(points) 
    #                    FROM constructor_standings 
    #                    INNER JOIN races ON races.id = constructor_standings.raceId
    #                    WHERE races.season = 2022
    #                    GROUP BY constructorId
    #             )
    # ORDER BY constructorId
    # ''')

    cursor.execute('''
    
        SELECT constructorId, MAX(points) 
            FROM constructor_standings 
            INNER JOIN races ON races.id = constructor_standings.raceId
            WHERE races.season = 2022
            GROUP BY constructorId

        ''')

    for row in cursor.fetchall():
        print(row)

if __name__ == '__main__':
    main()