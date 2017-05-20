from flask import Flask,render_template,request, url_for, redirect
from mods_c import  get_stations, get_passengers_table,get_trips_table, get_one_way_trip,get_destination_stations,get_seats_free, get_all_available_trains,insert_trips
app = Flask(__name__)
class result:
    def __init__(self,train_num,dep_date,dep_time,outgoing_station,destination_station,tickets):
        self.train_id = train_num
        self.dep_date = dep_date
        self.dep_time = dep_time
        self.outgoing_station = get_destination_stations(outgoing_station,destination_station)[0]
        self.destination_station =get_destination_stations(outgoing_station,destination_station)[1]
        self.tickets = tickets
        #price = #of segments * 8 * #of tickets
        self.price = (abs(int(outgoing_station)-int(destination_station))*8)*int(tickets)



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
        print(_tickets)
        # PROCESS VALUES HERE FOR QUERIES
        trip_found = True
        trips = []#query results
        results = []
        all_results = []

        #query available trips
        trips.append(get_one_way_trip(_dep_date,_dep_time,_outgoing_station,_destination_station))

        #list of 'result' object for each trip
        for x in range(len(trips[0])):
            results.append(result(trips[0][x][0],_dep_date,trips[0][x][2],_outgoing_station,_destination_station,_tickets))

        #If there is no match, display all available times for the desired start/end destination.
        if results == []:
            #query gets all results
            all_results.append(get_all_available_trains(_dep_date,_outgoing_station,_destination_station))

            #list of 'result' object for each trip
            for x in range(len(all_results[0])):
                results.append(result(all_results[0][x][0],_dep_date, all_results[0][x][2],_outgoing_station, _destination_station, _tickets))
            trip_found = False

        # if TRIP is found from query, change trip found to TRUE
        return render_template('results.html', found = trip_found, results = results)
    return "Oops you can't access this page"


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

        _outgoing_station = request.form['from-station'] #station symbol
        _destination_station = request.form['to-station'] #station symbol

        # PROCESS VALUES HERE
        #put results into results list as a type (perhaps results type)
        trip_found = False

        results = []
        return render_template('results.html',found= trip_found,results = results)
    return "Oops you can't access this page"


@app.route('/purchase', methods =['POST'])
def purchase_tkt():
    # USERS will only be redirected to this page from selecting a trip - otherwise inaacessible page
    if request.method == 'POST':
        result = request.form['book_button']  # result type - still need to be defined
        #page that has the form- once form is submitted - goes to purchase act
        return render_template('purchase.html', result = result)
    return "Oops you can't access this page"


@app.route('/purchase-action', methods=['POST'])
def purchase_act():
    if request.method=='POST':
        trip_details = request.form['result'] # TODO need to pass the trip details into the purchase
        print("trip details: '{}".format(trip_details))#nothing prints for some reason.
        fname = request.form['fname'] #str
        lname = request.form['lname'] #str
        email = request.form['email'] #email
        billing_addr = request.form['addr'] #str
        credit_card = request.form['payment'] #number

        return "Purchsed Template"
    return "Oops you can't access this page"


@app.route('/tables')
def tables():
    all_passengers = get_passengers_table()
    trips = get_trips_table()
    seats_free = get_seats_free()
    return render_template('tables.html', passengers = all_passengers, trips = trips, sf = seats_free)

if __name__ == "__main__":
    app.run()