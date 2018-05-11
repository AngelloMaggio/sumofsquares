#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquares/__init__.py

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

from sumofsquares.database import db_session
import sumofsquares.views


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Flask will automatically remove database sessions at the end of the request or when the application shuts down"""
    db_session.remove()

