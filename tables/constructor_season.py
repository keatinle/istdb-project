import pandas as pd
from pandasql import sqldf

def fill_table(cur):
    data = pd.read_csv(r'./data/constructor_standings.csv')
    df = pd.DataFrame(data)
    
    data = pd.read_csv(r'./data/races.csv')
    races = pd.DataFrame(data)

    constructor_seasons = []
    sql = '''
        INSERT INTO constructor_standings(year, constructorId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''

    for num in range(1950, 2023):

        q = """SELECT races.year, constructorId, position, MAX(points) as max, wins 
            FROM df
            INNER JOIN races ON races.raceid = df.raceId 
            WHERE races.year = """ + str(num) + " GROUP BY constructorId ORDER BY max DESC, wins DESC"

        fixed_df = sqldf(q, locals())

        for row in fixed_df.itertuples(index=True):
            cs = (row.year, row.constructorId, row.Index + 1, row.max, row.wins)
            constructor_seasons.append(cs)

    cur.executemany(sql, constructor_seasons)
