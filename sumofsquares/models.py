#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/models.py
""" Application Models
"""

from sqlalchemy import Column, Integer, DateTime
from sumofsquares.database import Base
import datetime


class Natural(Base):
    """ Database model for storing a natural number, the square of its termial, and the sum of its squares. """
    __tablename__ = 'naturals'
    n = Column(Integer, primary_key=True)
    termial = Column(Integer)
    termial_sq = Column(Integer)
    sumofsquares = Column(Integer)
    request_count = Column(Integer)
    last_request = Column(DateTime)

    def __init__(self, n, termial=None, termial_sq=None, sumofsquares=None, request_count=0):
        self.n = n
        self.termial = termial
        self.termial_sq = termial_sq
        self.sumofsquares = sumofsquares
        self.request_count = 0
        self.last_request = datetime.datetime.now()

    def __repr__(self):
        return '<Natural {}>'.format(self.n)

    def construct(self):
        """ Set values depending solely on n being set """
        if not self.termial:
            self.termial = self.get_termial(self.n)
        if not self.termial_sq:
            self.termial_sq = self.termial**2
        if not self.sumofsquares:
            self.sumofsquares = self.get_ss(self.n)

    @staticmethod
    def get_termial(n: int) -> int:
        """ Termial is defined as the sum of the first n natural numbers"""
        return (n**2+n)/2

    @staticmethod
    def get_ss(n: int) -> int:
        """ Returns the sum of the squares of the first n natural numbers """
        return n**3/3 + n**2/2 + n/6
