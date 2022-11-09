import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/driver_standings.csv')
    df = pd.DataFrame(data)

    driver_seasons = []
    sql = '''
        INSERT INTO driver_standings(year, driverId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''

    for row in df.itertuples():
        cur.execute('''SELECT races.season FROM races where races.id = ''' + str(row.raceId))
        year = cur.fetchone()[0]

        ds = (year, row.driverId, row.position, row.points, row.wins)
        driver_seasons.append(ds)

    cur.executemany(sql, driver_seasons)

