import pandas as pd

def create_circuit(cur, circuit):
    sql = '''
        INSERT INTO circuits (id, name, country, city, altitude)
        VALUES (?, ?, ?, ?, ?)
        '''
    cur.execute(sql, circuit)

def fill_table(cur):
    data = pd.read_csv(r'./data/circuits.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        circuit = (row.circuitId, row.name, row.country, row.location, row.alt)
        create_circuit(cur, circuit)
