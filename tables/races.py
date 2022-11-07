import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/races.csv')
    df = pd.DataFrame(data)

    races = []

    for row in df.itertuples():
        race = (row.raceId, row.name, row.circuitId, row.year, row.round, row.date)
        races.append(race)

    sql = '''
        INSERT INTO races (id, name, circuitId, season, round, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
    cur.executemany(sql, races)