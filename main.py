import sqlite3
import pandas as pd

def csv_to_db():
    df = pd.read_csv('Dataset_NQ_1min_2022_2025.csv')

    connection = sqlite3.connect('NQ_Futures.db')

    df.rename(columns={'timestamp ET': 'timestampET'}, inplace=True)

    df.set_index('timestampET', inplace=True)

    cursor = connection.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS NQ_1m
                   (
                       timestampET TEXT PRIMARY KEY,
                       open        REAL,
                       high        REAL,
                       low         REAL,
                       close       REAL,
                       volume      INTEGER,
                       Vwap_RTH    REAL,
                       Vwap_ETH    REAL
                   );
                   ''')

    for row in df.itertuples():
        cursor.execute('''
                INSERT OR REPLACE INTO NQ_1m (timestampET, open, high, low, close, volume, Vwap_RTH, Vwap_ETH) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       row)

    connection.commit()
    connection.close()


if __name__ == '__main__':
    csv_to_db()