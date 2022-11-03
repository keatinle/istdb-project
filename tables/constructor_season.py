import pandas as pd

def create_constructor_standing(cur, constructor):
    sql = '''
        INSERT INTO constructor_standings (raceId, constructorId, position, points, wins)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, constructor)

def fill_cs_table(cur):
    data = pd.read_csv(r'./data/constructor_standings.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        cs = (row.raceId, row.constructorId, row.position, row.points, row.wins)
        create_constructor_standing(cur, cs)


def create_constructor_season(cur, con_sea):
    sql = '''
        INSERT INTO constructor_season (year, constructorId, position, points, wins)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, con_sea)

def fill_table(cur):
    fill_cs_table(cur)

    for num in range(1950, 2023):
        cur.execute('''
            SELECT races.season, constructorId, position, MAX(points), wins FROM constructor_standings
            INNER JOIN races ON races.id = constructor_standings.raceId
            WHERE races.season = ''' 
            + str(num)
            + ' GROUP BY constructorId')
