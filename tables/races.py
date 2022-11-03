import pandas as pd

def create_race(cur, race):
    sql = '''
        INSERT INTO races (id, name, circuitId, season, round, date)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
    cur.execute(sql, race)

def fill_table(cur):
    data = pd.read_csv(r'./data/races.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        race = (row.raceId, row.name, row.circuitId, row.year, row.round, row.date)
        create_race(cur, race)
