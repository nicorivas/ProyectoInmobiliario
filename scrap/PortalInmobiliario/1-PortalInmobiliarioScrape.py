from scrapPortalInmobiliario import get_urls_PI, base_building_search_PI
import codecs

'''
Gets urls of a search that feeds the second search that returns building name, url and type. Then it writes
the results in text files to feed the functions that get the actual data of de buildings and houses in 
the 2-PortalInmobiliarioScrape.py script.'''

''' First step, given  a url of a search in PortalInmobiliario.cl, returns all pages of that search'''

mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/PortalInmobiliario/'
path = pc_path
comuna = str(input('Elija comuna: '))

'''
url = ['https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1',
       'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1']
providencia_search_urls = codecs.open(path + 'providencia_urls_PI.txt', 'w+', "utf-8")

for dir in url:
    urls = get_urls_PI(dir)
    for item in urls:
        providencia_search_urls.write("%s\n" % item)
        print(item)
providencia_search_urls.close()

'''

'''Second step, takes the list of urls from the previous search en returns a 
list of list with building name, url, type.'''


search = codecs.open(path + 'providencia_urls_PI.txt', 'r', "utf-8")
buildings = codecs.open(path + 'providencia_properties_PI.txt', 'w', "utf-8")

index = 0
for url in search.readlines():
    print(index)
    for item in base_building_search_PI(url):
        buildings.write("%s\n" % item)
    index += 1

search.close()
buildings.close()
