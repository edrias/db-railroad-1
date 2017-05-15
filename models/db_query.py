import sqlite3 as sql

#Use this class to access DB

class db_connect():
    def __int__(self):
        with sql.connect("rail.db") as self.con:
            self.cur = self.con.cursor()

    def get_stations(self):
        q = self.cur.execute('select station_name,station_symbol from stations')
        stations = q.fetchall()
        return stations

    def get_one_way_trip(self, dep_date,dep_time,outgoing_station,destination_station):
        #TODO: write query
        return None

    def get_round_trip(self,dep_date,dep_time,return_date,return_time, outgoing_station,destination_station):
        #TODO: write query
        return None

    def insert_purchase(self,trip_details,fname,lname,email,billing_addr,credit_card):
        #TODO: write query
        return None








