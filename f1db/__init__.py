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
                                  #sslmode='allow')
    
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("Connected Successfully to PostgreSQL server!!")
    
    # Obtain a DB Cursor to perform database operations
    
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    os._exit(1)

cursor = con.cursor()

query_dict = {
    "season_crashes_altitude": {
        'name':'Seasons with the most Collisions over 500metres',
        'description':"Returns an ordered list of seasons and the number of crashes that occurred at an altitude of over 500 metres", 
        'sql': """SELECT races.season, count(*) FROM races 
            INNER JOIN circuits on races.circuitId = circuits.id
            INNER JOIN results ON results.raceId = races.id 
            WHERE results.status = 'Collision' AND circuits.altitude >= 500
            GROUP BY races.season
            ORDER BY count DESC"""
    }, 
    "circuit_most_retirements": {
        'name':'Circuits with most Retirements',
        'description':"Returns an ordered list of circuits by the number of retirements that are bigger than one at that circuit", 
        'sql':""" SELECT circuits.name, COUNT(*) FROM circuits
            INNER JOIN races ON races.circuitId = circuits.id
            INNER JOIN results ON results.raceId = races.id
            WHERE results.status = 'Retired'
            GROUP BY circuits.name
            HAVING COUNT(*) > 1
            ORDER BY count DESC; """,
    },
    "driver_birthday_dnf": {
        'name':"Drivers who did not finish on their birthday",
        'description': " Returns the full name of drivers that did not finish a race on their birthday",
        'sql': """SELECT drivers.forename, drivers.surname FROM drivers
            INNER JOIN results ON results.driverId = drivers.id
            INNER JOIN races ON races.id = results.raceId
            WHERE results.position IS NULL 
            AND EXTRACT(MONTH FROM drivers.dob) = EXTRACT(MONTH FROM races.date)
            AND EXTRACT(DAY FROM drivers.dob) = EXTRACT(DAY FROM races.date) """
    }, # WHERE results.position = '1' 
    "driver_last_first":{
        'name':"Which drivers have gone from the back of the grid to first place in the same race",
        'dewscription': "Returns the name(s) of driver that managed to win from the end of the grid, including their starting position",
        'sql':"""SELECT drivers.forename, drivers.surname, results.grid FROM drivers
                INNER JOIN results ON results.driverId = drivers.id
                WHERE results.grid >= '20'
                AND results.position = '1';         
        """
    }, #( SELECT MAX(results.grid) FROM results GROUP BY results.raceID )
    "test":{
        'name':"test test test ",
        'dewscription': "",
        'sql':"""SELECT MAX(results.grid), results.raceID, races.season FROM results 
        INNER JOIN races ON races.id = results.raceID
        GROUP BY results.raceID, races.season
        ORDER BY results.raceID DESC;         
        """
    },
    "driver_country_res":{
        'name':"",
        'dewscription': "",
        'sql':"""SELECT drivers.nationality, SUM(drivers_standings.points) FROM drivers
                INNER JOIN driver_standings ON driver_standings.driverId = drivers.id
                GROUP BY nationality         
        """

    }
}



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

    except(Exception, psycopg2.Error) as error :
        con.rollback()
        print("Error:", error)
        abort(500)

    table_head = cursor.description
    title = query_dict[query_name]['name']
    sql = query_dict[query_name]['sql']
    
    return render_template("races.html", title=title, table_head = table_head, rows=rows, code=util.sql_html_formatter(sql))