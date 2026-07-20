import sqlite3
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

#timestampET = 0
#open = 1
#high = 2
#low = 3
#close = 4
#volume = 5
#Vwap_RTH = 6
#Vwap_ETH = 7

def csv_to_db():
    df = pd.read_csv('Dataset_NQ_1min_2022_2025.csv')

    connection = sqlite3.connect('NQ_Futures.db')

    df.rename(columns={'timestamp ET': 'timestampET'}, inplace=True)

    df['timestampET'] = pd.to_datetime(df['timestampET']) #converts M/D/Y Hour:Mins to a date time object
    df['timestampET'] = df['timestampET'].dt.strftime('%Y-%m-%d %H:%M:%S') #back to string :D

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


def read_date_to_date(starting_date : dt.datetime, ending_date : dt.datetime) -> list:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    starting_date = starting_date.strftime('%Y-%m-%d %H:%M:%S')
    ending_date = ending_date.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(''' SELECT * FROM NQ_1m WHERE timestampET >= ? AND timestampET <= ?;
    ''', (starting_date, ending_date))

    rows = cursor.fetchall()

    connection.close()
    return rows


def zero_volume_test() -> int:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT *
                      FROM NQ_1m
                      WHERE volume == 0;''')

    rows = cursor.fetchall()

    connection.close()
    return len(rows)


def hour_count_test() -> list:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    hours_amount = []

    cursor.execute('''SELECT COUNT(*) 
                          FROM NQ_1m
                          GROUP BY strftime('%H', timestampET);''')

    counts = cursor.fetchall()
    for i in range(24):
        print(f"Hour {i} length:  {counts[i][0]}")


    hours_amount.extend(counts)

    cursor.execute(''' SELECT COUNT(*) 
                       FROM NQ_1m
                       WHERE strftime('%H:%M', timestampET) == '17:00';''')
    five_vol = cursor.fetchone()[0]
    print(f"Note that number of 17:00 candles is {five_vol}.")

    connection.close()
    return hours_amount


def candle_per_day_test() -> dict:
    n_dict = {}

    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    cursor.execute(''' SELECT COUNT(*) 
                       FROM NQ_1m
                       GROUP BY strftime('%Y-%m-%d', timestampET, '+6 hours');''')

    counts = cursor.fetchall()
    for count in counts:
        if n_dict.keys().__contains__(count[0]):
            n_dict[count[0]] += 1

        else:
            n_dict.update({count[0]: 1})

    connection.close()
    return n_dict

def test_a_day(n : int) -> list:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    cursor.execute(''' SELECT timestampET
                           FROM NQ_1m
                           GROUP BY strftime('%Y-%m-%d', timestampET, '+6 hours')
                           HAVING COUNT(*) >= ?;''', (n,))

    rows = cursor.fetchall()
    connection.close()
    return rows


def holidays() -> list:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    cursor.execute(''' SELECT timestampET
                       FROM NQ_1m
                       GROUP BY strftime('%Y-%m-%d', timestampET, '+6 hours')
                       HAVING (COUNT(*) >= 1000) AND (COUNT(*)) <= 1300;''')

    rows = cursor.fetchall()
    connection.close()
    return rows


def find_jumps(diff : int) -> list:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()

    cursor.execute(''' SELECT close, sub.next_open, timestampET, sub.next_timestampET
                       FROM (SELECT timestampET,
                                    close,
                                    LEAD(timestampET) OVER (ORDER BY timestampET) AS next_timestampET,
                                    LEAD(open) OVER (ORDER BY timestampET) AS next_open
                           FROM NQ_1m
                            ) sub
                       WHERE (sub.close + ? < sub.next_open) OR (sub.close - ? > sub.next_open);
                       ''', (diff, diff,))



    rows = cursor.fetchall()
    print(rows)
    print(len(rows))
    connection.close()
    return rows


def plot_rolling_period() -> None:
    connection = sqlite3.connect('NQ_Futures.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT timestampET, open, close, volume
                       FROM NQ_1m
                       WHERE strftime('%Y/%m', timestampET) == '2023/03';
                   ''')

    rows = cursor.fetchall()
    connection.close()
    timestampET, open, close, volume = [],[],[],[]

    for row in rows:
        timestampET.append(row[0])
        open.append(row[1])
        close.append(row[2])
        volume.append(row[3])

    fig, ax = plt.subplots()

    ax.plot(timestampET, open, label = 'open')
    ax.plot(timestampET, close, label = 'close')
    ax.plot(timestampET, volume, label = 'volume')
    print(close)
    plt.show()
    connection.close()



if __name__ == '__main__':
    plot_rolling_period()