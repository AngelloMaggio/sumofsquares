#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/views.py
""" Application Views
"""

from sumofsquares import app
from sumofsquares.models import Natural
from sumofsquares.database import init_db
from sumofsquares.dbtools import DBHandler
from flask import jsonify
import datetime


@app.route('/sstermialdiff/<int:n>', methods=['GET'])
def ss_termial_diff(n):
    """
    {
"datetime":current_datetime,
"value":solution,
"number":n,
"occurrences":occurrences // the number of times n has been requested
"last_datetime": datetime_of_last_request
}
    """
    init_db()

    natural = Natural.query.filter(Natural.n == n).first()

    try:
        answer = natural.termial_sq - natural.sumofsquares
    except AttributeError:
        return jsonify({'Message': 'Number %d not in range for current configration.'})

    response = {'datetime': datetime.datetime.now(), 'value': answer, 'numer': n, 'occurences': natural.request_count,
                'last_datetime': natural.last_request}

    return jsonify(response)


@app.route('/populate/<int:n>', methods=['GET'])
def populate_db(n):
    """ Endpoint to trigger database population"""
    handler = DBHandler('w')
    handler.populate(n)
    return jsonify({'Status': 'Done'})
