import pandas as pd
import psycopg2
import os
import tables
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

    tables.create_all(con)
    cursor = con.cursor()

if __name__ == '__main__':
    main()
