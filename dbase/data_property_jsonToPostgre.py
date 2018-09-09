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

def error(string):
    print('Error: '+string)

def warning(string):
    print('Warning: '+string)

def communeStringToId(communeName):
    '''
    Convert name of commune to the unique id of a commune stored in the database
    '''
    engine = create_engine('postgresql://nico:@localhost:5432/data')
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
    engine = create_engine('postgresql://nico:@localhost:5432/data')
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

def fileToString(filename=""):
    '''
    Given a filename, return a list with lines as string
        @filename: filename
    '''
    fileData = []
    try:
        file = open(filename,'r',encoding='utf-8-sig')#,encoding="ISO-8859-1")
        fileData = file.readlines()
        if len(fileData) == 0:
            error("Source file is empty!")
            exit(0)
    except FileNotFoundError:
        error("Source file not found: {}".format(filename))
        exit(0)
    return fileData

def stringToDictionaries(fileData):
    '''
    Given a list with lines as string, return a dictionary
        @fileData: list with strings, each element a property
    '''
    buildings_dict = []
    for line in fileData:
        buildings_dict.append(ast.literal_eval(line))
    return buildings_dict

def jsonToDictionaries(filepath):
    '''
    Given a filepath, which is a JSON file, load the file and return dictionaries
    '''
    dictionaries = json.load(codecs.open(filepath,'r','utf-8-sig'))
    return dictionaries

def createCleanDictionaries_Building(source, properties, debug=0, from_apartment=0):
    '''
    Create dictionaries of buildings with the variables names and styles of DB,
    taking as input the dictionaries read from the source files.
    '''

    buildings = []
    if not from_apartment:
        variables = pi_b_variables
    else:
        variables = pi_ab_variables

    c = 0

    for i in range(len(properties)):

        buildings.append({})

        for vname, vdict in variables.items():
            if not vdict['name'] in properties[i].keys():
                error("Variable '{}' not found in dictionary keys".format(vdict['name']))
            value = properties[i][vdict['name']]
            if vdict['strip']:
                value.strip()
            if vname == 'lat':
                value = float(value[0])
            if vname == 'lon':
                value = float(value[1])
            if vname == 'addressStreet' or vname == 'addressNumber':
                if source == 'toctoc':
                    if direccion.find(',') >= 0:
                        # Most probably commune was added at the end
                        warning("We're ignoring everything after the ',' in direccion: {}".format(direccion))
                        direccion = direccion[0:direccion.find(',')]
                elif source == 'portali':
                    value = value.split(',')[0]
                    value = value.strip()

                # split address street from number
                reSearch = re.search("\d+$",value)
                if reSearch == None:
                    warning('Direccion no tiene un número: {}'.format(value))
                    continue

                if vname == 'addressStreet':
                    value = value[0:reSearch.start()].strip()
                elif vname == 'addressNumber':
                    value = reSearch.group().strip()
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        error('Número no es número: '+value)
            if vname == 'addressCommune_id' or vname == 'addressRegion_id':
                # assuming format of TocToc 'Commune - Region'
                value = value.split('-')
                if vname == 'addressCommune_id':
                    value = value[0].strip()
                    value = communeStringToId(value)
                    if value == None: continue
                if vname == 'addressRegion_id':
                    value = value[1].strip()
                    value = regularizeRegionName(value)
                    value = regionStringToId(value)
                    if value == None: continue

            buildings[c][vname] = value
            if debug:
                print('{} = {}'.format(vname,value))

        buildings[c]['sourceName'] = source
        if from_apartment and source == 'portali':
            buildings[c]['addressRegion_id'] = 13
        c += 1

    return buildings

def createCleanDictionaries_Apartment(source, properties, debug=0):
    '''
    Create dictionaries of buildings with the variables names and styles of DB,
    taking as input the dictionaries read from the source files.
    '''

    apartments = []
    variables = pi_a_variables

    c = 0

    for i in range(len(properties)):

        apartments.append({})

        for vname, vdict in variables.items():
            if not vdict['name'] in properties[i].keys():
                error("Variable '{}' not found in dictionary keys".format(vdict['name']))

            value = properties[i][vdict['name']]

            if vdict['strip']:
                value.strip()
            if vname == 'lat':
                value = float(value[0])
            if vname == 'lon':
                value = float(value[1])
            if vname == 'marketPrice':
                value = value.replace('UF','').strip()
            if vdict['type'] == 'int':
                try:
                    bedrooms = int(value)
                except (ValueError, TypeError):
                    error('{} is not an int: {}'.format(vname,str(value)))
                    continue
            elif vdict['type'] == 'float':
                value = value.replace('.','')
                value = value.replace(',','.')
                try:
                    bedrooms = float(value)
                except (ValueError, TypeError):
                    error('{} is not a float: {}'.format(vname,str(value)))
                    exit(0)

            apartments[c][vname] = value

            if debug:
                print('{} = {}'.format(vname,value))

        apartments[c]['sourceName'] = source
        c += 1

    return apartments

def createCleanDictionaries(source,propertyType,properties_i,path_out_base,debug=0):
    '''
    Given a list of dictionaries, where every dictionary has the info
    of buildings, then clean the data.
        @buildingDicts: list of building dictionaries
        ?save: option to save the dictionaries to JSON
        ?debug: print shit
    '''

    global commune

    debug = 1

    if propertyType == 'building':
        properties_o = createCleanDictionaries_Building(source,properties_i,debug=debug)
    elif propertyType == 'apartment':
        buildings_o = createCleanDictionaries_Building(source,properties_i,debug=debug,from_apartment=1)
        properties_o = createCleanDictionaries_Apartment(source,properties_i,debug=debug)
    else:
        error("Property type not recognized")

    if path_out_base == None:
        error("Give 'path_out_base' argument if you want ot save")

    filepaths = []
    dictionaries = []

    filename_o = '{}-{}-{}.json'.format(
        commune,datetime.datetime.now().strftime("%Y%m%d%H%M%S"),source)
    path_o = path_out_base / '{}s/'.format(propertyType)
    filepath_o = path_o / filename_o
    file_o = open(filepath_o,'w')
    json.dump(properties_o, file_o)
    file_o.close()

    if propertyType == 'apartment':
        fp_o = [filepath_o]
        filename_o = '{}-{}-{}.json'.format(
            commune,datetime.datetime.now().strftime("%Y%m%d%H%M%S"),source)
        path_o = path_out_base / 'buildings/'
        filepath_o = path_o / filename_o
        file_o = open(filepath_o,'w')
        json.dump(buildings_o, file_o)
        file_o.close()
        properties_o = [properties_o,buildings_o]
        fp_o.append(filepath_o)
        filepath_o = fp_o

    return [filepath_o,properties_o]

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

def dictionariesToPanda(buildingDicts):
    '''
    Given a list of dictionaries, with each element the dictionary of a
    building, generate a panda DataFrame that contains the data.
    '''
    buildingsDF = pd.DataFrame.from_dict(buildingDicts)
    return buildingsDF

def dataFrameToPostgre(buildingsDF,table,if_exists='append'):
    '''
    Given a pandas' DataFrame, insert the data to the database.
    Sensitive shit, be careful.
    '''

    # Hardcoded
    engine = create_engine('postgresql://nico:@localhost:5432/data')
    if if_exists == 'append':
        # When appending, we need to first get the last id in the table
        ids = engine.execute("SELECT id FROM {}".format(table)).fetchall()
        if len(ids) > 0:
            id_i = max([d[0] for d in ids])+1
        else:
            id_i = 1
        # Then create a new column with the name of unique identifier that
        # Django uses
        buildingsDF['id'] = range(id_i,id_i+len(buildingsDF))
    elif if_exists == 'replace':
        buildingsDF['id'] = range(len(buildingsDF))

    # Do the thing you do.
    # We dont want the automatic indexing so index=False
    buildingsDF.to_sql(table, engine, if_exists=if_exists, index=False)
    return 0

def buildingToPostgre(building,sql_engine,sql_metadata,sql_connection):

    addressNumber = building['addressNumber']
    addressStreet = building['addressStreet']
    addressCommune_id = building['addressCommune_id']
    addressRegion_id = building['addressRegion_id']

    sql_buildings_table = sql_metadata.tables['building_building']

    sql_select = sql_buildings_table.select().where(and_(
        sql_buildings_table.c.addressNumber == addressNumber,
        sql_buildings_table.c.addressStreet == addressStreet,
        sql_buildings_table.c.addressCommune_id == addressCommune_id,
        sql_buildings_table.c.addressRegion_id == addressRegion_id))
    sql_buildings = sql_connection.execute(sql_select)

    building_id = -1

    if sql_buildings.rowcount == 0:
        # Building does not exist. Add.
        id = sql_engine.execute("SELECT MAX(id) FROM building_building").fetchall()[0][0]
        if id == None:
            id = 1
        else:
            id = id+1
        building['id'] = id
        sql_insert = sql_buildings_table.insert().values(building)
        sql_result = sql_connection.execute(sql_insert)
        building_id = sql_result.inserted_primary_key[0]
    elif sql_buildings.rowcount > 1:
        error("There is more than one building with the same address!")
    else:
        building = sql_buildings.first()
        building_id = building[0]

        stmt = sql_buildings_table.update().\
                values(sourceUrl=building['sourceUrl']).\
                where(sql_buildings_table.c.id == building_id)
        sql_connection.execute(stmt)

        warning('Tried to insert building that already exists: id={}'.format(building_id))

    return building_id

def apartmentToPostgre(apartment,sql_engine,sql_metadata,sql_connection):
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

    sql_engine = create_engine('postgresql://nico:@localhost:5432/data')
    sql_metadata = MetaData(sql_engine,reflect=True)
    sql_connection = sql_engine.connect()

    for i, apartment in enumerate(apartments):
        building_id = buildingToPostgre(buildings[i],
            sql_engine,sql_metadata,sql_connection)
        apartment['building_id'] = building_id
        apartmentToPostgre(apartment,sql_engine,sql_metadata,sql_connection)

    sql_connection.close()

def buildingsToDatabase(buildings):

    sql_engine = create_engine('postgresql://nico:@localhost:5432/data')
    sql_metadata = MetaData(sql_engine,reflect=True)
    sql_connection = sql_engine.connect()

    for i, building in enumerate(buildings):
        building_id = buildingToPostgre(building,sql_engine,sql_metadata,sql_connection)

    sql_connection.close()

def sourceToJson(source,propertyType,filepath_i,path_o):
    '''
    Converts raw data from source, as saved by scrappers, into a JSON that has
    the format, field names and structure of our database.
    '''
    if not os.path.isfile(filepath_i):
        error("Input file doesn't exist: {}".format(filepath_i))
        exit(0)

    filetype = str(filepath_i)[-10:].split('.')[1].strip()

    if filetype == 'txt':
        fileData = fileToString(filepath_i)
        properties = stringToDictionaries(fileData)
    elif filetype == 'json':
        fileData = fileToString(filepath_i)
        # temp fix to corrupted data
        fileData.insert(0,u'[\n')
        f = open('tmp','w');
        c = 0
        for line in fileData:
            if line.strip() == '}{':
                fileData[c] = '},{\n'
            if line.strip() == '][':
                fileData[c] = ',\n'
            if line.strip() == '][][':
                fileData[c] = ',\n'
            f.write(fileData[c])
            c += 1
        fileData.insert(c,u']\n')
        f.write(fileData[c])
        f.close()
        f = open('tmp','r')
        properties = json.load(f)[0]
    else:
        error("File format not supported: {}".format(filetype))
        exit(0)

    [filepath, properties] = createCleanDictionaries(source,propertyType,properties,path_o)
    return [filepath, properties]

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
commune = 'providencia'
date = '2018-09-05T11-15-34'

path_i = Path('../data/realestate/source/{}/{}/'.format(source,date))
path_o_base = Path('../data/realestate/')
#filename_i = '{}_{}s_data_{}.json'.format(commune,propertyType,source)
filename_i = '{}_aptarment_appraisal_data_{}.json'.format(commune,source)
filepath_i = path_i / filename_i

filepaths, dictionaries = sourceToJson(source,propertyType,filepath_i,path_o_base)

#filepaths = [
#'/Users/nico/Code/ProyectoInmobiliario/data/realestate/buildings/Providencia-20180904174356-toctoc.json',
#'/Users/nico/Code/ProyectoInmobiliario/data/realestate/apartments/Providencia-20180904174356-toctoc.json']

jsonToDatabase(filepaths,propertyType)
