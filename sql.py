import sqlite3 as sql

with sql.connect("rail.db") as con:
    cur = con.cursor()

    cur.execute("DROP TABLE if EXISTS passengers")
    cur.execute("CREATE TABLE passengers ("
                "passenger_id INTEGER PRIMARY KEY,"
                "lname varchar(40) NOT NULL,"
                "email varchar(40) NOT NULL,"
                "billing_addr text DEFAULT NULL,"
                "payment char(16) NOT NULL)")

    cur.execute("DROP TABLE if EXISTS segments")
    cur.execute("CREATE TABLE segments ("
                "segment_id INTEGER PRIMARY KEY,"
                "seg_northend int DEFAULT NULL,"
                "seg_southend int DEFAULT NULL,"
                "far decimal(7,2) NOT NULL )")

    cur.execute("DROP TABLE if EXISTS seats_free")
    cur.execute("CREATE TABLE seats_free ("
                "train_num int NOT NULL,"
                "sf_segment_id int NOT NULL,"
                "sf_date DEFAULT NULL,"
                "sf_free int NOT NULL,"
                "FOREIGN KEY (train_num) REFERENCES trains (train_num),"
                "FOREIGN KEY (sf_segment_id) REFERENCES segments (segment_id)"
                ")")

    cur.execute("DROP TABLE if EXISTS stations")
    cur.execute("CREATE TABLE stations ("
                "station_id INTEGER PRIMARY KEY,"
                "station_name text NOT NULL,"
                "station_symbol char(5) NOT NULL )")

    cur.execute("DROP TABLE if EXISTS stops_at")
    cur.execute("CREATE TABLE stops_at ("
                "train_id int DEFAULT NULL,"
                "station_id int DEFAULT NULL,"
                "time_in timestamp NOT NULL,"
                "time_out timestamp NOT NULL )")

    cur.execute("DROP TABLE if EXISTS trains")
    cur.execute("CREATE TABLE trains ("
                "train_num int NOT NULL,"
                "train_starts int NOT NULL,"
                "train_ends int NOT NULL,"
                "train_direction boolean NOT NULL )")

    cur.execute("DROP TABLE if EXISTS trips")
    cur.execute("CREATE TABLE trips ("
                "trid_id int INTEGER PRIMARY KEY,"
                "trip_date date DEFAULT NULL,"
                "trip_start int NOT NULL,"
                "trip_end int NOT NULL,"
                "train_id int NOT NULL,"
                "passenger_id int NOT NULL,"
                "trip_fare decimal(7,2) NOT NULL,"
                "payment_method boolean NOT NULL, "
                "FOREIGN KEY (train_id) REFERENCES trains (train_num),"
                "FOREIGN KEY (trip_start) REFERENCES segments (segment_id),"
                "FOREIGN KEY (trip_end) REFERENCES segments (segment_id),"
                "FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id))")

    # data for stations
    cur.execute("""INSERT INTO stations (station_id, station_name, station_symbol) VALUES
                (1, 'Boston - South Station, MA', 'BOS'),
                (2, 'Boston - Back Bay Station, MA', 'BBY'),
                (3, 'Route 128, MA', 'RTE'),
                (4, 'Providence, RI', 'PVD'),
                (5, 'Kingston, RI', 'KIN'),
                (6, 'Westerly, RI', 'WLY'),
                (7, 'Mystic, CT', 'MYS'),
                (8, 'New London, CT', 'NLC'),
                (9, 'Old Saybrook, CT', 'OSB'),
                (10, 'New Haven, CT', 'NHV'),
                (11, 'Bridgeport, CT', 'BRP'),
                (12, 'Stamford, CT', 'STM'),
                (13, 'New Rochelle, NY', 'NRO'),
                (14, 'New York - Penn Station, NY', 'NYP'),
                (15, 'Newark, NJ', 'NWK'),
                (16, 'Newark - International Airport', 'EWR'),
                (17, 'Metropark, NJ', 'MET'),
                (18, 'Trenton, NJ', 'TRE'),
                (19, 'Philadelphia - 30th Street Sta', 'PHL'),
                (20, 'Wilmington - Joseph R. Biden J', 'WIL'),
                (21, 'Aberdeen, MD', 'ABE'),
                (22, 'Baltimore - Penn Station, MD', 'BAL'),
                (23, 'BWI Marshall Airport, MD', 'BWI'),
                (24, 'New Carrollton, MD', 'NCR'),
                (25, 'Washington - Union Station, DC', 'WAS'),
                (26, 'Boston - North Station', 'BON'),
                (27, 'Woburn - Anderson, MA', 'WOB'),
                (28, 'Haverhill, MA', 'HAV'),
                (29, 'Exeter, NH', 'EXE'),
                (30, 'Durnham - UNH, NH', 'DUR'),
                (31, 'Dover - NH', 'DOV'),
                (32, 'Wells - ME', 'WEL'),
                (33, 'Saco, ME', 'SAC'),
                (34, 'Old Orchard Beach, ME', 'OOB'),
                (35, 'Portland, ME', 'POR')""")

    # data for TRAINS
    cur.execute("""INSERT INTO trains VALUES
                (1,1,25,0),
                (2,1,25,0),
                (3,1,25,0),
                (4,1,25,0),
                (5,1,25,0),
                (6,1,25,0),
                (7,1,25,0),
                (8,1,25,0),
                (9,1,25,0),
                (10,1,25,0),
                (11,1,25,0),
                (12,1,25,0),
                (13,1,25,0),
                (14,1,25,0),
                (15,1,25,0),
                (16,25,1,1),
                (17,25,1,1),
                (18,25,1,1),
                (19,25,1,1),
                (20,25,1,1),
                (21,25,1,1),
                (22,25,1,1),
                (23,25,1,1),
                (24,25,1,1),
                (25,25,1,1),
                (26,25,1,1),
                (27,25,1,1),
                (28,25,1,1),
                (29,25,1,1),
                (30,25,1,1),
                (31,26,35,0),
                (32,26,35,0),
                (33,26,35,0),
                (34,26,35,0),
                (35,26,35,0),
                (36,35,26,1),
                (37,35,26,1),
                (38,35,26,1),
                (39,35,26,1),
                (40,35,26,1)""")

    # data for segments
    cur.execute("""INSERT INTO segments VALUES
    (1,35,2,1.00),
    (2,1,3,1.00),
    (3,2,4,1.00),
    (4,3,5,1.00),
    (5,4,6,1.00),
    (6,5,7,1.00),
    (7,6,8,1.00),
    (8,7,9,1.00),
    (9,8,10,1.00),
    (10,9,11,1.00),
    (11,10,12,1.00),
    (12,11,13,1.00),
    (13,12,14,1.00),
    (14,13,15,1.00),
    (15,14,16,1.00),
    (16,15,17,1.00),
    (17,16,18,1.00),
    (18,17,19,1.00),
    (19,18,20,1.00),
    (20,19,21,1.00),
    (21,20,22,1.00),
    (22,21,23,1.00),
    (23,22,24,1.00),
    (24,23,25,1.00),
    (25,24,NULL,1.00),
    (26,NULL,27,1.00),
    (27,26,28,1.00),
    (28,27,29,1.00),
    (29,28,30,1.00),
    (30,29,31,1.00),
    (31,30,32,1.00),
    (32,31,33,1.00),
    (33,32,34,1.00),
    (34,33,35,1.00),
    (35,34,1,1.00)""")

