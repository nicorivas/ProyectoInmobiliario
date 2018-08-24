from scrapTocToc import get_urls
from scrapTocToc import base_building_search
import codecs

'''
Gets urls of a search that feeds the second search that returns building name, url and type. Then it writes
the results in text files to feed the functions that get the actual data of de buildings and houses in 
the 2-TocTocDataScrape.py script.


'''

''' First step, given  a url of a search in TocToc.cl, returns all pages of that search'''

mac_path = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/'
pc_path = 'G:/Mi unidad/ProyectoInmobiliario/Datos/'
path = pc_path

#url = 'https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=Huechuraba&tipoVista=lista&viewport=-34.2878148%2C-71.70881020000002%2C-32.919451%2C-69.76899430000003&comuna=Huechuraba&region=Regi%C3%B3n%20Metropolitana&atributos=&idle=false&zoom=14&buscando=true&vuelveBuscar=false&dibujaPoligono=true&resetMapa=true&animacion=false&idZonaHomogenea=0&esPrimeraBusqueda=false'
#urls = get_urls(url)

#huechuraba_search_urls = open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_urls.txt', 'w+', "utf-8")  #PC trabajo
#huechuraba_search_urls = open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_urls.txt', 'w', "utf-8")  #desde el mac

#for item in urls:
#    huechuraba_search_urls.write("%s\n" % item)
#huechuraba_search_urls.close()



'''Second step, takes the list of urls from the previous search en returns a 
list of list with building name, url, type.'''


#search = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_urls.text', 'r', "utf-8")  #PC
#buildings = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_buildings.txt', 'w', "utf-8")  #PC


search = codecs.open(path + 'huechuraba_urls.txt', 'r', "utf-8")
buildings = codecs.open(path + 'huechuraba_buildings.txt', 'w', "utf-8")

index = 0
for url in search.readlines():
    print(index)
    for item in base_building_search(url):
        buildings.write("%s\n" % item)
    index += 1

search.close()
buildings.close()




