#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/models.py
""" Application Models
"""

from sqlalchemy import Column, Integer, DateTime
from sumofsquares.database import Base
import datetime
import numpy as np


class Natural(Base):
    """ Database model for storing a natural number, the square of its termial, and the sum of its squares. """
    __tablename__ = 'naturals'
    n = Column(Integer, primary_key=True)
    termial = Column(Integer)
    termial_sq = Column(Integer)
    sumofsquares = Column(Integer)
    request_count = Column(Integer)
    last_request = Column(DateTime)

    def __init__(self, n, square=None, termial=None, termial_sq=None, sumofsquares=None, request_count=0):
        self.n = n
        self.square = square
        self.termial = termial
        self.termial_sq = termial_sq
        self.sumofsquares = sumofsquares
        self.request_count = request_count
        self.last_request = datetime.datetime.now()

    def __repr__(self):
        return '<Natural {}>'.format(self.n)

    def construct(self):
        """ Set values depending solely on n being set """
        if not self.square:
            self.square = self.n**2
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


class Triplet(Base):
    """ Store triplets for easy querying"""
    __tablename__ = 'triplets'

    product = Column(Integer, primary_key=True)
    a = Column(Integer)
    b = Column(Integer)
    c = Column(Integer)
    last_request = Column(DateTime)
    request_count = Column(Integer)

    def __init__(self, a: int, b: int, c, product, request_count=0):
        self.a = a
        self.b = b
        self.c = c
        self.product = product
        self.last_request = datetime.datetime.now()
        self.request_count = request_count

    @staticmethod
    def is_pythagorean_triplet(a: int, b: int, c: int, product=None) -> bool:
        """ Simple way of checking if a,b,c are a pythagorean triplet and if their product equals to n (if n given)
        If n is not given it will just return whether they are a triplet."""
        if not product:
            return a**2 + b**2 == c**2
        return (a**2 + b**2 == c**2) and a*b*c == product

    @staticmethod
    def gen_prim_pyth_trips(limit):
        """ Finds all primitive Pythagorean triplets up to limit
        Sourced from Stackoverflow
        https://stackoverflow.com/questions/575117/generating-unique-ordered-pythagorean-triplets/"""
        u = np.mat(' 1  2  2; -2 -1 -2; 2 2 3')
        a = np.mat(' 1  2  2;  2  1  2; 2 2 3')
        d = np.mat('-1 -2 -2;  2  1  2; 2 2 3')
        uad = np.array([u, a, d])
        m = np.array([3, 4, 5])
        while m.size:
            m = m.reshape(-1, 3)
            if limit:
                m = m[m[:, 2] <= limit]
            yield from m
            m = np.dot(m, uad)

    @staticmethod
    def gen_all_pyth_trips(limit):
        """ Finds all Pythagorean triplets up to limit"""
        for prim in Triplet.gen_prim_pyth_trips(limit):
            i = prim
            for _ in range(limit//prim[2]):
                yield i
                i = i + prim
