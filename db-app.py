from flask import Flask,render_template,request, url_for, redirect
from mods_c import  get_stations, get_passengers_table

app = Flask(__name__)


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
        _outgoing_station = request.form['from-station'] # PASSED AS station symbol
        _destination_station = request.form['to-station'] #PASSED as station symbol

        # PROCESS VALUES HERE FOR QUERIES
        trip_found = False
        results = []
        # if TRIP is found from query, chane trip found to TURUE
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


@app.route('/purchase/')
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
    return render_template('tables.html', passengers = all_passengers)

if __name__ == "__main__":
    app.run()