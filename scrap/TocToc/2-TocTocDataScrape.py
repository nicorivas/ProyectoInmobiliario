from scrapTocToc import building_data, apartment_data, house_data, base_building_search

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-TocTocScript.py'''

buildings = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_buildings.txt', 'r')
build_data = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_buildings_data.txt', 'w')
apart_data = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_apt_data.txt', 'w')
house_info = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_house_data.txt', 'w')
counter = 0

for apt in buildings:
    if apt.split(',')[-1].replace(']','').replace('', '').strip("\r\n").split(' ')[1] == "'Departamento'":
        print(apt)
        counter += 1
        build_data.write("%s\n" % building_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0].replace('[', '')))
        apart_data.write("%s\n" % apartment_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0].replace('[', '')))
        print(str(counter) + ' ' + 'apartment')

    elif apt.split(',')[-1].replace(']','').replace('', '').strip("\r\n").split(' ')[1] == "'Casa'":
        print(apt)
        counter +=1
        house_info.write("%s\n" % house_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0]))
        print(str(counter) + ' ' + "house")


buildings.close()
build_data.close()
apart_data.close()
house_info.close()
