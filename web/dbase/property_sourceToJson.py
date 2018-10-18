#!/usr/bin/env python
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
from globals import *
import os.path
import random

def createBuilding(source,realestate,variables,debug=0):

    status('Creating building')

    building = {}

    for vname, vdict in variables.items():
        if not vdict['name'] in realestate.keys():
            error("Variable '{}' not found in dictionary keys".format(vdict['name']))
        value = realestate[vdict['name']]
        if vdict['strip']:
            value.strip()
        if vname == 'lat':
            value = float(value[0])
        if vname == 'lng':
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

        building[vname] = value
        if debug:
            if len(str(value)) > 80:
                print('{} = {}...'.format(vname,str(value)[0:77]))
            else:
                print('{} = {}'.format(vname,value))

    building['sourceName'] = source
    building['addressCommune_id'] = COMMUNE_NAME__CODE[commune]
    building['addressRegion_id'] = REGION_NAME__CODE[region]
    building['fromApartment'] = True
    building['apartmentRef'] = random.randint(1,100000000)
    building['addressRegion_id'] = 13

    return building

def createApartment(source, realestate, variables, debug=0):

    status('Creating apartment')

    apartment = {}

    for vname, vdict in variables.items():

        exists = False
        vnamesource = ""
        for vnametmp in vdict['name']:
            if vnametmp in realestate.keys():
                vnamesource = vnametmp
                exists = True
        if not exists:
            error("Variable '{}' not found in dictionary keys = {}".format(
                vdict['name'],
                realestate.keys()))
            continue

        value = realestate[vnamesource]

        if vdict['strip']:
            value.strip()
        if vname == 'lat':
            value = float(value[0])
        if vname == 'lng':
            value = float(value[1])
        if vname == 'marketPrice':
            value = value.replace('UF','').strip()
        if vname == 'sourceDatePublished':
            value = datetime.datetime.strptime(value,'%d-%m-%Y')
            value = value.isoformat()
        if vdict['type'] == 'int':
            try:
                bedrooms = int(value)
            except (ValueError, TypeError):
                error('{} is not an int: {}'.format(vname,str(value)))
                continue
        elif vdict['type'] == 'float':
            value = value.replace('.','')
            value = value.replace(',','.')
            value = value.replace('/m²','') # some had this at the end
            try:
                bedrooms = float(value)
            except (ValueError, TypeError):
                error('{} is not a float: {}'.format(vname,str(value)))
                exit(0)

        apartment[vname] = value

        if debug:
            if len(str(value)) > 80:
                print('{} = {}...'.format(vname,str(value)[0:77]))
            else:
                print('{} = {}'.format(vname,value))

    apartment['sourceName'] = source

    return apartment

def createCleanDictionaries_Building(source, realestate, debug=0, from_apartment=0):
    '''
    Create dictionaries of buildings with the variables names and styles of DB,
    taking as input the dictionaries read from the source files.
    '''

    global commune, region

    buildings = []
    if not from_apartment:
        variables = pi_b_variables
    else:
        variables = pi_ab_variables

    for re in realestate:
        buildings.append(createBuilding(source,re,variables,debug=debug))

    return buildings

def createCleanDictionaries_Apartment(source, apartments, debug=0):
    '''
    Create dictionaries of buildings with the variables names and styles of DB,
    taking as input the dictionaries read from the source files.

    This is just a wrapper function, to be able to create buildings associated
    to flats easily
    '''

    apartments_clean = []
    buildings_clean = []

    for i in range(len(apartments)):
        print(i)
        bld = createBuilding(source,apartments[i],pi_ab_variables,debug=debug)
        buildings_clean.append(bld)
        apt = createApartment(source,apartments[i],pi_a_variables,debug=debug)
        apt['buildingRef'] = bld['apartmentRef']
        apartments_clean.append(apt)

    return apartments_clean, buildings_clean

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
        properties_o, buildings_o = createCleanDictionaries_Apartment(source,properties_i,debug=debug)
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
        properties = fileToDictionary(filepath_i)
    else:
        error("File format not supported: {}".format(filetype))
        exit(0)

    [filepath, properties] = createCleanDictionaries(source,propertyType,properties,path_o)
    return [filepath, properties]

# Parameters

source1 = ['toctoc','portali'][1]
source2 = ['TocToc','PortalInmobiliario'][1]
propertyType = 'apartment'
region = 'Metropolitana de Santiago'
commune = 'Providencia'
date = '2018-09-21T21-22-40'

# Check parameters
if region not in REGION_NAME:
    print('region not found')
    exit(0)
if commune not in COMMUNE_NAME:
    print('commune not found')
    exit(0)

path_i = Path(REALSTATE_DATA_PATH+'/source/{}/{}/{}/{}/'.format(slugify(region),commune,source2,date))
path_o_base = Path(REALSTATE_DATA_PATH)
filename_i = '{}_aptarment_data_{}.json'.format(commune,source1)
filepath_i = path_i / filename_i

filepaths, dictionaries = sourceToJson(source1,propertyType,filepath_i,path_o_base)
