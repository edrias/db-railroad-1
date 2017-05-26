from flask import Flask,render_template,request, url_for, redirect
from mods_c import * #get_stations, get_passengers_table,get_trips_table, get_one_way_trip,get_destination_stations,get_seats_free, get_all_available_trains,insert_trips
from ast import literal_eval
import os

app = Flask(__name__)
class result:
    def __init__(self,result_id,train_num,dep_date,dep_time,outgoing_station,destination_station,tickets):
        self.result_id = result_id
        self.train_id = train_num
        self.dep_date = dep_date
        self.dep_time = dep_time
        self.outgoing_station = get_destination_stations(outgoing_station,destination_station)[0]
        self.destination_station =get_destination_stations(outgoing_station,destination_station)[1]
        self.tickets = tickets
        #price = #of segments * 8 * #of tickets
        self.price = (abs(int(outgoing_station)-int(destination_station))*8)*int(tickets)


    #def __str__(self):
    #    return self.train_id


@app.route("/")
@app.route('/<path>')
def main():
    return render_template('index.html')

@app.route('/one-way/')
def one_way():
    stations = get_stations()
    return render_template('one-way.html',stations =stations)


@app.route('/oneway-action',methods=["POST"])
def one_way_act():
    if request.method == "POST":
        _dep_date = request.form['departure-date'] #date type
        _dep_time = request.form['departure-time'] #time type
        _outgoing_station = request.form['from-station'] # PASSED AS station id
        _destination_station = request.form['to-station'] #PASSED as station id
        _tickets = request.form['tickets'] # number of tickets max 8

        # PROCESS VALUES HERE FOR QUERIES
        trip_found = True
        trips = []#query results
        results = [] #if customer forms return a match, this list is used
        all_results = []#if customer forms do not return any matches, this list displays all available times for given day.

        #query for  available trips given dep_time
        trips.append(get_one_way_trip(_dep_date,_dep_time,_outgoing_station,_destination_station))

        #list of 'result' object for each trip
        for x in range(len(trips[0])):
            result_id = get_max_result_id()[0]
            results.append(result(generate_result_id(result_id),trips[0][x][0],_dep_date,trips[0][x][2],_outgoing_station,_destination_station,_tickets))

            #insert values of results class into results table.
            # train_id, date,time,start_station,end_station,tickets
            insert_results(trips[0][x][0],_dep_date,trips[0][x][2],_outgoing_station,_destination_station,_tickets)

        #If there is no match, display all available times for the desired start/end destination.
        if results == []:
            #query gets all results
            all_results.append(get_all_available_trains(_dep_date,_outgoing_station,_destination_station))

            #list of 'result' object for each trip
            for x in range(len(all_results[0])):
                result_id = get_max_result_id()[0]
                results.append(result(generate_result_id(result_id),all_results[0][x][0],_dep_date, all_results[0][x][2],_outgoing_station, _destination_station, _tickets))
                #insert values of results class into results table
                #train_id, date,time,start_station,end_station,tickets
                insert_results(all_results[0][x][0],_dep_date, all_results[0][x][2],_outgoing_station, _destination_station, _tickets)

            trip_found = False



        # if TRIP is found from query, change trip found to TRUE
        return render_template('results.html', found = trip_found, results = results, roundtrip = False)
    return "Oops you can't access this page"


#checks if index is none and increments accordingly if not none
def generate_result_id(index):
    if index == None:
        return 1
    else:
        return index + 1

@app.route('/round-trip/')
def round_trip():
    stations = get_stations()
    #page that renders the round trip form-
    # results of the form are retrieved in round_trip_act()
    return render_template('round-trip.html', stations= stations)


@app.route('/round-trip-action', methods =['POST'])
def round_trip_act():
    if request.method =='POST':
        _dep_date = request.form['departure-date'] #date type
        _dep_time = request.form['departure-time'] #time type
        _return_date = request.form['return-date'] #date type
        _return_time = request.form['return-time'] #time type
        _tickets = request.form['tickets']
        _outgoing_station = request.form['from-station'] #station symbol
        _destination_station = request.form['to-station'] #station symbol
        print(_destination_station)
        # PROCESS VALUES HERE
        #put results into results list as a type (perhaps results type)
        departing_trips = []
        returning_trips = []
        all_departing_trips =[]#not sure if we should do this, seems like a big mess waiting to happen
        all_arriving_trips = []#look at above comment
        results = []

        departing_trips.append(get_one_way_trip(_dep_date,_dep_time,_outgoing_station,_destination_station))
        returning_trips.append(get_one_way_trip(_return_date,_return_time,_destination_station,_outgoing_station))

        print(departing_trips)
        print(returning_trips[0])

        #for each departing trip, have each available returning trip
        for x in range(len(departing_trips[0])):
            for y in range(len(returning_trips[0])):
                result_id = get_max_result_id()[0]

                trip_departing = result(generate_result_id(result_id),departing_trips[0][x][0],_dep_date,departing_trips[0][x][2],_outgoing_station,_destination_station,_tickets)
                insert_results(trip_departing.train_id,trip_departing.dep_date,trip_departing.dep_time,_outgoing_station,_destination_station,trip_departing.tickets)

                result_id = get_max_result_id()[0]

                #trip_returning = result(generate_result_id(result_id),returning_trips[0][y][0],_return_date,returning_trips,[0][y][2],_destination_station,_outgoing_station,_tickets)
                trip_returning = result(generate_result_id(result_id),returning_trips[0][y][0],_return_date,returning_trips[0][y][2],_destination_station,_outgoing_station,_tickets)

                insert_results(trip_returning.train_id,trip_returning.dep_date,trip_returning.dep_time,_destination_station,_outgoing_station,trip_returning.tickets)

                results.append((trip_departing,trip_returning))


        if results == []:
            trip_found = False
        else:
            trip_found = True


        return render_template('results.html', found= trip_found, results = results, roundtrip = True)
    return "Oops you can't access this page"


@app.route('/purchase', methods =['POST'])
def purchase_tkt():
    # USERS will only be redirected to this page from selecting a trip - otherwise inaacessible page
    if request.method == 'POST':
        result_id = request.form['book_button']  # result type - still need to be defined

        print(result_id)

        #if result_id
        #page that has the form- once form is submitted - goes to purchase act
        return render_template('purchase.html', result = result_id)
    return "Oops you can't access this page"


@app.route('/purchase-action', methods=['POST'])
def purchase_act():
    if request.method=='POST':
        result_id= request.form['action'] # TODO need to pass the trip details into the purchase
        #rint(trip_details.dep_date)
        result_id = literal_eval(result_id)#value from form is a string, convert to int.



        fname = request.form['fname'] #str
        lname = request.form['lname'] #str
        email = request.form['email'] #email
        billing_addr = request.form['addr'] #str
        credit_card = request.form['payment'] #number

        if isinstance(result_id,tuple):#IF ROUND TRIP!
            dep_trip = get_result(result_id[0])[0]
            ret_trip = get_result(result_id[1])[0]
            print(dep_trip)
            print(ret_trip)

            dtrain_id = dep_trip[1]
            dtrip_date = dep_trip[2]
            dtrip_time = dep_trip[3]
            dtrip_start = dep_trip[4]
            dtrip_end = dep_trip[5]
            tickets = dep_trip[6]

            rtrain_id = ret_trip[1]
            rtrip_date = ret_trip[2]
            rtrip_time = ret_trip[3]
            rtrip_start = ret_trip[4]
            rtrip_end = ret_trip[5]
            #tickets already taken care of
            fare = abs(int(rtrip_start) - int(rtrip_end)) * 8 * int(tickets)

            insert_passenger(fname,lname,email,billing_addr,credit_card)
            passenger_id = get_passenger_id(email)[0]

            #departing trip
            insert_trips(dtrip_date,dtrip_time,dtrip_start,dtrip_end,dtrain_id,passenger_id,fare,credit_card)
            decrease_seats_free(dtrain_id, dtrip_date, dtrip_start, dtrip_end, tickets)
            #returning trip
            insert_trips(rtrip_date,rtrip_time,rtrip_start,rtrip_end,rtrain_id,passenger_id,fare,credit_card)
            decrease_seats_free(rtrain_id, rtrip_date, rtrip_start, rtrip_end, tickets)

        else:
            #retrieve trip info from results table given result_id
            trip_details = get_result(result_id)[0]
            print(trip_details)
           #info that will be entered into trip details
            train_id = trip_details[1]
            trip_date = trip_details[2]
            trip_time = trip_details[3]
            trip_start = trip_details[4]
            trip_end = trip_details[5]
            tickets = trip_details[6]
            # fare is calucuated by # of segments and tickets. General price is $8.00
            fare = abs(int(trip_start) - int(trip_end))*8*int(tickets)

            #insert passenger info from form values
            insert_passenger(fname,lname,email,billing_addr,credit_card)

            #insert into trips table.
            passenger_id = get_passenger_id(email)[0]#passenger_id from passengers table.
            insert_trips(trip_date,trip_time,trip_start,trip_end,train_id,passenger_id,fare,credit_card)

            #update seats_free for each segment!
            decrease_seats_free(train_id,trip_date,trip_start,trip_end,tickets)

        return render_template('purchased.html')
    return "Oops you can't access this page"


@app.route('/north-sched')
def north_sched():
    #17 northbound trains.
    direction = 1
    trains = []  # list of tuples, holding train number, train day
    station_times = []  # w.e said about the list of 18 pieces list

    #get trains 13-24
    for x in range(13,25):
        trains.append((x,get_day_of_week(x)[0]))

    #get trains 31-35
    for x in range(31,36):
        trains.append((x,get_day_of_week(x)[0]))

    for x in range(35,0,-1):
        station_times.append((get_time_by_station(x,13,24,31,35)))


    print(station_times)

    return render_template('sched_template.html',direction = direction, trains = trains, stationtimes = station_times)

@app.route('/south-sched')
def south_sched():
    direction = 0
    trains = [] # list of tuples, holding train number, train direction
    station_times=[] #w.e said about the list of 18 pieces list

    for x in range(1,13):
        trains.append((x,get_day_of_week(x)[0]))

    for x in range(25,31):
        trains.append((x,get_day_of_week(x)[0]))

    for x in range(1,36):
        station_times.append((get_time_by_station(x,1,12,25,31)))
    return render_template('sched_template.html',direction = direction, trains = trains, stationtimes = station_times)

@app.route('/tables')
def tables():
    all_passengers = get_passengers_table()
    trips = get_trips_table()
    seats_free = get_all_seats_free()
    return render_template('tables.html', passengers = all_passengers, trips = trips, sf = seats_free)

if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
