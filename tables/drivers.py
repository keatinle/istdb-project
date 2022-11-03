import pandas as pd

def create_driver(cur, driver):
    sql = '''
        INSERT INTO drivers (id, forename, surname, dob, nationality)
        VALUES (?,?,?,?,?)
        '''
    cur.execute(sql, driver)

def fill_table(cursor):
    data = pd.read_csv(r'./data/drivers.csv')
    df = pd.DataFrame(data)

    for row in df.itertuples():
        driver = (row.driverId, row.forename, row.surname, row.dob, row.nationality)
        create_driver(cursor, driver)
