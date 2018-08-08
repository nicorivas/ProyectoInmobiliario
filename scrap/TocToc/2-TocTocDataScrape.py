from scrapTocToc import building_data, apartment_data, house_data, base_building_search

buildings = open('G:/Mi unidad/ProyectoInmobiliario/Datos/providencia_buildings.txt', 'r')

for apt in buildings:
    print(apt.split(',')[-1].replace(']',''))

buildings.close()

