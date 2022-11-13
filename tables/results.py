import pandas as pd

def fill_table(cur):
    statuses = pd.read_csv(r'./data/status.csv')
    statusdict = {}

    for row in statuses.itertuples():
        statusdict[row.statusId] = row.status

    data = pd.read_csv(r'./data/results.csv')
    df = pd.DataFrame(data)

    results = []

    for row in df.itertuples():
        position = row.position if row.position != '\\N' else None
        fastestLap = row.fastestLap if row.fastestLap != '\\N' else None

        result = (row.resultId, 
                row.raceId, 
                row.driverId,
                row.constructorId,
                row.grid,
                position,
                row.points,
                fastestLap,
                statusdict[row.statusId])

        results.append(result)

    sql = '''
        INSERT INTO results (id, raceId, driverId, constructorId, grid, position, points, fastestLap, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
    cur.executemany(sql, results)