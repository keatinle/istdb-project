import pandas as pd

def create_result(cur, result):
    sql = '''
        INSERT INTO results (id, raceId, driverId, constructorId, grid, position, points, fastestLap, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    cur.execute(sql, result)

def fill_table(cur):
    statuses = pd.read_csv(r'./data/status.csv')
    statusdict = {}

    for row in statuses.itertuples():
        statusdict[row.statusId] = row.status

    data = pd.read_csv(r'./data/results.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        result = (row.resultId, 
                row.raceId, 
                row.driverId,
                row.constructorId,
                row.grid,
                row.position,
                row.points,
                row.fastestLap,
                statusdict[row.statusId])
        create_result(cur, result)