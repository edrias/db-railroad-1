import sqlite3
import datetime
import datetime as dt

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


def get_seats_free():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from seats_free')
    return cursor.fetchall()


#displays all avaiable traings +/- 30 minutes
def get_one_way_trip(dep_date,dep_time,outgoing_station,destination_station):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    time_range = get_time_range(dep_time)
    if get_seats_free(outgoing_station,destination_station,dep_date,tickets=0) == True:
        results = cursor.execute("SELECT seats_free.train_num, seats_free.sf_date, stops_at.time_in FROM seats_free INNER JOIN stops_at ON "
                            "seats_free.train_num = stops_at.train_id WHERE sf_date = '{}' and "
                            "stops_at.station_id = '{}' and stops_at.time_in BETWEEN '{}' AND '{}'".format(dep_date,outgoing_station,time_range[0],time_range[1])).fetchall()
    else:
        results = []

    return results
#so start station is 1, destination station is 5.

#checks if there are seats available between segements
def get_seats_free(start_station,end_station,date,tickets):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    start_station = int(start_station)
    end_station = int(end_station)
    print(int(start_station))
    for x in range(start_station,end_station):
       sf_free = cursor.execute("SELECT sf_free-'{}' FROM seats_free WHERE sf_segment_id = '{}' AND  sf_date = '{}'".format(tickets,x,date)).fetchone()
       print(sf_free[0])
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


#simple example. start_station =1, end_station = 2.
#time = datetime.strftime('05:30')
print(get_one_way_trip('2017-05-01','05:30','1','5'))
#print(get_time_range('05:30'))
#print(get_seats_free(1,4,'2017-05-01',4))
