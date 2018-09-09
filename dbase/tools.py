#!/usr/bin/env python
import numpy as np
from shapely.geometry import Polygon

def polygonArea(points):
    polygon = Polygon(points)
    return float(polygon.area)

def polygonCenter(points):
    polygon = Polygon(points)
    return np.array(polygon.representative_point()).tolist()

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
