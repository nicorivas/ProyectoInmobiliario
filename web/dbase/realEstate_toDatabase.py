#!/usr/bin/env python
import re # regular expressions
import requests # to call the API of Google to get lat-lon
from pathlib import Path # nice way to manage paths
import json # to save nice dictionaries
# Datetime and timezones
import datetime
from pytz import timezone
from tools import *
from globals import *
from output import *

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
from house.models import House
from region.models import Region
from commune.models import Commune

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

def coordinatesToAddress(lat,lng,out):
    '''
    Given a lat-long pair, return an address
    '''

    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url_latlng = 'latlng={},{}'.format(lat,lng)
    url_key='&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_latlng+url_key)
    resp_json_payload = response.json()
    if 'results' not in resp_json_payload.keys():
        out.error('Google returned something weird: {}'.format(resp_json_payload))
        return None
    try:
        resp_json_payload['results'][0]['address_components']
    except IndexError:
        out.error('Google returned something weird: {}'.format(resp_json_payload))
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
        elif 'administrative_area_level_3' in ac['types']:
            commune = ac['long_name']
        if 'administrative_area_level_1' in ac['types']:
            region = ac['long_name']
    if number == None:
        out.error('Address number not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]))
        return None
    if street == None:
        out.error('Address street not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]))
        return None
    if commune == None:
        out.error('Commune not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]))
        return None
    if commune == 'Los Cerrillos':
        commune = 'Cerrillos'
    if region == None:
        out.error('Region not found from lat={} lng={}: {}'.format(
            lat,lng,resp_json_payload['results'][0]))
        return None
    return [number,street,commune,region]

def setAddressFromCoords(re,out):
    address = coordinatesToAddress(re.lat,re.lng,out)
    if address == None:
        out.error('Coordinate to address failed, skipping real estate')
        return False
    else:
        number = address[0]
        street = address[1]
        commune = address[2]
        region = address[3]
        if len(number) > RealEstate._meta.get_field('addressNumber').max_length:
            out.error('Number is too long, something is weird: {}'.format(number))
            return False
        else:
            setattr(re,'addressNumber',number)
        if len(street) > RealEstate._meta.get_field('addressStreet').max_length:
            out.error('Street is too long: {}'.format(street))
            return False
        else:
            setattr(re,'addressStreet',street)
        if commune not in COMMUNE_NAME__CODE.keys():
            out.error('Commune {}, as given by Google, does not exist in our names'.format(commune))
            return False
        else:
            setattr(re,'addressCommune_id',COMMUNE_NAME__CODE[commune])
        if region not in REGION_NAME__CODE.keys():
            out.error('Region {}, as given by Google, does not exist in our names'.format(region))
            return False
        else:
            setattr(re,'addressRegion_id',REGION_NAME__CODE[region])
        setattr(re,'addressFromCoords',True)

def createRealEstate(re,re_dict,propertyType,out):
    '''
    Populates the real esatte variable of any real estate
    '''

    setattr(re,'propertyType',propertyType)

    # Automatic fields
    if propertyType == RealEstate.TYPE_APARTMENT:
        translation = [
            ('nombre_edificio','name'),
            ('codigo','sourceId'),
            ('fecha_publicacion','sourceDatePublished'),
            ('url','sourceUrl'),
            ('direccion','address')]
    elif propertyType == RealEstate.TYPE_HOUSE:
        translation = [
            ('nombre_casa','name'),
            ('codigo','sourceId'),
            ('fecha-publicacion','sourceDatePublished'),
            ('url','sourceUrl'),
            ('direccion','address')]
    for v_sc, v_db in translation:
        re_dict[v_db] = re_dict[v_sc]
    variables = re._meta.get_fields()
    for var in variables:
        if var.name in re_dict.keys():
            setattr(re,var.name,re_dict[var.name])

    if len(re.name) > 200:
        re.name = re.name[0:200]

    # Coordinates
    setattr(re,'lat',float(re_dict['coordenadas'][0]))
    setattr(re,'lng',float(re_dict['coordenadas'][1]))
    re.addressFromCoords = True

    # Others
    tz_santiago = timezone('America/Santiago')
    setattr(re,'sourceName','portali')
    setattr(re,'sourceDatePublished',
        tz_santiago.localize(
            datetime.datetime.strptime(re.sourceDatePublished,'%d-%m-%Y')
        ).isoformat())

    return True

def createBuilding(bd_dict,out):
    '''
    Creates a Building object, populated with the values of a dictionary
    '''

    out.status('Creating building')

    bd = Building()
    ret = createRealEstate(bd,bd_dict,RealEstate.TYPE_BUILDING,out)
    if ret == False:
        out.error('Creating building failed, returning')
        return False

    setattr(bd,'fromApartment',True)

    return bd

def createHouse(hs_dict,out):
    '''
    Creates a Building object, populated with the values of a dictionary
    '''

    out.status('Creating house')

    hs = House()
    ret = createRealEstate(hs,hs_dict,RealEstate.TYPE_HOUSE,out)
    if ret == False:
        out.error('Creating house failed, returning')
        return False

    v = hs_dict['precio_publicacion2'].replace('UF','').strip()
    v = v.replace('.','')
    v = v.replace(',','.')
    v = v.replace('/m²','') # strange cases
    try:
        float(v)
    except ValueError:
        out.error("Failed converting 'precio_publicacion2' = {} to float".format(v))
        return False
    setattr(hs,'marketPrice',v)

    if 'Dormitorio' in hs_dict.keys():
        try:
            setattr(hs,'bedrooms',int(hs_dict['Dormitorio']))
        except ValueError:
            out.error("Failed converting 'Dormitorio' = {} to int".format(hs_dict['Dormitorio']))
            return False
    elif 'Dormitorios' in hs_dict.keys():
        try:
            setattr(hs,'bedrooms',int(hs_dict['Dormitorios']))
        except ValueError:
            out.error("Failed converting 'Dormitorios' = {} to int".format(hs_dict['Dormitorios']))
            return False
    else:
        out.warning("'Dormitorio(s)' not found in source dictionary")

    if 'Baño' in hs_dict.keys():
        try:
            setattr(hs,'bathrooms',int(hs_dict['Baño']))
        except ValueError:
            out.error("Failed converting 'Baño' = {} to int".format(hs_dict['Baño']))
            return False
    elif 'Baños' in hs_dict.keys():
        try:
            setattr(hs,'bathrooms',int(hs_dict['Baños']))
        except ValueError:
            out.error("Failed converting 'Baños' = {} to int".format(hs_dict['Baños']))
            return False
    else:
        out.warning("'Baño(s)' not found in source dictionary")

    if 'm² construida' in hs_dict.keys():
        try:
            setattr(hs,'builtSquareMeters',float(hs_dict['m² construida']))
        except ValueError:
            out.error("Failed converting 'm² construida' = {} to float".format(hs_dict['m² construida']))
            return False
    else:
        out.warning("'m² útil' not found in source dictionary")
    if 'm² terreno' in hs_dict.keys():
        try:
            setattr(hs,'terrainSquareMeters',float(hs_dict['m² terreno']))
        except ValueError:
            out.error("Failed converting 'm² terreno' = {} to float".format(hs_dict['m² terreno']))
            return False
    else:
        out.warning("'m² terreno' not found in source dictionary")

    return hs

def createApartment(apt_dict,bd, out):

    out.status('Creating apartment')

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
        out.error("Failed converting 'precio_publicacion2' = {} to float".format(v))
        return False
    setattr(apt,'marketPrice',v)

    if 'Dormitorio' in apt_dict.keys():
        try:
            setattr(apt,'bedrooms',int(apt_dict['Dormitorio']))
        except ValueError:
            out.error("Failed converting 'Dormitorio' = {} to int".format(apt_dict['Dormitorio']))
            return False
    elif 'Dormitorios' in apt_dict.keys():
        try:
            setattr(apt,'bedrooms',int(apt_dict['Dormitorios']))
        except ValueError:
            out.error("Failed converting 'Dormitorios' = {} to int".format(apt_dict['Dormitorios']))
            return False
    else:
        out.warning("'Dormitorio(s)' not found in source dictionary")
    if 'Baño' in apt_dict.keys():
        try:
            setattr(apt,'bathrooms',int(apt_dict['Baño']))
        except ValueError:
            out.error("Failed converting 'Baño' = {} to int".format(apt_dict['Baño']))
            return False
    elif 'Baños' in apt_dict.keys():
        try:
            setattr(apt,'bathrooms',int(apt_dict['Baños']))
        except ValueError:
            out.error("Failed converting 'Baños' = {} to int".format(apt_dict['Baños']))
            return False
    else:
        out.warning("'Baño(s)' not found in source dictionary")
    if 'm² útil' in apt_dict.keys():
        try:
            setattr(apt,'usefulSquareMeters',float(apt_dict['m² útil']))
        except ValueError:
            out.error("Failed converting 'm² útil' = {} to float".format(apt_dict['m² útil']))
            return False
    else:
        out.warning("'m² útil' not found in source dictionary")
    if 'm² total' in apt_dict.keys():
        try:
            setattr(apt,'builtSquareMeters',float(apt_dict['m² total']))
        except ValueError:
            out.error("Failed converting 'm² total' = {} to float".format(apt_dict['m² total']))
            return False
    else:
        out.warning("'m² total' not found in source dictionary")

    setattr(apt,'building_in_id',bd.id)

    return apt

def realEstateExists(re,out):
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
            out.warning('Apartment doesnt have a number. Checking if duplicate by other means might be dangerous')
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
    elif re.propertyType == RealEstate.TYPE_HOUSE:
        if not re.addressFromCoords:
            try:
                tmp = House.objects.get(
                    propertyType=re.propertyType,
                    addressStreet=re.addressStreet,
                    addressNumber=re.addressNumber,
                    addressRegion=re.addressRegion,
                    addressCommune=re.addressCommune)
                return tmp
            except RealEstate.DoesNotExist:
                return None
        else:
            try:
                tmp = House.objects.get(
                    propertyType=re.propertyType,
                    lat=re.lat,
                    lng=re.lng)
                return tmp
            except RealEstate.DoesNotExist:
                return None

def dictionariesToDatabase_Apartment(re_dicts, out, ci=0, cf=None, debug=0):
    '''
    Generate the objects from dictionaries.
    This is just a wrapper function, to be able to create buildings associated
    to flats easily
    '''

    objects = []

    re_id = RealEstate.objects.latest('id').id + 1
    bd_id = Building.objects.latest('id').id + 1
    apt_id = Apartment.objects.latest('id').id + 1

    if isinstance(cf,type(None)):
        cf = len(re_dicts)

    for c, re_dict in enumerate(re_dicts):

        if c < ci or c > cf:
            continue

        out.say('{} {}'.format(c,re_dict['nombre_edificio']))
        building = createBuilding(re_dict,out)
        if isinstance(building,bool):
            if not building:
                continue
        re = realEstateExists(building,out)
        if isinstance(re,type(None)):
            # We assign address from coords here to avoid doing it if it is not
            # necessary (the RE already exists)
            if building.addressFromCoords:
                setAddressFromCoords(building,out)
            building.save()
        else:
            out.warning('Building already existed')
            building = re # building is now the one that existed

        apartment = createApartment(re_dict,building,out)
        if isinstance(apartment,bool):
            if not apartment:
                continue
        re = realEstateExists(apartment,out)
        if isinstance(re,type(None)):
            if apartment.addressFromCoords:
                setAddressFromCoords(apartment,out)
            apartment.save()
        else:
            out.warning('Apartment already existed')

        objects.append(building)
        objects.append(apartment)

    return objects

def dictionariesToDatabase_House(re_dicts, out, ci=0, cf=None, debug=0):
    '''
    Generate the objects from dictionaries, for houses.
    '''

    objects = []

    re_id = RealEstate.objects.latest('id').id + 1
    hs_id = House.objects.latest('id').id + 1

    if isinstance(cf,type(None)):
        cf = len(re_dicts)

    for c, re_dict in enumerate(re_dicts):

        if c < ci or c > cf:
            continue

        out.say('{} {}'.format(c,re_dict['nombre_casa']))

        house = createHouse(re_dict,out)
        if isinstance(house,bool) and not house:
            continue
        re = realEstateExists(house,out)
        if isinstance(re,type(None)) and house.addressFromCoords:
            setAddressFromCoords(house,out)
            house.save()
        else:
            out.warning('House already existed')

        objects.append(house)

    return objects

def dictionariesToDatabase(re_dicts,property_type,out,ci=0,cf=None,debug=1):
    '''
    Given a list of dictionaries, where every dictionary has the info
    of a real estate, then create and save objects, as defined by the django
    models.
        @re_dict: list of real estate dictionaries
        @property_type: type of property the dictionary comes from
        @out: messenger object
        ?ci: initial real estate, as index in the dictionary
        ?cf: final real estate, as index in the dictionary
        #debug: bananas pijamas
    '''

    if property_type == RealEstate.TYPE_BUILDING:
        objects = dictionariesToDatabase_Building(re_dicts,out,ci=ci,cf=cf,debug=debug)
    elif property_type == RealEstate.TYPE_APARTMENT:
        objects = dictionariesToDatabase_Apartment(re_dicts,out,ci=ci,cf=cf,debug=debug)
    elif property_type == RealEstate.TYPE_HOUSE:
        objects = dictionariesToDatabase_House(re_dicts,out,ci=ci,cf=cf,debug=debug)
    else:
        out.error("Property type not recognized")

    return objects

def sourceToDictionaries(filepath_i,out):
    '''
    Converts raw data from source, as saved by scrappers, into a dictionary,
    assuming a JSON filetype.
        @filepath_i: filename with the dictionaries
        @out: messenger object
    '''

    if not os.path.isfile(filepath_i):
        out.error("Input file doesn't exist: {}".format(filepath_i))
        return False

    filetype = str(filepath_i)[-10:].split('.')[1].strip()

    if filetype == 'txt':
        fileData = fileToString(filepath_i)
        re_dict = stringToDictionaries(fileData)
    elif filetype == 'json':
        re_dict = fileToDictionary(filepath_i)
    else:
        out.error("File format not supported: {}".format(filetype))
        exit(0)

    return re_dict

if __name__ == "__main__":

    # Create output objects
    out = Messenger(open('logs/log_{}'.format(datetime.datetime.now().isoformat()),'w'))
    out_runs = Messenger(open('logs/log_runs','a'))

    # Parameters
    source1 = ['toctoc','portali'][1]
    source2 = ['TocToc','PortalInmobiliario'][1]
    property_type = RealEstate.TYPE_HOUSE

    regions = Region.objects.filter(code=13) # solo RM por ahora

    i_c = 0
    ci = 0
    #commune = 'Puente Alto'
    commune_skip = ['Cerro Navia','Maipú','Calera de Tango','Providencia',
    'Independencia','Curacaví','Quilicura','Estación Central','San Joaquín']
    #commune_skip = []

    for region in regions:
        communes = Commune.objects.filter(region=region)
        for commune in communes:
            if commune.name in commune_skip:
                out.info('{} skipped'.format(commune))
                continue
            out.info(commune.name)

            basepath = Path(REALSTATE_DATA_PATH+'/source/{}/{}/{}'.format(
                slugify(region),
                slugify(commune),
                source2))
            dates = [a for a in glob.glob(str(basepath / '*/')) if os.path.isdir(a)]
            if len(dates) == 0:
                out.warning('{} does not have any data files'.format(commune.name))
                continue
            dates.sort(key=lambda x: os.path.getmtime(x))
            path_i = Path(dates[0])

            path_o_base = Path(REALSTATE_DATA_PATH)
            if property_type == RealEstate.TYPE_APARTMENT:
                filename_i = '{}_{}_data_{}.json'.format(
                    slugify(commune.name),
                    'aptarment',
                    source1)
            elif property_type == RealEstate.TYPE_HOUSE:
                filename_i = '{}_{}_data_{}.json'.format(
                    slugify(commune.name),
                    'house',
                    source1)
            filepath_i = path_i / filename_i

            re_dict = sourceToDictionaries(filepath_i,out)
            if isinstance(re_dict,bool) and not re_dict:
                out.warning('Failed getting dictionary from source file')
                continue

            out_runs.say('{} {} {} {}\n'.format(
                datetime.datetime.now().isoformat(),region,commune,filepath_i),
                show=False,log=True)

            if i_c == 0:
                objs = dictionariesToDatabase(re_dict,property_type,out,ci=ci)
            else:
                objs = dictionariesToDatabase(re_dict,property_type,out,ci=0)

            out_runs.say('Finished {}\n'.format(len(re_dict)),show=False,log=True)

            i_c += 1
