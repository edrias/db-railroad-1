from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/one-way')
def one_way():
    return render_template('one-way.html')

@app.route('/round-trip')
def round_trip():
    return render_template('round-trip.html')


if __name__ == "__main__":
    app.run()