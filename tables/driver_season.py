import pandas as pd


def fill_intermediate_ds_table(cur):
    data = pd.read_csv(r'./data/driver_standings.csv')
    df = pd.DataFrame(data)

    driver_standings = []

    for row in df.itertuples():
        ds = (row.raceId, row.driverId, row.position, row.points, row.wins)
        driver_standings.append(ds)

    sql = '''
        INSERT INTO driver_standings (raceId, driverId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''
    cur.executemany(sql, driver_standings)

def fill_table(cur):
    fill_ds_table(cur)

    sql = '''
        INSERT INTO driver_season (year, driverId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''

    for num in range(1950, 2023):
        cur.execute('''
            SELECT races.season, driverId, position, MAX(points), wins FROM driver_standings
            INNER JOIN races ON races.id = driver_standings.raceId
            WHERE races.season = ''' 
            + str(num)
            + ' GROUP BY driverId')

        driver_seasons = []

        for row in cur.fetchall():
            driver_seasons.append(row)

        cur.executemany(sql, driver_seasons)
        cur.execute("DROP TABLE driver_standings")
