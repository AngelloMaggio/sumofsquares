#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/views.py
""" Application Views
"""

from sumofsquares import app
from sumofsquares.models import Natural
from sumofsquares.database import init_db
from sumofsquares.dbtools import DBHandler
from flask import jsonify, request
import datetime


@app.route('/difference', methods=['GET'])
def ss_termial_diff():
    """
    {
"datetime":current_datetime,
"value":solution,
"number":n,
"occurrences":occurrences // the number of times n has been requested
"last_datetime": datetime_of_last_request
}
    """
    n = request.args.get('n', type=int)

    init_db()

    natural = Natural.query.filter(Natural.n == n).first()

    try:
        answer = natural.termial_sq - natural.sumofsquares
    except (AttributeError, NameError) as err:
        if not n:
            return jsonify({'Message': "Input value is not an integer."})
        return jsonify({'Message': "Input value {} is either not natural or out of range.".format(n)})

    response = {'datetime': datetime.datetime.now(), 'value': answer, 'number': n, 'occurences': natural.request_count,
                'last_datetime': natural.last_request}

    return jsonify(response)


@app.route('/populate/<int:n>', methods=['GET'])
def populate_db(n):
    """ Endpoint to trigger database population"""
    handler = DBHandler('w')
    handler.populate(n)
    return jsonify({'Status': 'Done'})
