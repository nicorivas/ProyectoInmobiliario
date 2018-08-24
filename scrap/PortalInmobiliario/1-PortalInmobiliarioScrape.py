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

url = 'https://www.portalinmobiliario.com/venta/departamento/providencia-metropolitana?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
urls = get_urls_PI(url)

providencia_search_urls = codecs.open( path + 'providencia_urls_PI.txt', 'w+', "utf-8")

for item in urls:
    providencia_search_urls.write("%s\n" % item)
providencia_search_urls.close()

