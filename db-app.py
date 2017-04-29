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
        return


def book_ticket():
    ticket_info = input("ticket info")
    #SEE purchase_act() for values
    # this will need to be a sql entry
    # create new passengers
    # reduce the seats free and etc


book_trip_term()

@app.route("/")
@app.route('/<path>')
def main():
    my_str = input("one way or round trip?")
    return render_template('index.html')


#@app.route('/one-way/<path>',methods=["GET","POST"])
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
    return "result template"


@app.route('/round-trip/')
def round_trip():
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
        results = []
        return render_template('results.html',results = results)


@app.route('/purchase/')
def purchase_tkt():
    return render_template('purchase.html')


@app.route('/purchase-action', methods=['POST'])
def purchase_act():
    if request.method=='POST':
        fname = request.form['fname'] #str
        lname = request.form['lname'] #str
        email = request.form['email'] #email
        billing_addr = request.form['addr'] #str
        credit_card = request.form['payment'] #number
    return "purchased!"

if __name__ == "__main__":
    app.run()