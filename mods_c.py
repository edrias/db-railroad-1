import sqlite3

def get_stations():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select station_name,station_symbol from stations')
    stations = cursor.fetchall()
    return stations


def get_passengers_table():
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    cursor.execute('select * from passengers')
    return  cursor.fetchall()

#display available trains given dates/time
def get_one_way_trip(dep_date,dep_time,outgoing_station,destination_station):
    db = sqlite3.connect('rail.db')
    cursor = db.cursor()
    #
   #cursor.execute("SELECT trains.train_num, stops_at.time_out FROM trains INNER JOIN ")
