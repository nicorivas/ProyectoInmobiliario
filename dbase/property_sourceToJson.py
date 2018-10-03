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
        #save: option to save the dictionaries to JSON
        #debug: print shit
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

source = ['toctoc','portali'][1]
propertyType = 'apartment'
commune = 'providencia'
date = '2018-09-05T11-15-34'

path_i = Path(REALSTATE_DATA_PATH+'/source/{}/{}/'.format(source,date))
path_o_base = Path(REALSTATE_DATA_PATH)
filename_i = '{}_aptarment_appraisal_data_{}.json'.format(commune,source)
filepath_i = path_i / filename_i

filepaths, dictionaries = sourceToJson(source,propertyType,filepath_i,path_o_base)
