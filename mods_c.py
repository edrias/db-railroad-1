
class stations():
    def setStation(self,long_name, station_sym):
        self.long_name = long_name
        self.station_symbol = station_sym
    long_name = ""
    station_symbol = ""


def make_stationsList(sql_query_list):
    stations_type_list = []
    n = 0
    while n < len(sql_query_list):
        s = stations()
        s.setStation(sql_query_list[n][0],sql_query_list[n][1])
        stations_type_list.append(s)
        n+=1

    return stations_type_list