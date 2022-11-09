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


    cursor.execute('''
        SELECT cs.constructorId, cs.year, max(points)
        FROM constructor_standings AS cs
        GROUP BY cs.constructorId, cs.year 
        ORDER BY max)
        '''


    for row in cursor.fetchall():
        print(row)

if __name__ == '__main__':
    main()