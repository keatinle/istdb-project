import pandas as pd
from pandasql import sqldf

def fill_table(cur):
	data = pd.read_csv(r'./data/driver_standings.csv')
	df = pd.DataFrame(data)

	data = pd.read_csv(r'./data/races.csv')
	races = pd.DataFrame(data)

	driver_seasons = []
	sql = '''
		INSERT INTO driver_standings(year, driverId, position, points, wins)
		VALUES (%s, %s, %s, %s, %s)
		'''

	for num in range(1950, 2023):

		q = """SELECT races.year, driverId, position, MAX(points) as max, wins 
			FROM df
			INNER JOIN races ON races.raceid = df.raceId 
			WHERE races.year = """ + str(num) + " GROUP BY driverId"

		fixed_df = sqldf(q, locals())

		for row in fixed_df.itertuples():
			ds = (row.year, row.driverId, row.position, row.max, row.wins)
			driver_seasons.append(ds)

	cur.executemany(sql, driver_seasons)

