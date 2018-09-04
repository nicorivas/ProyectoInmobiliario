import codecs
import re
import json
import ast
import os
import datetime
from scrapPortalInmobiliario import building_data_PI, apartment_data_PI, apartment_appraisal_data_PI
from scrapPortalInmobiliario import house_data_PI, house_appraisal_data_PI

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-TocTocScript.py. This is an UPDATE from 2-TocTocDataScrape.py
The script run through the entire list of buildings and registers all properties which couldn't retrieve data in error_list'''

mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
path = pc_path
comuna = 'providencia' #str(input('Eija comuna: '))
date = str(datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))
#commit = str(input('Commit hash: '))
path2 = path + date  #+ '-' + commit
os.makedirs(path2)

user = 'cove@fefe.cl'
password = 'pipass123'
users = ['cove@fefe.cl','covfece@cov.cl']


buildings = codecs.open(path + comuna + '_properties_PI.txt', 'r', "utf-8-sig")

build_data = codecs.open(path2 + '/' + comuna + '_buildings_data_portali.json', 'w', "utf-8-sig")
apart_data = codecs.open(path2 + '/' +  comuna +'_aptarment_data_portali.json', 'w', "utf-8-sig")
apart_appraisal = codecs.open(path2 + '/' +  comuna +'_aptarment_appraisal_data_portali.json', 'w', "utf-8-sig")
house_info = codecs.open(path2 + '/' +  comuna + '_house_data_portali.json', 'w', "utf-8-sig")
error_list = codecs.open(path2 + '/' +  comuna +'_error_list_portali.json', 'w', "utf-8-sig")

counter = 0
#buildings= json.loads(buildings)
for prop in buildings:
    prop = ast.literal_eval(prop)
    url = prop[1]
    type = prop[0]
    state = prop[2]
    #user = users[n]
    if type == 'departamento':
        print(prop)
        print(url)
        counter += 1
        json.dump(building_data_PI(url), build_data)
        if state == 'Proyecto ':
            json.dump(apartment_appraisal_data_PI(url, user, password),apart_appraisal)
            print('NUEVO')
    else:
        continue


buildings.close()
build_data.close()
apart_data.close()
house_info.close()
error_list.close()