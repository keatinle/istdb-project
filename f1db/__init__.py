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
								  #sslmode="allow")
	
	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	print("Connected Successfully to PostgreSQL server!!")
	
	# Obtain a DB Cursor to perform database operations
	
except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
	os._exit(1)

cursor = con.cursor()

# X What team won the constructor"s championship with the most retirements by fire (if any)? (constructor standing, result(status), season into results?)\\

# Did a driver that started their career in a team that never scored any points ever win the driver"s championship (Name).\\

# XX Which season had the most crashes at an altitude of over 500 metres 
# XX Which drivers have gone from last start position to first in the race  (Jenson Button)\\

# Have any drivers scored over 50\% of a teams lifetime points\\

# XX Circuit with the most accidents or where the least drivers finish a race\\
# XX Which driver did not finish the most races on their birthday?\\

# Which driver/team pairing lasted the longest?

# Driver death? 

# XX Which season/race had the most retirements (by fire?)

# X Which driver country has the most points overall?
# X Which constructor country has the most points overall?

query_dict = {
	"season_crashes_altitude": {
		"name": "Seasons with the most Collisions over 500metres",
		"description": "Returns an ordered list of seasons and the number of crashes that occurred at an altitude of over 500 metres", 
		"sql": """
			SELECT races.season, count(*) FROM races 
			INNER JOIN circuits on races.circuitId = circuits.id
			INNER JOIN results ON results.raceId = races.id 
			WHERE results.status = 'Collision' AND circuits.altitude >= 500
			GROUP BY races.season
			ORDER BY count DESC;
		"""
	}, 
	"circuit_most_retirements": {
		"name": "Circuits with most Retirements",
		"description": "Returns an ordered list of circuits by the number of retirements (if greater than one) at that circuit", 
		"sql": """ 
			SELECT circuits.name, COUNT(*) FROM circuits
			INNER JOIN races ON races.circuitId = circuits.id
			INNER JOIN results ON results.raceId = races.id
			WHERE results.status = 'Retired'
			GROUP BY circuits.name
			HAVING COUNT(*) > 1
			ORDER BY count DESC; 
		"""
	},
	"driver_birthday_dnf": {
		"name": "Drivers who did not finish on their birthday",
		"description": " Returns the full name of drivers that did not finish a race on their birthday",
		"sql": """
			SELECT drivers.forename, drivers.surname FROM drivers
			INNER JOIN results ON results.driverId = drivers.id
			INNER JOIN races ON races.id = results.raceId
			WHERE results.position IS NULL 
			AND EXTRACT(MONTH FROM drivers.dob) = EXTRACT(MONTH FROM races.date)
			AND EXTRACT(DAY FROM drivers.dob) = EXTRACT(DAY FROM races.date)
			ORDER BY races.date;
			"""
	}, # WHERE results.position = "1" 
	"driver_last_first": {
		"name": "Which drivers have gone from the back of the grid to first place in the same race",
		"description": "Returns the name(s) of driver that managed to win from the end of the grid, including their starting position",
		"sql": """
			SELECT drivers.forename, drivers.surname, results.grid FROM drivers
			INNER JOIN results ON results.driverId = drivers.id
			WHERE results.grid >= 20
			AND results.position = 1;         
		"""
	}, #( SELECT MAX(results.grid) FROM results GROUP BY results.raceID )
	"driver_country_res": {
		"name": "Most points by driver nationality",
		"description": "",
		"sql": """
			SELECT drivers.nationality, SUM(driver_standings.points) FROM drivers
			INNER JOIN driver_standings ON driver_standings.driverId = drivers.id
			GROUP BY nationality;     
		"""
	},
	# "driver_zero_teammate_win": {
	# 	"name": "Did any driver ever score 0 points the same year their teammate won the Driver's Championship",
	# 	"description": "",
	# 	"sql": """
			
	# 		SELECT forename, surname, zeros.year FROM
	# 		(
	# 			SELECT drivers.forename, drivers.surname, driver_standings.year, results.constructorId
	# 			FROM drivers 
	# 			INNER JOIN results ON results.driverId = drivers.id
	# 			INNER JOIN driver_standings ON driver_standings.driverId = drivers.id
	# 			WHERE driver_standings.points = 0
	# 		) zeros 
	# 		INNER JOIN
	# 		( 
	# 			SELECT DISTINCT ds.driverId, ds.year, results.constructorId
	# 			FROM driver_standings AS ds
	# 			INNER JOIN results ON results.driverId = ds.driverId
	# 			INNER JOIN races 
	# 			ON races.season = ds.year
	# 			AND results.raceId = races.id
	# 			WHERE ds.position = 1
	# 		) AS winners
	# 			ON winners.constructorId = zeros.constructorId
	# 			AND winners.year = zeros.year;
			

	# 	"""

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
		cursor.execute(query_dict[query_name]["sql"], (0,))
		rows = cursor.fetchall() 

	except(Exception, psycopg2.Error) as error :
		con.rollback()
		print("Error: ", error)
		abort(500)

	table_head = cursor.description
	title = query_dict[query_name]["name"]
	sql = query_dict[query_name]["sql"]
	
	return render_template("races.html", title=title, table_head = table_head, rows=rows, code=util.sql_html_formatter(sql))