import sqlite3
import datetime
import datetime as dt
from ast import literal_eval

def get_stations():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from stations')
    stations = cursor.fetchall()
    return stations


def get_passengers_table():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from passengers')
    return  cursor.fetchall()


def get_trips_table():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from trips')
    return  cursor.fetchall()


def get_all_seats_free():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from seats_free')
    return cursor.fetchall()

#returns a tuple with the outgoing and destination stations names.
def get_destination_stations(outgoing_station,destination_station):
    db= sqlite3.connect('rail.db')
    cursor = db.cursor()
    start = cursor.execute("SELECT station_name FROM stations WHERE station_id = '{}'".format(outgoing_station)).fetchone()
    end =  cursor.execute("SELECT station_name FROM stations WHERE station_id = '{}'".format(destination_station)).fetchone()
    result = (start[0],end[0])
    return result

#displays all avaiable traings +/- 30 minutes
def get_one_way_trip(dep_date,dep_time,outgoing_station,destination_station):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()

    #time range
    time_range = get_time_range(dep_time)

    #need to get train direction.
    direction = get_direction((int(outgoing_station)),int(destination_station))

    #this query gets the train_id, date, and departure time for the trip. It checks for a time range, in case there is no
    # exact match. It also only gets the trains going a certain direction.
    if get_seats_free(outgoing_station,destination_station,dep_date,tickets=0) == True:
        results = cursor.execute("SELECT seats_free.train_num, seats_free.sf_date, stops_at.time_in FROM seats_free INNER JOIN stops_at ON "
                            "seats_free.train_num = stops_at.train_id WHERE sf_date = '{}' and "
                            "stops_at.station_id = '{}' and seats_free.sf_segment_id = '{}' and "
                                 "stops_at.time_in BETWEEN '{}' AND '{}' and seats_free.train_num in "
                                 "(SELECT train_num FROM trains WHERE train_direction ='{}')".format(dep_date,outgoing_station,destination_station,time_range[0],time_range[1],direction)).fetchall()

    else:
        results = []

    return results
#If no matches are shown for given time and date, display all available trains at that day for the desired start,end location
def get_all_available_trains(dep_date,outgoing_station,destination_station):
    direction = get_direction(int(outgoing_station),int(destination_station))

    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    #This query is for the case where there are no matches. It will display all available times for the desired destination.
    #this is easier than just going back and entering new times until you are matched with one. Since all of our trains run
    #at the same time everyday, it would be silly to try to find a different time for your trip.
    cursor.execute("SELECT seats_free.train_num, seats_free.sf_date, stops_at.time_in FROM seats_free INNER JOIN "
                             " stops_at ON seats_free.train_num = stops_at.train_id WHERE seats_free.sf_date = '{}' and "
                             " stops_at.station_id = '{}' and seats_free.sf_segment_id = '{}' "
                   "and seats_free.train_num in (SELECT train_num FROM trains WHERE train_direction = '{}')".format(dep_date,outgoing_station,destination_station,direction))
    return cursor.fetchall()


#get the direction of the trip
def get_direction(outgoing_station,destination_station):
    if outgoing_station - destination_station < 0:
        return 0 #south
    else:
        return 1 #north



#checks if there are seats available between segements
def get_seats_free(start_station,end_station,date,tickets):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    start_station = int(start_station)
    end_station = int(end_station)
    #print(int(start_station))

    for x in range(start_station,end_station):
       sf_free = cursor.execute("SELECT sf_free-'{}' FROM seats_free WHERE sf_segment_id = '{}' AND  sf_date = '{}'".format(tickets,x,date)).fetchone()
       #print(sf_free[0])
       if sf_free[0] < 0:
           return False

    return True

#returns a +/- 30 minute time range.
def get_time_range(time):
    range = '00:30'
    mid_time = datetime.datetime.strptime(time, '%H:%M')
    range = datetime.datetime.strptime(range, '%H:%M')
    #print(range)
    lo_range = (mid_time - dt.timedelta(0,1800)) #30 minutes
    lo_range = '{:02d}:{:02d}'.format(lo_range.hour, lo_range.minute)

    hi_range = (mid_time + dt.timedelta(0,1800))
    hi_range = '{:02d}:{:02d}'.format(hi_range.hour,hi_range.minute)
    time_range = (lo_range,hi_range)
    #print(time_range)

    return time_range

def insert_trips(date,trip_time,trip_start,trip_end, train_id,passenger_id,trip_fare,payment_method):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()

    cursor.execute("INSERT INTO trips(trip_date,trip_time,trip_start,trip_end,train_id,passenger_id,trip_fare,payment_method)"
                   " VALUES(?,?,?,?,?,?,?,?)",(date,trip_time,trip_start,trip_end,train_id,passenger_id,trip_fare,payment_method))
    db.commit()

def decrease_seats_free(train_num,date,outgoing_station,destination_station,tickets):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    if int(outgoing_station) < int(destination_station):
        start = outgoing_station
        end = destination_station
    else:
        start = destination_station
        end = outgoing_station
    for x in range(start,end+1):
        print(x)
        cursor.execute("UPDATE seats_free SET sf_free = sf_free -'{}' WHERE train_num = '{}' and sf_segment_id = '{}' "
                       "and sf_date = '{}'".format(tickets,train_num,x,date))
        db.commit()

def insert_results(train_id,dep_date,dep_time,start_station,end_station,tickets):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO results (train_id,dep_date,dep_time,start_station,end_station,tickets) "
                   " VALUES (?,?,?,?,?,?)",(train_id,dep_date,dep_time,start_station,end_station,tickets))
    db.commit()


def get_max_result_id():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT max(result_id) FROM results")

    return cursor.fetchone()

def get_result(result_id):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM results WHERE result_id = '{}'".format(result_id))

    return cursor.fetchall()

def insert_passenger(fname,lname,email,billing_addr,payment):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO passengers (fname,lname,email,billing_addr,payment) VALUES (?,?,?,?,?)",
                   (fname,lname,email,billing_addr,payment))
    db.commit()

#get passenger_id with email
def get_passenger_id(email):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT passenger_id FROM passengers WHERE email = '{}'".format(email))
    return cursor.fetchone()

#get station names
def get_station_names(station_id):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT station_name FROM stations WHERE station_id = '{}'".format(station_id))
    return cursor.fetchone()

#get times for each train number based on direction.
def get_train_by_direction(train_direction):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT train_num FROM trains WHERE train_direction ='{}'".format(train_direction))
    return cursor.fetchall()

def get_times_by_train_id(train_id):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT time_out FROM stops_at WHERE train_id = '{}'".format(train_id))
    return cursor.fetchall()

def get_days_from_train_in(train_id):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT day FROM trains WHERE train_id = '{}'".format(train_id))
    return cursor.fetchall()

def get_time_by_station(station_id,train_id_weekday_start,train_id_weekday_end,train_id_weeknd_start,train_id_weeknd_end):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    station_name = cursor.execute("SELECT station_name FROM stations WHERE station_id ='{}'".format(station_id)).fetchone()
    weekday = cursor.execute("SELECT time_out FROM stops_at WHERE station_id = '{}' and train_id BETWEEN '{}' AND '{}'".format(station_id,train_id_weekday_start,train_id_weekday_end)).fetchall()
    weekend = cursor.execute("SELECT time_out FROM stops_at WHERE station_id = '{}' and train_id BETWEEN '{}' and '{}'".format(station_id,31,35)).fetchall()
    weekday1 = []
    weekend1 = []

    for y in range(1):
        weekday1.append(station_name[0])
        for x in range(len(weekday)):
            weekday1.append(weekday[x][0])

    for x in range(len(weekend)):
        weekend1.append(weekend[x][0])


    all_days = weekday1 + weekend1

    return all_days 

def get_day_of_week(train_num):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute("SELECT day FROM trains WHERE train_num ='{}'".format(train_num))
    return cursor.fetchone()




    #Some tests:
#time = datetime.strftime('05:30')
#print(get_one_way_trip('2017-05-01','05:30','25','1'))
#print(get_time_range('05:30'))
#print(get_seats_free(1,4,'2017-05-01',4))
#print(get_all_available_trains('2017-05-06',1,12))
#insert_trips('2017-05-01',1,2,1,1,10.00,'0')
#decrease_seats_free(1,'2017-05-01',5,1,4)
#index = get_max_result_id()[0]
#print(index)#
#print(get_time_by_station(1))
#print(get_day_of_week(1))
print(get_time_by_station(35,13,24,31,35))