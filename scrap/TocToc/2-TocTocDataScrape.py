from scrapTocToc import building_data, apartment_data, house_data, base_building_search, apartment_value_data
import codecs
import re

print('THIS SCRIPT HAS BEEN DEPRECATED, use 3-TocTocApraisalDataScrape.py')

''' Scrape for the actual data of the buildings/houses, using functions on scrapTocToc.py and the basic information
 of building's urls from 1-TocTocScript.py'''
#PC path
buildings = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_buildings.txt', 'r', "utf-8")
build_data = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_buildings_data.txt', 'w', "utf-8")
apart_data = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_apt_data.txt', 'w', "utf-8")
apart_appraisal = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_apt_appraisal_data.txt', 'w', "utf-8")
house_info = codecs.open('G:/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_house_data.txt', 'w', "utf-8")

counter = 0


#Personal MAC path
'''
buildings = codecs.open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_buildings.txt', 'r', "utf-8")
build_data = codecs.open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_buildings_data.txt', 'w', "utf-8")
apart_data = codecs.open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_apt_data.txt', 'w', "utf-8")
apart_appraisal = codecs.open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_apt_appraisal_data.txt', 'w', "utf-8")
house_info = codecs.open('/Users/pabloferreiro/Google Drive File Stream/Mi unidad/ProyectoInmobiliario/Datos/huechuraba_house_data.txt', 'w', "utf-8")
counter = 0
'''
password = 'toctocpass12'
user = 'app@usa.cl'

for apt in buildings:
    if apt.split(',')[-1].replace(']','').replace('', '').strip("\r\n").split(' ')[1] == "'Departamento'":
        print(apt)
        print(apt.split(',')[-2].replace("'",""))
        counter += 1
        build_data.write("%s\n" % building_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0].replace('[', '')))
        apart_data.write("%s\n" % apartment_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0].replace('[', '')))
        #try:
        apart_appraisal.write("%s\n" % apartment_value_data(apt.split(',')[-2].replace("'",""),user , password))
        print('success appraisal in ' + apt)
        #except:
         #   print('error in ' + apt)
        #print(str(counter) + ' ' + 'apartment')

    elif apt.split(',')[-1].replace(']','').replace('', '').strip("\r\n").split(' ')[1] == "'Casa'":
        print(apt)
        counter +=1
        house_info.write("%s\n" % house_data(apt.split(',')[-2].replace("'",""), apt.split(',')[0]))
        print(str(counter) + ' ' + "house")


buildings.close()
build_data.close()
apart_data.close()
house_info.close()
