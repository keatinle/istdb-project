import pandas as pd

def create_constructor(cur, constructor):
    sql = '''
        INSERT INTO constructors (id, name, nationality)
        VALUES (?, ?, ?)
        '''
    cur.execute(sql, constructor)

def fill_table(cur):
    data = pd.read_csv(r'./data/constructors.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        constructor = (row.constructorId, row.name, row.nationality)
        create_constructor(cur, constructor)
