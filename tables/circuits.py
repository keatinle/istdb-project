import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/circuits.csv')
    df = pd.DataFrame(data)

    circuits = []

    for row in df.itertuples():
        circuit = (row.circuitId, row.name, row.country, row.location, row.alt)
        circuits.append(circuit)

    sql = '''
        INSERT INTO circuits (id, name, country, city, altitude)
        VALUES (%s, %s, %s, %s, %s)
        '''
    
    cur.executemany(sql, circuits)