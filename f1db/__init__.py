import psycopg2  #import of the psycopg2 python library
import os
from flask import Flask, render_template, abort
from f1db import util

##No transaction is started when commands are executed and no commit() or rollback() is required. 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to the postgreSQL server with username, and password credentials
    con = psycopg2.connect(user = os.environ.get("PG_USER"),
                                  password = os.environ.get("PG_PASSWORD"),
                                  host = os.environ.get("PG_HOST"),
                                  port = os.environ.get("PG_PORT"),
                                  database = os.environ.get("PG_DATABASE"))
    
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    print("Connected Successfully to PostgreSQL server!!")
    
    # Obtain a DB Cursor to perform database operations
    
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    os._exit(1)

cursor = con.cursor()

query_dict = {
    "query1": {
        'name':'Get all information about the customers',
        'description':"a wonderful query", 
        'sql':""" SELECT * FROM customer"""
    }, 
    "query2": {
        'name':'Get the customers name',
        'description':"another wonderful query", 
        'sql':""" SELECT name FROM customer """,
    } 

}


#sql_select_query = """ SELECT * FROM customer"""


app = Flask(__name__)

@app.route("/")
def homeroute():
    return render_template("home.html", title="Home", queries=query_dict, sql_html_formatter = util.sql_html_formatter )

@app.route("/query/<query_name>")
def route_query(query_name):
    if query_name not in query_dict:
        abort(404)

    try:
        cursor.execute(query_dict[query_name]['sql'], (0,))
        rows = cursor.fetchall() 
        for row in rows:
         print(row)
    except(Exception, psycopg2.Error) as error :
        con.rollback()
        print("Error:", error)
        abort(500)
    table_head = cursor.description
    title = query_dict[query_name]['name']
    sql = query_dict[query_name]['sql']
    
    return render_template("races.html", title=title, table_head = table_head, rows=rows, code=util.sql_html_formatter(sql))