import codecs
import json
import ast
import os
import datetime
from scrapPortalInmobiliario import building_data_PI, apartment_appraisal_data_PI, apartment_data_PI
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

user = 'covfece@cov.cl'
password = 'pipass123'
users = ['app@usa.com', 'cove@fefe.cl', 'covfece@cov.cl','Cotiza@cotiza.cl']


buildings = codecs.open(path + comuna + '_properties_PI2.txt', 'r', "utf-8-sig")
error_list = codecs.open(path2 + '/' + comuna +'_error_list_portali.json', 'w', "utf-8-sig")

building = []
apartment_appraisals = []
apartment = []
house = []
house_appraisals = []

counter = 0

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
        try:
            if state == 'Proyecto ':
                building.append(building_data_PI(url))
                build_data = codecs.open(path2 + '/' + comuna + '_building_data_portali.json', 'w', "utf-8-sig")
                json.dump(building, build_data, ensure_ascii=False, indent=1)
                build_data.close()
                for i in apartment_appraisal_data_PI(url, user, password):
                    apartment_appraisals.append(i)
                    apart_appraisal = codecs.open(path2 + '/' + comuna + '_aptarment_appraisal_data_portali.json', 'w',
                                                  "utf-8-sig")
                    json.dump(apartment_appraisals, apart_appraisal, ensure_ascii=False, indent=1)
                    apart_appraisal.close()
                print('apt appraisal' + str(counter))
            else:
                apartment.append(apartment_data_PI(url))
                apart_data = codecs.open(path2 + '/' + comuna + '_aptarment_data_portali.json', 'w', "utf-8-sig")
                json.dump(apartment, apart_data, ensure_ascii=False, indent=1)
                apart_data.close()
                print('apt ' + str(counter))
        except:
            json.dump(prop, error_list, ensure_ascii=False, indent=1)
            print('error in ' + str(prop))
    else:
        try:
            if state == 'Proyecto ':
                for j in house_appraisal_data_PI(url, user, password):
                    house_appraisals.append(j)
                    house_appraisal = codecs.open(path2 + '/' + comuna + '_house_appraisal_data_portali.json', 'w',
                                                  "utf-8-sig")
                    json.dump(house_appraisals, house_appraisal, ensure_ascii=False, indent=1)
                    house_appraisal.close()
                print('house aprraisal ' + str(counter))
            else:
                house.append(house_data_PI(url))
                house_data = codecs.open(path2 + '/' + comuna + '_house_data_portali.json', 'w', "utf-8-sig")
                json.dump(house, house_data, ensure_ascii=False, indent=1)
                house_data.close()
                print('house ' + str(counter))
        except:
            json.dump(prop, error_list, ensure_ascii=False, indent=1)
            print('error in ' + str(prop))


buildings.close()
error_list.close()