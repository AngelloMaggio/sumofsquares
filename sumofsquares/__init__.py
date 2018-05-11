#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/__init__.py

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

import sumofsquares.views


