import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/constructors.csv')
    df = pd.DataFrame(data)

    constructors = []

    for row in df.itertuples():
        constructor = (row.constructorId, row.name, row.nationality)
        constructors.append(constructor)

    sql = '''
        INSERT INTO constructors (id, name, nationality)
        VALUES (%s, %s, %s)
        '''
    cur.executemany(sql, constructors)