#!/usr/bin/env python
import re # regular expressions
import requests # to call the API of Google to get lat-lon
from pathlib import Path # nice way to manage paths
import json # to save nice dictionaries
import codecs
import os.path
import random
# Datetime and timezones
import datetime
from pytz import timezone
import pytz
from tools import *
from globals import *

# Importing DJANGO things
import sys
import os
import django
sys.path.append('/Users/nico/Code/tasador/web/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

# Models
from realestate.models import RealEstate
from building.models import Building
from apartment.models import Apartment

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

    global logfile

    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url_latlng = 'latlng={},{}'.format(lat,lng)
    url_key='&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_latlng+url_key)
    resp_json_payload = response.json()
    if 'results' not in resp_json_payload.keys():
        error('Google returned something weird: {}'.format(resp_json_payload),logfile)
        return None
    try:
        resp_json_payload['results'][0]['address_components']
    except IndexError:
        error('Google returned something weird: {}'.format(resp_json_payload),logfile)
        return None
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
        error('Address number not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]),logfile)
        return None
    if street == None:
        error('Address street not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]),logfile)
        return None
    if commune == None:
        error('Commune not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]),logfile)
        return None
    if commune == 'Los Cerrillos':
        commune = 'Cerrillos'
    if region == None:
        error('Region not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]),logfile)
        return None
    return [number,street,commune,region]

def setAddressFromCoords(re):
    address = coordinatesToAddress(re.lat,re.lng)
    if address == None:
        error('Coordinate to address failed, skipping real estate')
        return False
    else:
        number = address[0]
        street = address[1]
        commune = address[2]
        region = address[3]
        if len(number) > RealEstate._meta.get_field('addressNumber').max_length:
            error('Number is too long, something is weird: {}'.format(number))
            return False
        else:
            setattr(re,'addressNumber',number)
        if len(street) > RealEstate._meta.get_field('addressStreet').max_length:
            error('Street is too long: {}'.format(street))
            return False
        else:
            setattr(re,'addressStreet',street)
        if commune not in COMMUNE_NAME__CODE.keys():
            error('Commune {}, as given by Google, does not exist in our names'.format(commune))
            return False
        else:
            setattr(re,'addressCommune_id',COMMUNE_NAME__CODE[commune])
        if region not in REGION_NAME__CODE.keys():
            error('Region {}, as given by Google, does not exist in our names'.format(region))
            return False
        else:
            setattr(re,'addressRegion_id',REGION_NAME__CODE[region])
        setattr(re,'addressFromCoords',True)

def createRealEstate(re,re_dict,propertyType):
    '''
    Populates the real esatte variable of any real estate
    '''

    global logfile

    # Automatic fields
    translation = [
        ('nombre_edificio','name'),
        ('codigo','sourceId'),
        ('fecha_publicacion','sourceDatePublished'),
        ('url','sourceUrl'),
        ('direccion','address')]
    for v_sc, v_db in translation:
        re_dict[v_db] = re_dict[v_sc]
    variables = re._meta.get_fields()
    for var in variables:
        if var.name in re_dict.keys():
            setattr(re,var.name,re_dict[var.name])

    # Coordinates
    setattr(re,'lat',float(re_dict['coordenadas'][0]))
    setattr(re,'lng',float(re_dict['coordenadas'][1]))
    re.addressFromCoords = True

    # Others
    tz_santiago = timezone('America/Santiago')
    setattr(re,'propertyType',propertyType)
    setattr(re,'sourceName','portali')
    setattr(re,'sourceDatePublished',
        tz_santiago.localize(
            datetime.datetime.strptime(re.sourceDatePublished,'%d-%m-%Y')
        ).isoformat())

    return True

def createBuilding(bd_dict):
    '''
    Creates a Building object, populated with the values of a dictionary
    '''

    global logfile

    status('Creating building')

    bd = Building()

    ret = createRealEstate(bd,bd_dict,propertyType=RealEstate.TYPE_BUILDING)
    if ret == False:
        error('Creating building failed, returning')
        return False

    setattr(bd,'fromApartment',True)

    return bd

def createApartment(apt_dict,bd):

    global logfile

    status('Creating apartment')

    apt = Apartment()

    ret = createRealEstate(apt,apt_dict,propertyType=RealEstate.TYPE_APARTMENT)
    if ret == False:
        error('Creating apartment failed, returning')
        return False

    v = apt_dict['precio_publicacion2'].replace('UF','').strip()
    v = v.replace('.','')
    v = v.replace(',','.')
    v = v.replace('/m²','') # strange cases
    try:
        float(v)
    except ValueError:
        error("Failed converting 'precio_publicacion2' = {} to float".format(v))
        return False
    setattr(apt,'marketPrice',v)

    if 'Dormitorio' in apt_dict.keys():
        try:
            setattr(apt,'bedrooms',int(apt_dict['Dormitorio']))
        except ValueError:
            error("Failed converting 'Dormitorio' = {} to int".format(apt_dict['Dormitorio']))
            return False
    elif 'Dormitorios' in apt_dict.keys():
        try:
            setattr(apt,'bedrooms',int(apt_dict['Dormitorios']))
        except ValueError:
            error("Failed converting 'Dormitorios' = {} to int".format(apt_dict['Dormitorios']))
            return False
    else:
        warning("'Dormitorio(s)' not found in source dictionary",logfile)
    if 'Baño' in apt_dict.keys():
        try:
            setattr(apt,'bathrooms',int(apt_dict['Baño']))
        except ValueError:
            error("Failed converting 'Baño' = {} to int".format(apt_dict['Baño']))
            return False
    elif 'Baños' in apt_dict.keys():
        try:
            setattr(apt,'bathrooms',int(apt_dict['Baños']))
        except ValueError:
            error("Failed converting 'Baños' = {} to int".format(apt_dict['Baños']))
            return False
    else:
        warning("'Baño(s)' not found in source dictionary",logfile)
    if 'm² útil' in apt_dict.keys():
        try:
            setattr(apt,'usefulSquareMeters',float(apt_dict['m² útil']))
        except ValueError:
            error("Failed converting 'm² útil' = {} to float".format(apt_dict['m² útil']))
            return False
    else:
        warning("'m² útil' not found in source dictionary",logfile)
    if 'm² total' in apt_dict.keys():
        try:
            setattr(apt,'builtSquareMeters',float(apt_dict['m² total']))
        except ValueError:
            error("Failed converting 'm² total' = {} to float".format(apt_dict['m² total']))
            return False
    else:
        warning("'m² total' not found in source dictionary",logfile)

    setattr(apt,'building_in_id',bd.id)

    return apt

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

def realEstateExists(re):
    '''
    Given any realestate object, it checks if it already exists, considering
    the two cases of the address created by coords or manually. If by coords,
    then the building exists if it has the same coords, if by hand, if it has
    the same address.
    '''
    if re.propertyType == RealEstate.TYPE_BUILDING:
        if re.addressFromCoords:
            try:
                tmp = RealEstate.objects.get(
                    propertyType=re.propertyType,
                    lat=re.lat,
                    lng=re.lng)
                return tmp
            except RealEstate.DoesNotExist:
                return None
        else:
            try:
                tmp = RealEstate.objects.get(
                    propertyType=re.propertyType,
                    addressRegion_id=re.addressRegion_id,
                    addressCommune_id=re.addressCommune_id,
                    addressSreet=re.addressStreet,
                    addressNumber=re.addressNumber)
                return tmp
            except RealEstate.DoesNotExist:
                return None
    elif re.propertyType == RealEstate.TYPE_APARTMENT:
        if isinstance(re.number,type(None)):
            warning('Apartment doesnt have a number. Checking if duplicate by other means might be dangerous')
            try:
                tmp = Apartment.objects.get(
                    bedrooms=re.bedrooms,
                    bathrooms=re.bathrooms,
                    builtSquareMeters=re.builtSquareMeters,
                    usefulSquareMeters=re.usefulSquareMeters,
                    marketPrice=re.marketPrice,
                    propertyType=re.propertyType,
                    lat=re.lat,
                    lng=re.lng)
                return tmp
            except RealEstate.DoesNotExist:
                return None
        else:
            try:
                tmp = Apartment.objects.get(
                    number=re.number,
                    propertyType=re.propertyType,
                    lat=re.lat,
                    lng=re.lng)
                return tmp
            except RealEstate.DoesNotExist:
                return None

def dictionariesToDatabase_Apartment(re_dicts, ci=0, cf=None, debug=0):
    '''
    Generate the objects from dictionaries.
    This is just a wrapper function, to be able to create buildings associated
    to flats easily
    '''

    global logfile

    objects = []

    re_id = RealEstate.objects.latest('id').id + 1
    bd_id = Building.objects.latest('id').id + 1
    apt_id = Apartment.objects.latest('id').id + 1

    if isinstance(cf,type(None)):
        cf = len(re_dicts)

    for c, re_dict in enumerate(re_dicts):

        if c < ci or c > cf:
            continue

        print('{} {}'.format(c,re_dict['nombre_edificio']))
        building = createBuilding(re_dict)
        if isinstance(building,bool):
            if not building:
                continue
        re = realEstateExists(building)
        if isinstance(re,type(None)):
            # We assign address from coords here to avoid doing it if it is not
            # necessary (the RE already exists)
            if building.addressFromCoords:
                setAddressFromCoords(building)
            building.save()
        else:
            warning('Building already existed',logfile)
            building = re # building is now the one that existed

        apartment = createApartment(re_dict,building)
        if isinstance(apartment,bool):
            if not apartment:
                continue
        re = realEstateExists(apartment)
        if isinstance(re,type(None)):
            if apartment.addressFromCoords:
                setAddressFromCoords(apartment)
            apartment.save()
        else:
            warning('Apartment already existed',logfile)

        objects.append(building)
        objects.append(apartment)

    return objects

def objectsToJson(objs):

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

def dictionariesToDatabase(re_dicts,property_type,ci=0,cf=None,debug=1):
    '''
    Given a list of dictionaries, where every dictionary has the info
    of a real estate, then create proper objects, as defined in the models.
        @re_dict: list of real estate dictionaries
        @property_type: type of property the dictionary comes from
        #debug: bananas pijamas
    '''

    global logfile, logfile_runs

    if property_type == 'building':
        objects = dictionariesToDatabase_Building(re_dicts,ci=ci,cf=cf,debug=debug)
    elif property_type == 'apartment':
        objects = dictionariesToDatabase_Apartment(re_dicts,ci=ci,cf=cf,debug=debug)
    else:
        error("Property type not recognized")

    return objects

def sourceToDictionaries(filepath_i):
    '''
    Converts raw data from source, as saved by scrappers, into a JSON that has
    the format, field names and structure of our database.
    '''

    if not os.path.isfile(filepath_i):
        error("Input file doesn't exist: {}".format(filepath_i))
        return False

    filetype = str(filepath_i)[-10:].split('.')[1].strip()

    if filetype == 'txt':
        fileData = fileToString(filepath_i)
        re_dict = stringToDictionaries(fileData)
    elif filetype == 'json':
        re_dict = fileToDictionary(filepath_i)
    else:
        error("File format not supported: {}".format(filetype))
        exit(0)

    return re_dict

# Parameters

source1 = ['toctoc','portali'][1]
source2 = ['TocToc','PortalInmobiliario'][1]
property_type = 'apartment'
region = 'Metropolitana de Santiago'
# Check parameters
if region not in REGION_NAME:
    print('region not found')
    exit(0)

logfile = open('logs/log_{}'.format(datetime.datetime.now().isoformat()),'w')
logfile_runs = open('logs/log_runs','a')

i_c = 0
ci = 266
#commune = 'Puente Alto'
commune_skip = ['Santiago','Cerrillos','Conchalí','Estación Central',
'Huechuraba','Independencia','La Cisterna','La Florida','La Reina','Las Condes',
'Macul','Maipú','Lo Barnechea','Providencia']
for commune in COMMUNE_NAME:
    if COMMUNE_NAME__CODE[commune] > REGION_NAME__CODE[region]*1000 and \
        COMMUNE_NAME__CODE[commune] < (REGION_NAME__CODE[region]+1)*1000:
        if commune in commune_skip:
            info('{} skipped'.format(commune))
            continue
        info(commune)
        basepath = Path(REALSTATE_DATA_PATH+'/source/{}/{}/{}'.format(
            slugify(region),
            slugify(commune),
            source2))
        dates = [a for a in glob.glob(str(basepath / '*/')) if os.path.isdir(a)]
        if len(dates) == 0:
            warning('{} does not have any data files'.format(commune))
            continue
        dates.sort(key=lambda x: os.path.getmtime(x))
        path_i = Path(dates[0])

        path_o_base = Path(REALSTATE_DATA_PATH)
        filename_i = '{}_aptarment_data_{}.json'.format(slugify(commune),source1)
        filepath_i = path_i / filename_i

        re_dict = sourceToDictionaries(filepath_i)
        if isinstance(re_dict,bool):
            continue

        logfile_runs.write('{} {} {} {} {}\n'.format(
            datetime.datetime.now().isoformat(),region,commune,len(re_dict),filepath_i))

        if i_c == 0:
            objs = dictionariesToDatabase(re_dict,property_type,ci=ci)
        else:
            objs = dictionariesToDatabase(re_dict,property_type,ci=0)

        logfile_runs.write('finished {}\n'.format(len(re_dict)))

        i_c += 1
        #objectsToJson(objs)
