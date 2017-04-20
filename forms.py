# ourapp/forms.py
from flask_wtf import Form


class OneWayForm(Form):
    depart_date = ('departure-date')
    depart_time = ('departure-time')
    outgoing_st = ('from-station')
    destination_st =('to-station')

