#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/views.py
""" Application Views
"""

from sumofsquares import app
from sumofsquares.models import Natural, Triplet
from sumofsquares.database import init_db, db_session
from sumofsquares.dbtools import DBHandler
from flask import jsonify, request, render_template
import datetime


@app.route('/difference', methods=['GET'])
def ss_termial_diff():
    """
    Returns the following JSON were solution is difference between n's termial square and teh sum of the squares of n

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
    except (AttributeError, NameError):
        return jsonify({'Message': "Input value {} is either not natural or out of range.".format(n)})

    response = {'datetime': datetime.datetime.now(), 'value': answer, 'number': n, 'occurences': natural.request_count,
                'last_datetime': natural.last_request}
    natural.last_request = datetime.datetime.now()
    natural.request_count += 1
    db_session.commit()
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

    a, b = min(a, b), max(a, b)
    product = a*b*c
    triplet = Triplet.query.filter(Triplet.product == product, Triplet.a == a, Triplet.b == b).first()

    try:
        response = {'datetime': datetime.datetime.now(), 'Triplet': [a, b, c], 'number': product,
                    'occurences': triplet.request_count, 'last_datetime': triplet.last_request}
        triplet.last_request = datetime.datetime.now()
        triplet.request_count += 1
        db_session.commit()
        return jsonify(response)

    except (AttributeError, NameError) as err:
        return jsonify({'Error': str(err)})


@app.route('/tripletsInMem', methods=['GET'])
def triplets_in_mem():
    """ Returns whether 3 numbers are a pythagorean triplet and if their product is equals to n"""

    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    c = request.args.get("c", type=int)
    n = request.args.get("n", type=int)

    if None in (a, b, c, n):
        return jsonify({'Message': "One or more your input values is not an integer or you did not pass 4 values."})

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


'''
Front End Views
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
