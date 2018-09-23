#!/usr/bin/env python
import os
from subprocess import call
import numpy as np
import glob
import json
from shapely.geometry import Polygon
from shapely.geometry import Point
from globals import *

def error(string):
    print('Error: '+string)

def warning(string):
    print('Warning: '+string)

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

def dbase_create_engine(echo=False,verbose=True):
    if verbose:
        print('Connecting to database')
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://postgres:iCga1kmX@localhost:5432/data', echo=echo)
    return engine

def dbase_setup(verbose=True):
    from sqlalchemy import MetaData
    sql_engine = dbase_create_engine()
    if verbose:
        print('Downloading database metadata')
    sql_metadata = MetaData(sql_engine,reflect=True)
    if verbose:
        print('Stablishing connection with database')
    sql_connection = sql_engine.connect()
    if verbose:
        print('Database ready')
    return sql_engine, sql_metadata, sql_connection

def shape_simplify(filepath_in,filepath_out,ref=1000,verbose=False):
    '''
    Simplifies a shape geometry so that it contains less points.
        @filepath_in: path or list of paths for input file
        @filepath_out: path or list of paths for output files
        -ref: point proximity distance to count as one
        -verbose: print things
        #returns: list of filepaths created
    '''
    if not isinstance(filepath_in, list):
        filepath_in = [filepath_in]
    if not isinstance(filepath_out, list):
        filepath_out = [filepath_out]

    if verbose:
        print('Simplifying geometries ({}):'.format(ref))

    for i, fpi in enumerate(filepath_in):
        if verbose:
            print(filepath_in[i][filepath_in[i].find('/',-40):])
        cmd_simplify = ['ogr2ogr',
            '{}'.format(filepath_out[i]),
            '{}'.format(filepath_in[i]),
            '-simplify',str(ref)]
        call(cmd_simplify)

    return filepath_out

def shape_to_json(filepath_in,filepath_out,verbose=0):
    '''
    Convert shape files to GeoJSON (and convert coordinate system)
        @filepath_in: path or list of paths for input file
        @filepath_out: path or list of paths for output files
        -verbose: print things
        #returns: list of filepaths created
    '''
    if not isinstance(filepath_in, list):
        filepath_in = [filepath_in]
    if not isinstance(filepath_out, list):
        filepath_out = [filepath_out]

    if verbose:
        print('Converting to GeoJSON')

    for i, fpi in enumerate(filepath_in):
        if os.path.isfile(filepath_out[i]):
            os.remove(filepath_out[i])
        if verbose:
            print(filepath_in[i][filepath_in[i].rfind('/'):])
        cmd_convert = ['ogr2ogr',
            '-f','GeoJSON',
            '-t_srs','EPSG:4326',
            '{}'.format(filepath_out[i]),
            '{}'.format(filepath_in[i])]
        call(cmd_convert)

    return filepath_out

def polygonArea(points):
    '''
    '''
    polygon = Polygon(points)
    return float(polygon.area)

def polygonCenter(points):
    try:
        polygon = Polygon(points)
    except AssertionError:
        print('Could not turn coordinates to Polygon: {}'.format(points))
        return False
    return np.array(polygon.representative_point()).tolist()

def pointToPolygonDistance(point,polygon):
    polygon = Polygon(polygon)
    point = Point(point)
    return float(point.distance(polygon))

def getPolygonCoordinates(entity):

    for coords in entity['geometry']['coordinates']:
        coords = np.array(coords)
        if len(coords.shape) == 1:
            # There are many polygons
            coords = [np.array(c) for c in coords]
            return coords
        elif len(coords.shape) == 3:
            if coords.shape[0] == 1:
                return coords
        else:
            return [coords]

def loadGreenspaces(commune=''):

    path = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/areasverde/json/metropolitana-de-santiago/'
    filepaths_gs = glob.glob(path+'{}*'.format(commune))
    greenspaces = []
    for filepath_gs in filepaths_gs:
        file = open(filepath_gs,'r')
        greenspace = json.load(file)
        greenspaces.append(greenspace)
        file.close()
    return greenspaces

def loadCommune(commune=''):
    '''
    Given a commune name, return commune JSON data
    '''
    filepath = DATA_PATH+'/comunas/json/{}.geojson'.format(commune)
    file = open(filepath,'r')
    commune = json.load(file)
    return commune

def regularizeRegionName(region_name):
    # Regularize names of regions (WTF)
    if region_name.find('Región del') > -1:
        region_name = region_name[11:]
    if region_name.find('Región de') > -1:
        region_name = region_name[10:]
    if region_name.find('Región') > -1:
        region_name = region_name[7:]
    if region_name == "Libertador Bernardo O'Higgins":
        region_name = "Libertador General Bernardo O'Higgins"
    if region_name == "Aysén del Gral.Ibañez del Campo":
        region_name = "Aysén del General Carlos Ibáñez del Campo"
    if region_name == "Bío-Bío":
        region_name = "Biobío"
    if region_name == 'Zona sin demarcar':
        return None
    return region_name

pi_b_variables = {}
pi_b_variables['name'] = {
    'name':'nombre_proyecto',
    'read':1,
    'strip':1
}
pi_b_variables['sourceUrl'] = {
    'name':'url',
    'read':1,
    'strip':1
}
pi_b_variables['lat'] = {
    'name':'coordenadas',
    'read':1,
    'strip':0
}
pi_b_variables['lon'] = {
    'name':'coordenadas',
    'read':1,
    'strip':0
}
pi_b_variables['addressStreet'] = {
    'name':'direccion',
    'read':1,
    'strip':0
}
pi_b_variables['addressNumber'] = {
    'name':'direccion',
    'read':1,
    'strip':0
}
pi_b_variables['addressCommune_id'] = {
    'name':'comuna-region',
    'read':1,
    'strip':0
}
pi_b_variables['addressRegion_id'] = {
    'name':'comuna-region',
    'read':1,
    'strip':0
}


pi_a_variables = {}
pi_a_variables['number'] = {
    'name':'depto',
    'read':1,
    'strip':1,
    'type':'int'
}
pi_a_variables['floor'] = {
    'name':'Piso',
    'read':1,
    'strip':1,
    'type':'int'
}
pi_a_variables['bedrooms'] = {
    'name':'Dormitorios',
    'read':1,
    'strip':1,
    'type':'int'
}
pi_a_variables['bathrooms'] = {
    'name':'Baños',
    'read':1,
    'strip':1,
    'type':'int'
}
pi_a_variables['builtSquareMeters'] = {
    'name':'Total m²',
    'read':1,
    'strip':1,
    'type':'float'
}
pi_a_variables['usefulSquareMeters'] = {
    'name':'Útil m²',
    'read':1,
    'strip':1,
    'type':'float'
}
pi_a_variables['orientation'] = {
    'name':'Orientación',
    'read':1,
    'strip':1,
    'type':'char'
}
pi_a_variables['marketPrice'] = {
    'name':'Monto UF',
    'read':1,
    'strip':1,
    'type':'float'
}
pi_a_variables['sourceId'] = {
    'name':'codigo',
    'read':1,
    'strip':1,
    'type':'string'
}
pi_a_variables['sourceUrl'] = {
    'name':'url',
    'read':1,
    'strip':1,
    'type':'string'
}

pi_ab_variables = {}
pi_ab_variables['name'] = {
    'name':'edificio',
    'read':1,
    'strip':1
}
pi_ab_variables['sourceUrl'] = {
    'name':'url',
    'read':1,
    'strip':1
}
pi_ab_variables['lat'] = {
    'name':'coordenadas',
    'read':1,
    'strip':0
}
pi_ab_variables['lon'] = {
    'name':'coordenadas',
    'read':1,
    'strip':0
}
pi_ab_variables['addressStreet'] = {
    'name':'direccion',
    'read':1,
    'strip':0
}
pi_ab_variables['addressNumber'] = {
    'name':'direccion',
    'read':1,
    'strip':0
}
pi_ab_variables['addressCommune_id'] = {
    'name':'comuna',
    'read':1,
    'strip':0
}
