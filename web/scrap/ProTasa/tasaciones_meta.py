#Obtener metadata de los archivos de tasacion de ProTasa para generar ordenar los directorios

import os.path, time
from os import listdir, walk
import pandas as pd
import datetime

#Directorio en disco duro
pc_dir = 'D:\TASACIONES GENERALES CHILE'


def getAbsolutePath(dir):
    #retorna todos los archivos con directorios
    f = []
    for dirpath, dirnames, filenames in walk(dir):
        for file in filenames:
            f.append(os.path.join(dirpath, file))
    return(f)
def getFileDates(file):
    # retorna un dic con el directorio de un archivo, fecha de creacion y modificacion
    try:
        file_dic = {'dir': file,
                    'archivo': file.split('\\')[-1],
                    'banco': file.split('\\')[2],
                    'categoria': file.split('\\')[3],
                    'creado': datetime.datetime.utcfromtimestamp(os.path.getctime(file)),
                    'modificado': datetime.datetime.utcfromtimestamp(os.path.getmtime(file))}
    except IndexError:
        file_dic = {'dir': file,
                    'archivo': file.split('\\')[-1],
                    'creado': datetime.datetime.utcfromtimestamp(os.path.getctime(file)),
                    'modificado': datetime.datetime.utcfromtimestamp(os.path.getmtime(file))}
    return file_dic


file_list = []
for file in getAbsolutePath(pc_dir):
    file_list.append(getFileDates(file))

#file_list = json.dumps(file_list)

df = pd.DataFrame.from_dict(file_list)
print(df)

df.to_excel(pc_dir+'/lista_tasaciones.xlsx')
