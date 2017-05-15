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