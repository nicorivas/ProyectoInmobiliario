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
import datetime
from tools import *
import os.path

def communeStringToId(communeName):
    '''
    Convert name of commune to the unique id of a commune stored in the database
    '''
    engine = create_engine('postgresql://postgres:iCga1kmX@localhost:5432/data')
    query = "SELECT code FROM commune_commune WHERE name LIKE '%%{}%%'".format(communeName)
    ids = engine.execute(query).fetchall()
    if len(ids) == 0:
        error('Commune not found in database: {}'.format(communeName))
        return None
    elif len(ids) > 1:
        error('Two communes were returned {}'.format(ids))
        return None
    return ids[0][0]

def regionStringToId(regionName):
    '''
    Convert name of region to the unique id of a region stored in the database
    '''
    engine = create_engine('postgresql://postgres:iCga1kmX@localhost:5432/data')
    query = "SELECT code FROM region_region WHERE name LIKE '%%{}%%'".format(regionName)
    ids = engine.execute(query).fetchall()
    if len(ids) == 0:
        error('Region not found in database: {}'.format(regionName))
        return None
    elif len(ids) > 1:
        error('Two regions were returned {}'.format(ids))
        return None
    return ids[0][0]

def addressToCoordinates(address):
    '''
    Given an address (string that Google would understand)
    return coordinates in lat long
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url_address = 'address={}'.format(address)
    url_key='&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_address+url_key)
    resp_json_payload = response.json()
    return resp_json_payload['results'][0]['geometry']['location']


def coordinatesToAddress(lat,lng):
    '''
    Given a lat-long pair, return an address
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url_latlng = 'latlng={},{}'.format(lat,lng)
    url_key='&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_latlng+url_key)
    resp_json_payload = response.json()
    resp_json_payload['results'][0]['address_components']
    number = None
    street = None
    commune = None
    region = None
    for ac in resp_json_payload['results'][0]['address_components']:
        if 'street_number' in ac['types']:
            number = ac['long_name']
        if 'route' in ac['types']:
            street = ac['short_name']
        if 'locality' in ac['types']:
            commune = ac['long_name']
        if 'administrative_area_level_1' in ac['types']:
            region = ac['long_name']
    if number == None:
        error('Address number not found from lat lng: {}'.format(resp_json_payload['results'][0]))
        return None
    if street == None:
        error('Address street not found from lat lng: {}'.format(resp_json_payload['results'][0]))
        return None
    if commune == None:
        error('Commune not found from lat lng: {}'.format(resp_json_payload['results'][0]))
        return None
    if region == None:
        error('Region not found from lat lng: {}'.format(resp_json_payload['results'][0]))
        return None
    return [number,street,commune,region]

#===============================================================================

def loadCleanDictionaries(filepaths):
    '''
    Given a filename, load the file, which should be in JSON format,
    and convert it to a list of dictionaries.
    '''
    if not isinstance(filepaths,list):
        filepaths = [filepaths]
    properties = []
    for filepath in filepaths:
        f = open(filepath,'r')
        properties.append(json.load(f))
    if len(filepaths) == 1:
        return properties[0]
    else:
        return properties

def buildingToDatabase(building,sql_engine,sql_metadata,sql_connection):

    status('Inserting building: {} {} {} {}'.format(
        addressStreet,addressNumber,addressCommune_id,addressRegion_id))

    addressNumber = building['addressNumber']
    addressStreet = building['addressStreet']
    addressCommune_id = building['addressCommune_id']
    addressRegion_id = building['addressRegion_id']

    # We need to first insert a realestate row

    sql_realestate_table = sql_metadata.tables['realestate_realestate']

    sql_select = sql_realestate_table.select().where(and_(
        sql_realestate_table.c.propertyType == 3,
        sql_realestate_table.c.addressNumber == addressNumber,
        sql_realestate_table.c.addressStreet == addressStreet,
        sql_realestate_table.c.addressCommune_id == addressCommune_id,
        sql_realestate_table.c.addressRegion_id == addressRegion_id))
    sql_realestate = sql_connection.execute(sql_select)

    building_id = -1

    if sql_realestate.rowcount == 0:
        # Realestate does not exist. Add.
        id = sql_engine.execute("SELECT MAX(id) FROM realestate_realestate").fetchall()[0][0]
        if id == None:
            id = 1
        else:
            id = id+1
        realestate = building.copy()
        realestate['id'] = id
        realestate.pop('apartmentRef', None)
        realestate.pop('fromApartment', None)
        realestate['propertyType'] = 3
        sql_insert = sql_realestate_table.insert().values(realestate)
        sql_result = sql_connection.execute(sql_insert)
        building_id = sql_result.inserted_primary_key[0]
    elif sql_buildings.rowcount > 1:
        error("There is more than one building with the same address!")
        exit(0)
    else:
        building = sql_realestate.first()
        building_id = building[0]

        stmt = sql_realestate_table.update().\
                values(sourceUrl=building['sourceUrl']).\
                where(sql_buildings_table.c.id == building_id)
        sql_connection.execute(stmt)

        warning('Tried to insert building that already exists: id={}'.format(building_id))

    # Now we insert all the info we have regarding the building

    sql_realestate_table = sql_metadata.tables['building_building']

    sql_select = sql_realestate_table.select().where(and_(
        sql_realestate_table.c.propertyType == 3,
        sql_realestate_table.c.addressNumber == addressNumber,
        sql_realestate_table.c.addressStreet == addressStreet,
        sql_realestate_table.c.addressCommune_id == addressCommune_id,
        sql_realestate_table.c.addressRegion_id == addressRegion_id))
    sql_realestate = sql_connection.execute(sql_select)

    return building_id

def apartmentToDatabase(apartment,sql_engine,sql_metadata,sql_connection):
    '''
    '''
    apartment_id = -1

    sql_apartments_table = sql_metadata.tables['apartment_apartment']
    sql_select = sql_apartments_table.select().where(sql_apartments_table.c.sourceId == apartment['sourceId'])
    sql_apartments = sql_connection.execute(sql_select)

    if sql_apartments.rowcount == 0:
        # Apartment does not exist. Add.
        id = sql_engine.execute("SELECT MAX(id) FROM apartment_apartment").fetchall()[0][0]
        if id == None:
            id = 1
        else:
            id = id+1
        apartment['id'] = id
        sql_insert = sql_apartments_table.insert().values(apartment)
        sql_result = sql_connection.execute(sql_insert)
        apartment_id = sql_result.inserted_primary_key
    elif sql_apartments.rowcount > 1:
        error("There is more than one apartment with the same 'sourceId'")
    else:
        sql_apartment = sql_apartments.first()
        apartment_id = sql_apartment[0]

        # Upate fields
        stmt = sql_apartments_table.update().\
                values(sourceUrl=apartment['sourceUrl']).\
                where(sql_apartments_table.c.id == apartment_id)
        sql_connection.execute(stmt)

        warning('Tried to insert apartment that already exists: id={}'.format(apartment_id))

    return apartment_id

def apartmentsToDatabase(apartments,buildings):

    sql_engine, sql_metadata, sql_connection = dbase_setup()

    for i, apartment in enumerate(apartments):

        print(apartment['buildingRef'],buildings[i]['apartmentRef'])
        if apartment['buildingRef'] == buildings[i]['apartmentRef']:
            print('fuck yeah')

        building_id = buildingToDatabase(buildings[i],
            sql_engine,sql_metadata,sql_connection)
        apartment['building_id'] = building_id
        apartmentToDatabase(apartment,sql_engine,sql_metadata,sql_connection)

    sql_connection.close()

def buildingsToDatabase(buildings):

    sql_engine = create_engine('postgresql://postgres:iCga1kmX@localhost:5432/data')
    sql_metadata = MetaData(sql_engine,reflect=True)
    sql_connection = sql_engine.connect()

    for i, building in enumerate(buildings):
        building_id = buildingToDatabase(building,sql_engine,sql_metadata,sql_connection)

    sql_connection.close()

def jsonToDatabase(filepaths,propertyType):
    '''
    Reads JSON files with proper field names (as made by sourceToJson), and
    inserts the fields in the database.
    '''
    if propertyType == 'building':
        properties = loadCleanDictionaries(filepaths)
        buildingsToDatabase(properties)
    elif propertyType == 'apartment':
        apartments, buildings = loadCleanDictionaries(filepaths)
        apartmentsToDatabase(apartments,buildings)


source = ['toctoc','portali'][1]
propertyType = 'apartment'
commune = 'Providencia'
date = '20181017220743'

filepaths = [REALSTATE_DATA_PATH+'/{}s/{}-{}-{}.json'.format(propertyType,commune,date,source),
     REALSTATE_DATA_PATH+'/buildings/{}-{}-{}.json'.format(commune,date,source)]

jsonToDatabase(filepaths,propertyType)
