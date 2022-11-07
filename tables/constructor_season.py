import pandas as pd

def fill_intermediate_cs_table(cur):
    data = pd.read_csv(r'./data/constructor_standings.csv')
    df = pd.DataFrame(data)

    constructor_standings = []

    for row in df.itertuples():
        cs = (row.raceId, row.constructorId, row.position, row.points, row.wins)
        constructor_standings.append(cs)

    sql = '''
        INSERT INTO constructor_standings (raceId, constructorId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''
    cur.executemany(sql, constructor_standings)

def fill_table(cur):
    fill_intermediate_cs_table(cur)

    sql = '''
        INSERT INTO constructor_season (constructorId, year, points, position, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''

    for year in range(1950, 2023):
        cur.execute('''
            SELECT constructorId, races.season, points, position, wins
            FROM constructor_standings 
            INNER JOIN races ON races.id = constructor_standings.raceId
            WHERE races.season = ''' + str(year) 
            + ''' GROUP BY constructorId
            HAVING MAX(points)'''


        # constructor_seasons = []

        # for row in cur.fetchall():
        #     print(row)
        #     constructor_seasons.append(row)

        # cur.executemany(sql, constructor_seasons)