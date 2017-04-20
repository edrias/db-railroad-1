from flask import Flask,render_template,request, url_for, redirect
from forms import OneWayForm
app = Flask(__name__)

@app.route("/")
@app.route('/<path>')
def main():
    return render_template('index.html')


#@app.route('/one-way/<path>',methods=["GET","POST"])
@app.route('/one-way/')
def one_way():
    # form = OneWayForm()
    # if form.validate_on_submit():
    #     _dep_date = request.form['departure-date']
    #     _dep_time = request.form['departure-time']
    #     _outgoing_station = request.form['from-station']
    #     _destination_station = request.form['to-station']
    #     print(_dep_date)
    #     print (_dep_time)
    #     print (_outgoing_station)
    #     print (_destination_station)
    #     return "hello?"
    return render_template('one-way.html')

@app.route('/oneway-action',methods=["POST"])
def one_way_sub():
    if request.method == "POST":
        _dep_date = request.form['departure-date']
        _dep_time = request.form['departure-time']
        _outgoing_station = request.form['from-station']
        _destination_station = request.form['to-station']
        print(_dep_date)
        print (_dep_time)
        print (_outgoing_station)
        print (_destination_station)
    return "wtf"

    # return  render_template('index.html')

@app.route('/round-trip/')
def round_trip():
    return render_template('round-trip.html')


if __name__ == "__main__":
    app.run()