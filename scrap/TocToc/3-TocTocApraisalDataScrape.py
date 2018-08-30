from scrapTocToc import apartment_value_data, building_data, apartment_data, house_data
import codecs
import re
import json
import ast
import os
import datetime

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-TocTocScript.py. This is an UPDATE from 2-TocTocDataScrape.py
The script run through the entire list of buildings and registers all properties which couldn't retrieve data in error_list'''

mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/TocToc/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/TocToc/'
path = pc_path
comuna = str(input('Eija comuna: '))
date = str(datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))
#commit = str(input('Commit hash: '))
path2 = path + date  #+ '-' + commit
os.makedirs(path2)


password = 'toctocpass123'
users = ['covfefe@cove.cl', 'the_big_lebowsky@hotmail.com', 'palpo@nad.cl']


#user = 'the_big_lebowsky@hotmail.com'

buildings = codecs.open(path + comuna + '_properties_TT1.txt', 'r', "utf-8-sig")
build_data = codecs.open(path2 + '/' + comuna + '_buildings_data_TT.txt', 'w', "utf-8-sig")
apart_data = codecs.open(path2 + '/' +  comuna +'_apt_data_TT.txt', 'w', "utf-8-sig")
apart_appraisal = codecs.open(path2 + '/' +  comuna +'_apt_appraisal_data_TT.txt', 'w', "utf-8-sig")
house_info = codecs.open(path2 + '/' +  comuna + '_house_data_TT.txt', 'w', "utf-8-sig")
error_list = codecs.open(path2 + '/' +  comuna +'_error_list_TT.txt', 'w', "utf-8-sig")

counter = 0
regexp = re.compile(r'compranuevo')
#buildings= json.loads(buildings)

for apt in buildings:
    apt = ast.literal_eval(apt)
    url = apt[3]
    type = apt[4]
    name = apt[0]
    house_name =apt[0]
    coordinates = apt[1]
    n = 0
    i = 0
    user = users[n]
    if type == 'Departamento':
        print(apt)
        print(url)
        counter += 1
        try:
            build_data.write("%s\n" % building_data(url, name, coordinates))
        except:
            error_list.write("%s\n" % apt)

        if regexp.search(url):
            try:
                apart_appraisal.write("%s\n" % apartment_value_data(url, user, password, coordinates))
                print('success appraisal in ' + str(apt))
                i += 1
                if i == 30:
                    n += 1
                    i = 0
                    if n == 3:
                        n = 0
            except:
                error_list.write("%s\n" % apt)
                print('error in ' + str(apt))
            print(str(counter) + ' ' + 'apartment')
        else:
            try:
                apart_data.write("%s\n" % apartment_data(url, name, coordinates))
            except:
                error_list.write("%s\n" % apt)

    elif type == 'Casa':
        print(apt)
        try:
            counter +=1
            house_info.write("%s\n" % house_data(url, house_name, coordinates))
        except:
            error_list.write("%s\n" % apt)
        print(str(counter) + ' ' + "house")


buildings.close()
build_data.close()
apart_data.close()
house_info.close()
error_list.close()