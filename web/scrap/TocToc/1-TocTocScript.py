from scrapTocToc import get_urls
from scrapTocToc import base_building_search
import codecs
import os
import json
from web.region.models import Region
from web.commune.models import Commune

'''
Gets urls of a search that feeds the second search that returns building name, url and type. Then it writes
the results in text files to feed the functions that get the actual data of de buildings and houses in 
the 2-TocTocDataScrape.py script.


'''

''' First step, given  a url of a search in TocToc.cl, returns all pages of that search'''

#region = input('Introduzca numero de region: ')

#agregar
#numeroReg = input('Introduzca numero de region: ')
#comunas = codecs.open(base_dir + numeroReg +'_comunas.txt', 'r', 'utf-8-sig')
commune = Commune.objects.all()
communes = commune.filter(region=region)
regions = Region.objects.filter(code=13) # por ahora solo R.M.


for region in regions:
    pc_base_dir = 'G:/Mi unidad/ProyectoInmobiliario/Datos/realestate/'+str(region)+'/'
    mac_base_dir = '/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/'+str(region)+'/'
    base_dir = pc_base_dir
    try:
        os.makedirs(base_dir)
    except:
        pass
    for com in communes:
        print(com.strip().replace(' ', '-'))
        comuna = com.strip().replace(' ', '-')
        mac_path = mac_base_dir + str(comuna) + '/TT/'
        pc_path = pc_base_dir + str(comuna) + '/TT/'
        path = pc_path
        try:
            os.makedirs(path)
        except:
            continue

        url = 'https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda='+str(comuna)\
              +'&tipoVista=lista&viewport=-34.2878148%2C-71.70881020000002%2C-32.919451%2C-69.76899430000003&comuna='+ str(comuna) + '&region=Regi%C3%B3n%20Metropolitana&atributos=&idle=false&zoom=14&buscando=true&vuelveBuscar=false&dibujaPoligono=true&resetMapa=true&animacion=false&idZonaHomogenea=0&esPrimeraBusqueda=false'
        urls = get_urls(url)
        directory = []
        search_urls = codecs.open(path + comuna + '_urls_TT.json', 'w+', "utf-8")

        for item in urls:
            directory.append(item)
            search_urls.write("%s\n" % item)
            search_urls2 = codecs.open(path + comuna + '_urls_TT.json', 'w+', "utf-8")
            json.dump(directory, search_urls2,  ensure_ascii=False, indent=1)
            search_urls2.close
        search_urls.close()



        '''Second step, takes the list of urls from the previous search en returns a 
        list of list with building name, url, type.'''



        search = codecs.open(path + comuna + '_urls_TT.txt', 'r', "utf-8")
        buildings = codecs.open(path + comuna + '_properties_TT.txt', 'w', "utf-8")
        b_directory = []
        index = 0
        for url in search.readlines():
            print(index)
            for item in base_building_search(url):
                buildings.write("%s\n" % item)
                b_directory.append(item)
                buildings2 = codecs.open(path + comuna + '_properties_TT.json', 'w', "utf-8")
                json.dump(b_directory, buildings2, ensure_ascii=False, indent=1)
                buildings2.close()

            index += 1

        search.close()
        buildings.close()

