import codecs
import json
import ast
import os
import datetime
from scrapPortalInmobiliario import building_data_PI, apartment_appraisal_data_PI, apartment_data_PI
from scrapPortalInmobiliario import house_data_PI, house_appraisal_data_PI

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-PortalInmobiliarioScript.py.
The script run through the entire list of buildings and registers all properties which couldn't retrieve data in error_list'''



user = 'covfece@cov.cl'
password = 'pipass123'
users = ['app@usa.com', 'cove@fefe.cl', 'covfece@cov.cl','Cotiza@cotiza.cl']

numeroReg = str(input('Region: '))
mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/' + numeroReg + '/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/PI/' + numeroReg + '/'
base_dir = mac_path

comunas = codecs.open(base_dir + numeroReg + '_comunas.txt', 'r', 'utf-8-sig')

for com in comunas:
    com = com.strip().replace(' ', '-')
    date = str(datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))
    base_path = base_dir + str(com) + '/PI/'
    path2 = base_path + date
    os.makedirs(path2)
    print(str(com))


    buildings = codecs.open(base_path + str(com) + '_properties_PI.txt', 'r', "utf-8-sig")
    error_list = codecs.open(path2 + '/' + str(com) +'_error_list_PI.json', 'w', "utf-8-sig")
    done_list = codecs.open(base_dir + 'list_done.json', 'w', 'utf-8-sig')
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
        if type == 'departamento':
            print(prop)
            print(url)
            counter += 1
            try:
                if state == 'Proyecto ':
                    building.append(building_data_PI(url))
                    build_data = codecs.open(path2 + '/' + str(com) + '_building_data_PI.json', 'w', "utf-8-sig")
                    json.dump(building, build_data, ensure_ascii=False, indent=1)
                    build_data.close()
                    for i in apartment_appraisal_data_PI(url, user, password):
                        apartment_appraisals.append(i)
                        apart_appraisal = codecs.open(path2 + '/' + str(com) + '_apartment_appraisal_data_PI.json', 'w',
                                                      "utf-8-sig")
                        json.dump(apartment_appraisals, apart_appraisal, ensure_ascii=False, indent=1)
                        apart_appraisal.close()
                    print('apt appraisal ' + str(counter))
                else:
                    apartment.append(apartment_data_PI(url))
                    apart_data = codecs.open(path2 + '/' + str(com) + '_apartment_data_PI.json', 'w', "utf-8-sig")
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
                        house_appraisal = codecs.open(path2 + '/' + str(com) + '_house_appraisal_data_PI.json', 'w',
                                                      "utf-8-sig")
                        json.dump(house_appraisals, house_appraisal, ensure_ascii=False, indent=1)
                        house_appraisal.close()
                    print('house aprraisal ' + str(counter))
                    counter += 1
                else:
                    house.append(house_data_PI(url))
                    house_data = codecs.open(path2 + '/' + str(com) + '_house_data_PI.json', 'w', "utf-8-sig")
                    json.dump(house, house_data, ensure_ascii=False, indent=1)
                    house_data.close()
                    print('house ' + str(counter))
                    counter += 1
            except:
                json.dump(prop, error_list, ensure_ascii=False, indent=1)
                print('error in ' + str(prop))
    json.dump(str(com), done_list, ensure_ascii=False, indent=1)

    buildings.close()
    error_list.close()

    done_list.close()

