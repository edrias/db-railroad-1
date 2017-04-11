from flask import Flask,render_template,request
app = Flask(__name__)

@app.route("/")
@app.route('/<path>')
def main():
    return render_template('index.html')


@app.route('/one-way')
def one_way():
    # _dep_date = request.form['departure-date']
    # _dep_time = request.form['departure-time']
    # _outgoing_station = request.form['from-station']
    # _destination_station = request.form['to-station']
    return render_template('one-way.html')


@app.route('/round-trip')
def round_trip():
    return render_template('round-trip.html')





if __name__ == "__main__":
    app.run()