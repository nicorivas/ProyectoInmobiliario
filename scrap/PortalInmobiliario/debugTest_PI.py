from scrapPortalInmobiliario import get_urls_PI, base_building_search_PI
import codecs
import re
import json
import ast

mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
path = pc_path

'''
url = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
#url = 'https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
print(base_building_search_PI((url)))

'''

mac_path2 = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/'
pc_path2 = 'G:/Mi unidad/ProyectoInmobiliario/Datos/'
path2 = pc_path2
comuna = 'huechuraba' #str(input('Eija comuna: '))

password = 'toctocpass12'
user = 'app@usa.cl'
#user = 'covfe@cov.cl'
#user = 'the_big_lebowsky@hotmail.com'

buildings = codecs.open(path2 + comuna + '_buildings.txt', 'r', "ISO-8859-1")
build = path2 + comuna + '_buildings.txt'


for apt in buildings:
    apt = ast.literal_eval(apt)
    print(apt[1])