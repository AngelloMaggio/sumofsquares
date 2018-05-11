#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/dbtools.py
""" Functions and classes to manage DB tasks such as population
"""
from sumofsquares.database import init_db
from sumofsquares.models import Natural
from sumofsquares.database import db_session


class DBHandler(object):
    """ Handles the construction and decunstruction of the database """
    def __init__(self, mode='r'):
        self.mode = mode

    def populate(self, n: int) -> int:
        """ Populates database to work with the first n Natural numbers """
        if self.mode != 'w':
            return 0

        init_db()

        current_termial = 1
        current_ss = 1
        for i in range(1, n):
            ss = n**2 + current_ss
            termial = n + current_termial
            termial_square = termial**2
            natural = Natural(i, termial=termial, termial_sq=termial_square, sumofsquares=ss)
            db_session.add(natural)
            db_session.commit()
        return 1


