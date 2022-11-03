import psycopg2  #import of the psycopg2 python library
import os
from flask import Flask

##No transaction is started when commands are executed and no commit() or rollback() is required. 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to the postgreSQL server with username, and password credentials
    con = psycopg2.connect(user = os.environ.get("PG_USER"),
                                  password = os.environ.get("PG_PASSWORD"),
                                  host = os.environ.get("PG_HOST"),
                                  port = os.environ.get("PG_PORT"))
    
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    print("Connected Successfully to PostgreSQL server!!")
    
    # Obtain a DB Cursor to perform database operations
    cursor = con.cursor();
except (Exception, psycopg2.Error) as error :
     print ("Error while connecting to PostgreSQL", error)

app = Flask(__name__)

@app.route("/")
def homeroute():
    return "hello worls"