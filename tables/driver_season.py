import pandas as pd

def create_driver_standing(cur, constructor):
    sql = '''
        INSERT INTO driver_standings (raceId, driverId, position, points, wins)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, constructor)

def fill_ds_table(cur):
    data = pd.read_csv(r'./data/driver_standings.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        cs = (row.raceId, row.driverId, row.position, row.points, row.wins)
        create_driver_standing(cur, cs)


def create_driver_season(cur, dri_sea):
    sql = '''
        INSERT INTO driver_season (year, driverId, position, points, wins)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, dri_sea)

def fill_table(cur):
    fill_ds_table(cur)

    for num in range(1950, 2023):
        standings = []

        cur.execute('''
            SELECT races.season, driverId, position, MAX(points), wins FROM driver_standings
            INNER JOIN races ON races.id = driver_standings.raceId
            WHERE races.season = ''' 
            + str(num)
            + ' GROUP BY driverId')

        for row in cur.fetchall():
            standings.append(row)

        for row in standings:
            create_driver_season(cur, row)
        