from flask import Flask,render_template,request, url_for, redirect
app = Flask(__name__)

def book_trip_term():
    my_str = input("one way or round trip?")
    if my_str == "one_way":
        input_from_form =input("one way input") #format it yourselves and parse the string for now
        # SEE one_way_act()  function below
        # your  mysql queries produce some result
        # maybe make a new class that can store all of the information
        # bc will need to display it all in the GUI
    elif my_str == "round trip":
        # SEE round_trip_act() function below
        input_from_form =input("round trip input")
    else:
        t = False
        return


def book_ticket():
    ticket_info = input("ticket info")
    #SEE purchase_act() for values
    # this will need to be a sql entry
    # create new passengers
    # reduce the seats free and etc

# book_trip_term(terminal)


@app.route("/")
@app.route('/<path>')
def main():
    # my_str = input("one way or round trip?")
    return render_template('index.html')


#@app.route('/one-way/<path>')
@app.route('/one-way/')
def one_way():
    return render_template('one-way.html')


@app.route('/oneway-action',methods=["POST"])
def one_way_act():
    if request.method == "POST":
        _dep_date = request.form['departure-date'] #date type
        _dep_time = request.form['departure-time'] #time type
        _outgoing_station = request.form['from-station'] #can be the station symbol
        _destination_station = request.form['to-station'] #can be the station symbol

        # PROCESS VALUES HERE FOR QUERIES
        trip_found = False
        results = []
        # if TRIP is found from query, chane trip found to TURUE
        return render_template('results.html', found = trip_found, results = results)
    return "Oops you can't access this page"


@app.route('/round-trip/')
def round_trip():
    #page that renders the round trip form-
    # results of the form are retrieved in round_trip_act()
    return render_template('round-trip.html')


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

if __name__ == "__main__":
    app.run()