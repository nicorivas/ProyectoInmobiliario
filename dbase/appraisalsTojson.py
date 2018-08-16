import pandas as pd
import codecs

'''Functions that takes a bank's appraisal of a property in a Excel form and returns a json'''

file = '/Volumes/GoogleDrive/Mi unidad/ProyectoInmobiliario/Informes/N-1762594 (9910373-6) Bartolome Coleone 8248 Las Condes.xlsx'

df = pd.read_excel(file, sheet_name='INFORME TASACION')

print(df)
