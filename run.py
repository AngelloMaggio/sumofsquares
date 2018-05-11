#!/usr/bin/python
# -*- coding: UTF-8 -*-
# /run.py
""" Run Flask Server
    Host set to '0.0.0.0' to facilitate Docker implementation"""

from sumofsquares import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')
