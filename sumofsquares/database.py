#!/usr/bin/python
# -*- coding: UTF-8 -*-
# sumofsquare/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sumofsquares import app


engine = create_engine(app.config['SQLITE_URL'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """ Models imported here to be registered on the metadata """
    import sumofsquares.models
    Base.metadata.create_all(bind=engine)

