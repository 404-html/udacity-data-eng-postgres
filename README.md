# Data Modeling with Postgres

## Purpose

A fictitious startup called Sparkify wants to use song and user data to analyze song and user activities. The purpose of this project is to create an ETL pipeline that can use song and user data to create a Postgres database optimized for queries based on song plays.

## Dataset

The raw data comes in two types of files:
1. User activity in the form of JSON files. Sample entry: 
```
{
    "artist":null,
    "auth":"LoggedIn",
    "firstName":"Walter",
    "gender":"M",
    "itemInSession":0,
    "lastName":"Frye",
    "length":null,
    "level":"free",
    "location":"San Francisco-Oakland-Hayward, CA",
    "method":"GET",
    "page":"Home",
    "registration":1540919166796.0,
    "sessionId":38,
    "song":null,
    "status":200,
    "ts":1541105830796,
    "userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
    "userId":"39"
}
```
2. Song and artist data in the form of JSON files. Sample entry:
```
{
    "num_songs": 1, 
    "artist_id": "ARD7TVE1187B99BFB1", 
    "artist_latitude": null, 
    "artist_longitude": null, 
    "artist_location": "California - LA", 
    "artist_name": "Casual", 
    "song_id": "SOMZWCG12A8C13C480", 
    "title": "I Didn't Mean To", 
    "duration": 218.93179, 
    "year": 0
}
```

## Schema

We will use a star schema optimized for queries on song analyses. The fact table `songplays` consists of:
- `songplay_id` (primary key)
- `start_time`
- `user_id`
- `level`
- `song_id`
- `artist_id`
- `session_id`
- `location`
- `user_agent`
The first dimension table `users` consists of:
- `user_id` (primary key)
- `first_name`
- `last_name`
- `gender`
- `level`
The second dimension table `songs` consists of:
- `song_id` (primary key)
- `title`
- `artist_id`
- `year`
- `duration`
The third dimension table `artists` consists of:
- `artist_id` (primary key)
- `name`
- `location`
- `latitude`
- `longitude`
The fourth dimension table `time` consists of:
- `start_time` (primary key)
- `hour`
- `day`
- `week`
- `month`
- `year`
- `weekday`

## ETL Pipeline

The pipeline is described below:
1. Raw user and song data provided in JSON files (see Dataset section)
2. For each song file, perform the following:
    + Open as a Pandas dataframe
    + Insert song data into `songs` table (drop duplicates) First three rows:
    ```
          song_id       |              title              |     artist_id      | year | duration
    --------------------+---------------------------------+--------------------+------+-----------
     SOFNOQK12AB01840FC | Kutt Free (DJ Volume Remix)     | ARNNKDK1187B98BBD5 | 0    | 407.37914
     SOBAYLL12A8C138AF9 | Sono andati? Fingevo di dormire | ARDR4AC1187FB371A1 | 0    | 511.16363
     SOFFKZS12AB017F194 | A Higher Place (Album Version)  | ARBEBBY1187B9B43DB | 1994 | 236.17261
    ```
    + Insert artist data in `artists` table (drop duplicates). First three rows:
    ```
         artist_id      |                         name                          |    location     | latitude |     longitude
    --------------------+-------------------------------------------------------+-----------------+----------+-------------------
     ARNNKDK1187B98BBD5 | Jinx                                                  | Zagreb Croatia  | 45.80726 | 15.96760000000000.
                        |                                                       |                 |          |.1
     ARDR4AC1187FB371A1 | Montserrat Caballé;Placido Domingo;Vicente Sardinero. |                 | NaN      | NaN
                        |.;Judith Blegen;Sherrill Milnes;Georg Solti            |                 |          |
     ARBEBBY1187B9B43DB | Tom Petty                                             | Gainesville, FL | NaN      | NaN
     ```
3. For each user log file, perform the following:
    + Open as a Pandas dataframe
    + Filter out all entries that do not have `Page=NextSong` keyword
    + Convert the timestamp column to datetime format and extract hour, day, week, month, year and day-of-the-week information
    + Insert timestamp data into `time` table. First three rows:
    ```
           start_time        | hour | day | week | month | year | weekday
    -------------------------+------+-----+------+-------+------+---------
     2018-11-29 00:00:57.796 | 0    | 29  | 48   | 11    | 2018 | 3
     2018-11-29 00:01:30.796 | 0    | 29  | 48   | 11    | 2018 | 3
     2018-11-29 00:04:01.796 | 0    | 29  | 48   | 11    | 2018 | 3
    ```
    + Insert user data into `user` table. First three rows:
    ```
     user_id | first_name | last_name | gender | level
    ---------+------------+-----------+--------+-------
     54      | Kaleb      | Cook      | M      | free
     79      | James      | Martin    | M      | free
     78      | Chloe      | Roth      | F      | free
    ```
    + Find song and artist IDs from previous `songs` and `artists` tables
    + Insert songplay data into `songplays` table. First three rows:
    ```
     songplay_id |  start_time  | user_id | level | song_id | artist_id | session_id |        location         | user_agent
    -------------+--------------+---------+-------+---------+-----------+------------+-------------------------+------------
               1 | 154344965779.| 73      | paid  |         |           | 954        | Tampa-St. Petersburg-Cl.| "Mozilla/5.
                 |.6            |         |       |         |           |            |.earwater, FL            |..0 (Macint.
                 |              |         |       |         |           |            |                         |.osh; Intel.
                 |              |         |       |         |           |            |                         |. Mac OS X .
                 |              |         |       |         |           |            |                         |.10_9_4) Ap.
                 |              |         |       |         |           |            |                         |.pleWebKit/.
                 |              |         |       |         |           |            |                         |.537.78.2 (.
                 |              |         |       |         |           |            |                         |.KHTML, lik.
                 |              |         |       |         |           |            |                         |.e Gecko) V.
                 |              |         |       |         |           |            |                         |.ersion/7.0.
                 |              |         |       |         |           |            |                         |..6 Safari/.
                 |              |         |       |         |           |            |                         |.537.78.2"
               2 | 154344969079.| 24      | paid  |         |           | 984        | Lake Havasu City-Kingma.| "Mozilla/5.
                 |.6            |         |       |         |           |            |.n, AZ                   |..0 (Window.
                 |              |         |       |         |           |            |                         |.s NT 6.1; .
                 |              |         |       |         |           |            |                         |.WOW64) App.
                 |              |         |       |         |           |            |                         |.leWebKit/5.
                 |              |         |       |         |           |            |                         |.37.36 (KHT.
                 |              |         |       |         |           |            |                         |.ML, like G.
                 |              |         |       |         |           |            |                         |.ecko) Chro.
                 |              |         |       |         |           |            |                         |.me/36.0.19.
                 |              |         |       |         |           |            |                         |.85.125 Saf.
                 |              |         |       |         |           |            |                         |.ari/537.36.
                 |              |         |       |         |           |            |                         |."
               3 | 154344984179.| 24      | paid  |         |           | 984        | Lake Havasu City-Kingma.| "Mozilla/5.
                 |.6            |         |       |         |           |            |.n, AZ                   |..0 (Window.
                 |              |         |       |         |           |            |                         |.s NT 6.1; .
                 |              |         |       |         |           |            |                         |.WOW64) App.
                 |              |         |       |         |           |            |                         |.leWebKit/5.
                 |              |         |       |         |           |            |                         |.37.36 (KHT.
                 |              |         |       |         |           |            |                         |.ML, like G.
                 |              |         |       |         |           |            |                         |.ecko) Chro.
                 |              |         |       |         |           |            |                         |.me/36.0.19.
                 |              |         |       |         |           |            |                         |.85.125 Saf.
                 |              |         |       |         |           |            |                         |.ari/537.36.
                 |              |         |       |         |           |            |                         |."
    ```

## Build Instructions

Perform the following to execute the ETL pipeline:
1. Create the Sparkify database and tables: `python create_tables.py`
2. Run the ETL pipeline: `python etl.py`
3. Verify the tables have been populated by running the `etl.ipynb` Jupyter notebook