from scrapPortalInmobiliario import get_urls_PI, base_building_search_PI, building_data_PI, apartment_data_PI, house_data_PI
from scrapPortalInmobiliario import  apartment_appraisal_data_PI, house_appraisal_data_PI, clean_appraisals_PI
import codecs
import re
import json
import ast

#mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
#pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
#path = pc_path

'''
url = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
#url = 'https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
print(base_building_search_PI((url)))

'''

#mac_path2 = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario'
#pc_path2 = 'G:/Mi unidad/ProyectoInmobiliario/Datos/'
#path2 = pc_path2
#comuna = 'huechuraba' #str(input('Eija comuna: '))

'''password = 'toctocpass12'
user = 'app@usa.cl'
#user = 'covfe@cov.cl'
#user = 'the_big_lebowsky@hotmail.com'
'''
#buildings = codecs.open(path2 + comuna + '_buildings.txt', 'r', "ISO-8859-1")
#build = path2 + comuna + '_buildings.txt'

'''
for apt in buildings:
    apt = ast.literal_eval(apt)
    print(apt[4])
'''
''' 
url1 ='https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana/7004-edificio-holanda-320-nva?tp=2&op=1&iug=323&ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&i=0'
url2 = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana/7224-holanda-townhouses-nva?tp=1&op=1&iug=323&ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&i=0'
url3 = 'https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana/4005284-providencia-jose-manuel-infante-uda?tp=2&op=1&iug=323&ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&i=71'
url = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana/4238363-rancagua-bustamante-uda?tp=1&op=1&iug=323&ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&i=2'
print(house_data_PI(url))
'''

url = 'https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana/8022-edificio-galvarino-gallardo-1683-nva?tp=2&op=1&iug=323&ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&i=3'
user = 'cove@fefe.cl'
password = 'pipass123'
building = "ejemplo"
coordinates = '[-33.09383, -77.76542]'

print(clean_appraisals_PI(user, password))

