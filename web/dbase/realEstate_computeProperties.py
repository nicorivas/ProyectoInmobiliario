#!/usr/bin/env python
import ast # to load the file (literal_eval is nicer than eval, they say)
import re # regular expressions
import requests # to call the API of Google to get lat-lon
import pandas as pd # are cute
from pathlib import Path # nice way to manage paths
import json # to save nice dictionaries
import codecs
from sqlalchemy import create_engine # for pandas dataframes to postgre
from sqlalchemy import MetaData
from sqlalchemy.sql import and_
from sqlalchemy import update
from sqlalchemy import func
import datetime
from tools import *
import os.path

def getBuildings():
    sql_engine, sql_metadata, sql_connection = dbase_setup()
    sql_buildings_table = sql_metadata.tables['building_building']
    sql_select = sql_buildings_table.select()
    sql_buildings = sql_connection.execute(sql_select)
    for building in sql_buildings:
        coords = [building['lat'],building['lon']]
        sql = """SELECT square.code FROM square_square square WHERE
                 ST_DWithin(ST_SetSRID(ST_GeometryN(square.mpoly,1),0),
                   ST_MakePoint({},{}),0.0001)""".format(coords[1],coords[0])
        a = sql_engine.execute(sql)
        print(a.rowcount)
        print(building.addressStreet)
        for b in a:
            print(b)

getBuildings()
