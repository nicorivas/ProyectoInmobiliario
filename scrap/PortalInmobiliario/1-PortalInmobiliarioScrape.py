from scrapPortalInmobiliario import get_urls_PI, base_building_search_PI
import codecs
import os
import json

'''
Gets urls of a search that feeds the second search that returns building name, url and type. Then it writes
the results in text files to feed the functions that get the actual data of de buildings and houses in 
the 2-PortalInmobiliarioScrape.py script.'''

''' First step, given  a url of a search in PortalInmobiliario.cl, returns all pages of that search'''


region = input('Introduzca numero de region: ')
pc_base_dir = 'G:/Mi unidad/ProyectoInmobiliario/Datos/'+region+'/'
mac_base_dir = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/'+region+'/'
base_dir = pc_base_dir
try:
    os.makedirs(base_dir)
except:
    pass
#agregar
numeroReg = input('Introduzca numero de region: ')
comunas = codecs.open(base_dir + numeroReg +'_comunas.txt', 'r', 'utf-8-sig')

for com in comunas:
    print(com.strip().replace(' ', '-'))
    comuna = com.strip().replace(' ', '-')
    mac_path = mac_base_dir + str(comuna) + '/PortalInmobiliario/'
    pc_path = pc_base_dir + str(comuna) + '/PortalInmobiliario/'
    path = mac_path
    try:
        os.makedirs(path)
    except:
        continue
    url = ['https://www.portalinmobiliario.com/venta/departamento/'+str(comuna)+'-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1',
           'https://www.portalinmobiliario.com/venta/casa/'+str(comuna)+'-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1']

    search_urls_PI = codecs.open(path + comuna + '_urls_PI.txt', 'w+', "utf-8")
    directory = []

    for dir in url:
        urls = get_urls_PI(dir)
        for item in urls:
            directory.append(item)
            search_urls_PI.write("%s\n" % item)
            search_urls_PI2 = codecs.open(path + comuna + '_urls_PI.json', 'w+', "utf-8")
            json.dump(directory, search_urls_PI2,ensure_ascii=False, indent=1)
            search_urls_PI2.close()
            print(item)
    search_urls_PI.close()

    '''Second step, takes the list of urls from the previous search en returns a 
    list of list with building name, url, type.'''


    search=codecs.open(path+comuna+'_urls_PI.txt', 'r', "utf-8")
    buildings = codecs.open(path + comuna + '_properties_PI.txt', 'w', "utf-8")

    index = 0
    b_directory = []
    for url in search.readlines():
        print(index)
        for item in base_building_search_PI(url):
            buildings.write("%s\n" % item)
            b_directory.append(item)
            buildings2 = codecs.open(path + comuna + '_properties_PI.json', 'w', "utf-8")
            json.dump(b_directory, buildings2, ensure_ascii=False, indent=1)
            buildings2.close()
        index += 1

    search.close()
    buildings.close()

