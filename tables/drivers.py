import pandas as pd

def fill_table(cur):
    data = pd.read_csv(r'./data/drivers.csv')
    df = pd.DataFrame(data)

    drivers = []

    for row in df.itertuples():
        driver = (row.driverId, row.forename, row.surname, row.dob, row.nationality)
        drivers.append(driver)

    sql = '''
        INSERT INTO drivers (id, forename, surname, dob, nationality)
        VALUES (%s, %s, %s, %s, %s)
        '''
    cur.executemany(sql, drivers)