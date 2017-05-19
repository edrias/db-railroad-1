from datetime import date, timedelta
import datetime
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
                "time_in time NOT NULL,"
                "time_out time NOT NULL )")

    cur.execute("DROP TABLE if EXISTS trains")
    cur.execute("CREATE TABLE trains ("
                "train_num int NOT NULL,"
                "train_starts int NOT NULL,"
                "train_ends int NOT NULL,"
                "train_direction boolean NOT NULL,"
                "day tinyint(1) NOT NULL)")

    cur.execute("DROP TABLE if EXISTS trips")
    cur.execute("CREATE TABLE trips ("
                "trip_id int INTEGER PRIMARY KEY,"
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
                (1, 'Portland, ME', 'POR'),
                (2, 'Old Orchard Beach, ME', 'OOB'),
                (3, 'Saco, ME', 'SAC'),
                (4, 'Wells - ME', 'WEL'),
                (5, 'Dover - NH', 'DOV'),
                (6, 'Durnham - UNH, NH', 'DUR'),
                (7, 'Exeter, NH', 'EXE'),
                (8, 'Haverhill, MA', 'HAV'),
                (9, 'Woburn - Anderson, MA', 'WOB'),
                (10, 'Boston - North Station', 'BON'),
                (11, 'Boston - South Station, MA', 'BOS'),
                (12, 'Boston - Back Bay Station, MA', 'BBY'),
                (13, 'Route 128, MA', 'RTE'),
                (14, 'Providence, RI', 'PVD'),
                (15, 'Kingston, RI', 'KIN'),
                (16, 'Westerly, RI', 'WLY'),
                (17, 'Mystic, CT', 'MYS'),
                (18, 'New London, CT', 'NLC'),
                (19, 'Old Saybrook, CT', 'OSB'),
                (20, 'New Haven, CT', 'NHV'),
                (21, 'Bridgeport, CT', 'BRP'),
                (22, 'Stamford, CT', 'STM'),
                (23, 'New Rochelle, NY', 'NRO'),
                (24, 'New York - Penn Station, NY', 'NYP'),
                (25, 'Newark, NJ', 'NWK'),
                (26, 'Newark - International Airport', 'EWR'),
                (27, 'Metropark, NJ', 'MET'),
                (28, 'Trenton, NJ', 'TRE'),
                (29, 'Philadelphia - 30th Street Sta', 'PHL'),
                (30, 'Wilmington - Joseph R. Biden J', 'WIL'),
                (31, 'Aberdeen, MD', 'ABE'),
                (32, 'Baltimore - Penn Station, MD', 'BAL'),
                (33, 'BWI Marshall Airport, MD', 'BWI'),
                (34, 'New Carrollton, MD', 'NCR'),
                (35, 'Washington - Union Station, DC', 'WAS')""")

    # data for TRAINS
    #12 Trains going north and 12 going south on weekdays, 5 trains going north and 5 going south on weekend.
    #(train_num,start_station,end_station, direction, weekend/weekday)
    cur.execute("""INSERT INTO trains VALUES
                (1,1,35,0,1),
                (2,1,35,0,1),
                (3,1,35,0,1),
                (4,1,35,0,1),
                (5,1,35,0,1),
                (6,1,35,0,1),
                (7,1,35,0,1),
                (8,1,35,0,1),
                (9,1,35,0,1),
                (10,1,35,0,1),
                (11,1,35,0,1),
                (12,1,35,0,1),
                (13,35,1,1,1),
                (14,35,1,1,1),
                (15,35,1,1,1),
                (16,35,1,1,1),
                (17,35,1,1,1),
                (18,35,1,1,1),
                (19,35,1,1,1),
                (20,35,1,1,1),
                (21,35,1,1,1),
                (22,35,1,1,1),
                (23,35,1,1,1),
                (24,35,1,1,1),
                (25,1,35,0,0),
                (26,1,35,0,0),
                (27,1,35,0,0),
                (28,1,35,0,0),
                (29,1,35,0,0),
                (30,1,35,0,0),
                (31,35,1,1,0),
                (32,35,1,1,0),
                (33,35,1,1,0),
                (34,35,1,1,0),
                (35,35,1,1,0)""")

    #8 trains going north mon-fri
    # data for segments
    cur.execute("""INSERT INTO segments VALUES
    (1,NULL,2,10.00),
    (2,1,3,12.00),
    (3,2,4,13.00),
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
    (25,24,26,1.00),
    (26,25,27,1.00),
    (27,26,28,1.00),
    (28,27,29,1.00),
    (29,28,30,1.00),
    (30,29,31,1.00),
    (31,30,32,1.00),
    (32,31,33,1.00),
    (33,32,34,1.00),
    (34,33,35,1.00),
    (35,34,NULL,1.00)""")



    #SEATS FREE PYTHON SCRIPT#
    d1 = date(2017,5,1)
    d2 = date(2018,5,1)

    delta = d2 - d1
    days = []

    for i in range(delta.days+1):
        days.append(d1 + timedelta(days=i))

    weekend =[]
    weekday = []
    #get weekdays and weekends
    for x in range(len(days)):
        if x%7==5 or x%7==6:#sat/sunday
            weekend.append(str(days[x]))
        else:
            weekday.append(str(days[x]))

    #insert to weekdays
    for i in range(len(weekday)):
        for j in range(1,25):
                cur.execute("INSERT INTO seats_free (train_num,sf_segment_id,sf_date,sf_free)"
                            "VALUES(?,?,?,?)",(j,j,weekday[i],448))


    #insert into weekends
    for i in range(len(weekend)):
        count = 1
        for j in range(0,11):
            print(weekend[j])

            cur.execute("INSERT INTO seats_free (train_num,sf_segment_id,sf_date,sf_free)"
                        "VALUES(?,?,?,?)",(j+25, j+25, weekend[i], 448))
            count+=1


    #stops_at data
    #exmaple: train 1 stops at station 2 at 9:30AM, time out 9:33:
    now = datetime.datetime(2017,5,1,5,0)# for time_in
    now1 = datetime.datetime(2017,5,1,5,0)# for time_out
    end = now+datetime.timedelta(hours = 24)
    time_in =[]
    time_out = []
    #time_out = []
    while now <=end:
        time_in.append(now)
        time_out.append(now1)
        now1= now + datetime.timedelta(minutes=18)
        now+=datetime.timedelta(minutes=15)

    time_in = [t.strftime("%H:%M") for t in time_in]
    time_out = [t.strftime("%H:%M") for t in time_out]



    for y in range(1,36):
        for z in range(1,36):
            cur.execute("INSERT INTO stops_at (train_id,station_id,time_in,time_out) VALUES"
                            "(?,?,?,?)",(y,z,time_in[z+y],time_out[z+y]))


    #end of stops_at data. ( I think this will work -Eddy.S)


