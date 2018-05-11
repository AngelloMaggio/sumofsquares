#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/views.py
""" Application Views
"""

from sumofsquares import app
from sumofsquares.models import Natural, Triplet
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
    print(n)
    if not n:
        return jsonify({'Message': "Input value is not an integer."})

    init_db()

    natural = Natural.query.filter(Natural.n == n).first()

    try:
        answer = natural.termial_sq - natural.sumofsquares
    except (AttributeError, NameError) as err:
        return jsonify({'Message': "Input value {} is either not natural or out of range.".format(n)})

    response = {'datetime': datetime.datetime.now(), 'value': answer, 'number': n, 'occurences': natural.request_count,
                'last_datetime': natural.last_request}

    return jsonify(response)


@app.route('/triplets', methods=['GET'])
def triplets():
    """ Returns whether 3 numbers are a pythagorean triplet and if their product is equals to n"""

    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    c = request.args.get("c", type=int)
    n = request.args.get("n", type=int)

    if None in (a, b, c, n):
        return jsonify({'Message': "One or more your input values is not an integer."})

    if max(a, b, c) != c:
        return jsonify({'Value': "False"})

    if Triplet.is_pythagorean_triplet(a, b, c, n):
        return jsonify({'Value': "True"})


@app.route('/populate/<int:n>', methods=['GET'])
def populate_db(n):
    """ Endpoint to trigger database population"""
    handler = DBHandler('w')
    handler.populate(n)
    return jsonify({'Status': 'Done'})
