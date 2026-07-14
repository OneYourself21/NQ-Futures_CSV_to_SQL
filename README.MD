An online kaggle source had 2022-2025 NQ Futures data stored in a csv. This project converts it to a sqlite database.

To use the project:
Insert the csv file from: https://www.kaggle.com/datasets/tgtanalytics/nq-futures-1min-bar-2022-2025?resource=download
Make sure the name of the file is Dataset_NQ_1min_2022_2025.csv
Then run the program, and you shall receive a sqlite database version where the timestamp is the primary key called NQ_Futures

Note the time is saved in ET.

Findings:

There are 734 candles with a time of exactly 17:00 but none else in the 17:00 to 18:00. The dataset in empty between those ranges.
To check yourself the hour_count_test has been saved.
Otherwise, amount of candles in each hour is mostly the same with a few slight negligible differences.

We expect if there is not 17:00 candles that we will have 1380 candles per trading day. (from 18:00→17:00).
Running candles_per_day_test we find that 640 days out of 3 years do but not all do. a dict for number of candles a day and their relative frequency shall be posted below.
{1380: 640, 1379: 63, 1378: 17, 1139: 2, 1140: 16, 1203: 1, 1260: 1, 913: 1, 1375: 5, 1155: 5, 1138: 2, 1377: 3, 1371: 1, 1373: 1, 1137: 1, 1370: 1, 1372: 2, 930: 1, 1362: 1, 1154: 1, 508: 1, 172: 1}
From this we see 80 days missing a candle or too which doesn't seem that bad but in the 900s or even 500 and 172 is bad, so I went ahead and searched for those specific dates.
NOTE: most events happened a day after.
For 172:
-This was the last day in the dataset 2025-12-11 18:01 to 2025-12-11 20:52
For 508:
-Thanksgiving day caused it to end earlier than usual. (2025-11-27)
For 913:
-Thursday before good friday. (2023-04-06)
For 930
-National Day of Mourning for Jimmy Carter. (2025-01-08)
For between 1000-1300:
-All were holidays and the dates were:
[('2023-01-15 18:01:00',), ('2023-02-19 18:01:00',), ('2023-04-04 18:01:00',), ('2023-04-05 20:01:00',), ('2023-05-28 18:01:00',), ('2023-06-18 18:01:00',), ('2023-07-02 18:01:00',), ('2023-07-03 18:01:00',), ('2023-09-03 18:01:00',), ('2023-11-22 18:01:00',), ('2023-11-23 18:01:00',), ('2024-01-14 18:01:00',), ('2024-02-18 18:01:00',), ('2024-05-26 18:01:00',), ('2024-06-18 18:01:00',), ('2024-07-02 18:01:00',), ('2024-07-03 18:01:00',), ('2024-09-01 18:01:00',), ('2024-11-27 18:01:00',), ('2024-11-28 18:01:00',), ('2024-12-23 18:01:00',), ('2025-01-08 18:01:00',), ('2025-01-19 18:01:00',), ('2025-02-16 18:01:00',), ('2025-05-25 18:01:00',), ('2025-06-18 18:01:00',), ('2025-07-02 18:01:00',), ('2025-07-03 18:01:00',), ('2025-08-31 18:01:00',), ('2025-11-26 18:01:00',)]


