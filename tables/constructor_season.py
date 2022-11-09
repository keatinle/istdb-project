import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/constructor_standings.csv')
    df = pd.DataFrame(data)

    constructor_seasons = []
    sql = '''
        INSERT INTO constructor_standings(year, constructorId, position, points, wins)
        VALUES (%s, %s, %s, %s, %s)
        '''

    for row in df.itertuples():
        cur.execute('''SELECT races.season FROM races where races.id = ''' + str(row.raceId))
        year = cur.fetchone()[0]

        cs = (year, row.constructorId, row.position, row.points, row.wins)
        constructor_seasons.append(cs)

    cur.executemany(sql, constructor_seasons)

