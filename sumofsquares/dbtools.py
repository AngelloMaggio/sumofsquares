#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/dbtools.py
""" Functions and classes to manage DB tasks such as population
"""
from sumofsquares.database import init_db
from sumofsquares.models import Natural, Triplet
from sumofsquares.database import db_session
from sumofsquares import app
import math


class DBHandler(object):
    """ Handles the construction and decunstruction of the database """
    def __init__(self, mode='r'):
        self.mode = mode

    def populate(self, n: int) -> int:
        """ Triggers both populations; naturals and triplets."""
        if n > app.config["POPULATE_MAX"]:
            return 0
        self.populate_natural(n)
        self.populate_triplet(n)

    def populate_natural(self, n: int) -> int:
        """ Populates database to work with the first n Natural numbers """
        if self.mode != 'w' or not isinstance(n, int):
            return 0
        if n > app.config["POPULATE_MAX"]:
            return 0

        init_db()

        current_termial = 0
        current_ss = 0
        for i in range(1, n+1):

            ss = i**2 + current_ss
            current_ss = ss

            termial = i + current_termial
            current_termial = termial

            termial_square = termial**2

            natural = Natural(i, termial=termial, termial_sq=termial_square, sumofsquares=ss)

            db_session.add(natural)
            db_session.commit()
        return 1

    def populate_triplet(self, n: int) -> int:
        """ Will populate triplet DB"""

        if self.mode != 'w' or not isinstance(n, int):
            return 0
        if n > app.config["POPULATE_MAX"]:
            return 0

        init_db()

        triplets = Triplet.gen_all_pyth_trips(n)
        for triplet in triplets:
            a, b, c = int(triplet[0]), int(triplet[1]), int(triplet[2])
            new = Triplet(min(a, b), max(a, b), c, a*b*c)
            db_session.add(new)
            db_session.commit()

        return 1


