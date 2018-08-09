#!/usr/bin/env python
import ast # to load the file (literal_eval is nicer than eval, they say)
import re # regular expressions
import requests # to call the API of Google to get lat-lon
import pandas as pd # are cute
from pathlib import Path # nice way to manage paths
import json # to save nice dictionaries

def loadJsonToString(filename=""):
    '''
    Given a filename, return a list with lines as string
        @filename: filename
    '''
    file = open(filename,'r',encoding="ISO-8859-1")
    fileData = file.readlines()
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

def createCleanDictionaries(buildingDicts,save=0,debug=0):
    '''
    Given a list of dictionaries, where every dictionary has the info
    of buildings, then clean the data.
        @buildingDicts: list of building dictionaries
        ?save: option to save the dictionaries to JSON
        ?debug: print shit
    '''

    def addressToCoordinates(address):
        '''
        Given an address (string that Google would understand)
        return coordinates in lat long
        '''
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        url_address = 'address={}'.format(address)
        response = requests.get(url+''+url_address)
        resp_json_payload = response.json()
        return resp_json_payload['results'][0]['geometry']['location']

    debug = 1
    buildingDictsTmp = []
    for i in range(len(buildingDicts)):
        buildingDictsTmp.append({})

        # NAME
        name = buildingDicts[i]['nombre'].strip()
        buildingDictsTmp[i]['name'] = name
        if debug: print('name = {}'.format(name))

        # ADDRESS AND NUMBER
        direccion = buildingDicts[i]['direccion'].strip()
        if direccion.find(',') >= 0:
            # Most probably commune was added at the end
            direccion = direccion[0:direccion.find(',')]

        # split address street from number
        reSearch = re.search("\d+$",direccion)
        addressStreet = direccion[0:reSearch.start()].strip()
        addressNumber = reSearch.group().strip()

        # check that the address street doesnt have a number.
        reSearch = re.search("\d+",addressStreet)
        if reSearch != None:
            print('Error: esta dirección tiene un número:'+addressStreet)
            exit(0)

        # check that number is a number (is this always the case?)
        try:
            addressNumber = int(addressNumber)
        except (ValueError, TypeError):
            print('Error: número no es número:'+addressNumber)
            exit(0)

        if debug:
            print("addressStreet={}".format(addressStreet))
            print("addressNumber={}".format(addressNumber))
        buildingDictsTmp[i]['addressStreet'] = addressStreet
        buildingDictsTmp[i]['addressNumber'] = addressNumber

        # COMMUNE AND REGION
        # assuming format of TocToc 'Commune - Region'
        cr = buildingDicts[i]['comuna-region'].split('-')
        addressCommune = cr[0].strip()
        addressRegion = cr[1].strip()
        buildingDictsTmp[i]['addressCommune'] = addressCommune
        buildingDictsTmp[i]['addressRegion'] = addressRegion
        if debug:
            print("addressCommune={}".format(addressCommune))
            print("addressRegion={}".format(addressRegion))

        # LATITUDE LONGITUDE
        # we use Google for this, free geocoder api, see function up
        addressForGoogle = '{}+{},+{},+{}'.format(
            addressStreet.replace(' ','+'),
            addressNumber,
            addressCommune,
            addressRegion)
        latlng = addressToCoordinates(addressForGoogle)
        if debug:
            print("latlng={}".format(latlng))
        buildingDictsTmp[i]['lat'] = float(latlng['lat'])
        buildingDictsTmp[i]['lon'] = float(latlng['lng'])

    if save:
        file = open('test_clean','w')
        json.dump(buildingDictsTmp,file)

    return buildingDictsTmp

def loadCleanDictionaries(filename):
    '''
    Given a filename, load the file, which should be in JSON format,
    and convert it to a list of dictionaries.
    '''
    f = open(filename,'r')
    buildingDicts = json.load(f)
    return buildingDicts

def dictionariesToPanda(buildingDicts):
    '''
    Given a list of dictionaries, with each element the dictionary of a
    building, generate a panda DataFrame that contains the data.
    '''
    buildingsDF = pd.DataFrame.from_dict(buildingDicts)
    return buildingsDF

def pandaToPostgre():
    '''

    '''

path = Path('../data/inmobiliario/toctoc/')
load = 1

if not load:
    filename = path / 'test.txt'
    fileData = loadJsonToString(filename)
    buildingDicts = stringToDictionaries(fileData)
    buildingDicts = createCleanDictionaries(buildingDicts,save=1)
else:
    filename = 'test_clean'
    buildingDicts = loadCleanDictionaries(filename)

buildingsDF = dictionariesToPanda(buildingDicts)
