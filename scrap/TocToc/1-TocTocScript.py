from scrapTocToc import get_urls
from scrapTocToc import base_building_search

#Gets urls of a search thats feeds thes second search that returns building name, url and type.

#First step, given  a url of a search in TocToc.cl, returns all pages of that search
''' 
url = 'https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=Providencia&tipoVista=lista&viewport=-34.2878148%2C-71.70881020000002%2C-32.919451%2C-69.76899430000003&comuna=Providencia&region=Regi%C3%B3n%20Metropolitana&atributos=&idle=false&zoom=14&buscando=true&vuelveBuscar=false&dibujaPoligono=true&resetMapa=true&animacion=true&idZonaHomogenea=0&esPrimeraBusqueda=false'
urls = get_urls(url)

providencia_search_urls = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_urls.text', 'w')
for item in urls:
    providencia_search_urls.write("%s\n" % item)
providencia_search_urls.close()
'''
#Takes the list of urls from the previous search en returns a list of list with building name, url, type.
''' 
search = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_urls.text', 'r')
buildings = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_buildings.txt', 'w')
index = 0
for url in search.readlines():
    print(index)
    for item in base_building_search(url):
        buildings.write("%s\n" % item)
    index += 1

search.close()
buildings.close()'''

#url='https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=colina&tipoVista=lista&viewport=-34.2878148%2C-71.70881020000002%2C-32.919451%2C-69.76899430000003&comuna=Colina&region=Regi%C3%B3n%20Metropolitana&atributos=&idle=false&zoom=14&buscando=true&vuelveBuscar=false&dibujaPoligono=true&resetMapa=true&animacion=false&idZonaHomogenea=0&esPrimeraBusqueda=false'
url= 'https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=&tipoVista=lista&viewport=-33.45089597793767%2C-70.60617405725941%2C-33.44571804293457%2C-70.60308415247425&comuna=&region=&atributos=&idle=false&zoom=0&buscando=false&vuelveBuscar=false&dibujaPoligono=false&resetMapa=true&animacion=false&idZonaHomogenea=0&esPrimeraBusqueda=false'
get_urls(url)



