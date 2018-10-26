from scrapTocToc import apartment_appraisal_data_TT, building_data_TT, apartment_data_TT, house_data_TT, house_appraisal_data_TT
import codecs
import json
import ast
import os
import datetime

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-TocTocScript.py. This is an UPDATE from 2-TocTocDataScrape.py
The script run through the entire list of buildings and registers all properties which couldn't retrieve data in error_list'''

numeroReg = str(input('Region: '))
mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/' + numeroReg + '/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/' + numeroReg + '/'
base_dir = pc_path

n_archivo = str(input('Numero de archivo: '))
comunas = codecs.open(base_dir + numeroReg + '_comunas' + n_archivo + '.txt', 'r', 'utf-8-sig')


password = 'toctocpass123'

#CORREGIR USUARIOS
users = ['the_big_lebowsky@hotmail.com', 'palpo@nad.cl', 'covfefe@cove.cl', 'papi@damefunk.cl', ]


for com in comunas:
    com = com.strip().replace(' ', '-')
    date = str(datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))
    base_path = base_dir + str(com) + '/TocToc/'
    path2 = base_path + date
    os.makedirs(path2)
    print(str(com))
    done_list = codecs.open(base_dir + 'list_doneTT.json', 'w', 'utf-8-sig')
    buildings = codecs.open(base_path + com + '_properties_TT.txt', 'r', "utf-8-sig") #Cambiar para que abra json
    error_list = codecs.open(path2 + '/' + com +'_error_list_TT.json', 'w', "utf-8-sig")

    building = []
    apartment_appraisals = []
    apartment = []
    house = []
    house_appraisals = []

    counter = 0

    for prop in buildings:
        prop = ast.literal_eval(prop)
        url = prop[3]
        type = prop[4]
        state = prop[2]
        name = prop[0]
        coordinates = prop[1]
        if type == 'Departamento':
            print(prop)
            print(url)
            counter += 1
            try:
                if state == 'Nuevo':
                    building.append(building_data_TT(url, name, coordinates))
                    build_data = codecs.open(path2 + '/' + str(com) + '_building_data_TT.json', 'w', "utf-8-sig")
                    json.dump(building, build_data, ensure_ascii=False, indent=1)
                    build_data.close()
                    for i in apartment_appraisal_data_TT(url, users, password, coordinates):
                        apartment_appraisals.append(i)
                        print(i)
                        apart_appraisal = codecs.open(path2 + '/' + str(com) + '_apartment_appraisal_data_TT.json',
                                                      'w', "utf-8-sig")
                        json.dump(apartment_appraisals, apart_appraisal, ensure_ascii=False, indent=1)
                        apart_appraisal.close()
                    print('apt appraisal ' + str(counter))
                else:
                    apartment.append(apartment_data_TT(url, name, coordinates))
                    apart_data = codecs.open(path2 + '/' + str(com) + '_apartment_data_TT.json', 'w', "utf-8-sig")
                    json.dump(apartment, apart_data, ensure_ascii=False, indent=1)
                    apart_data.close()
                    print('apt ' + str(counter))
            except:
                json.dump(prop, error_list, ensure_ascii=False, indent=1)
                print('error in apartment ' + str(prop))
        else:
            try:
                if state == 'Nuevo':
                    for j in house_appraisal_data_TT(url, users, password, coordinates):
                        house_appraisals.append(j)
                        print(j)
                        house_appraisal = codecs.open(path2 + '/' + str(com) + '_house_appraisal_data_TT.json',
                                                      'w',
                                                      "utf-8-sig")
                        json.dump(house_appraisals, house_appraisal, ensure_ascii=False, indent=1)
                        house_appraisal.close()
                    print('house aprraisal ' + str(counter))
                    counter += 1
                else:
                    house.append(house_data_TT(url, name, coordinates))
                    house_data = codecs.open(path2 + '/' + str(com) + '_house_data_TT.json', 'w', "utf-8-sig")
                    json.dump(house, house_data, ensure_ascii=False, indent=1)
                    house_data.close()
                    print('house ' + str(counter))
                    counter += 1
            except:
                json.dump(prop, error_list, ensure_ascii=False, indent=1)
                print('error in house ' + str(prop))
    json.dump(str(com), done_list, ensure_ascii=False, indent=1)

    buildings.close()
    error_list.close()
    done_list.close()
