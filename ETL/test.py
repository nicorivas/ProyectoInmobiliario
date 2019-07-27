import decimal
import pandas as pd
import sys
import win32com.client
from datetime import datetime
sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/') #para pc

file = 'D:/TASACIONES GENERALES CHILE/Santander/Hipotecarias/23 5C N-901519 (15318565-4) San Martin 873 Departamento 1404 Santiago.xls'


def find_general_column(file, col, row):
    #Search for value through columns
    ws = file
    for i in range(50):
        try:
            element = ws[col+ 1 + i][row]
        except KeyError:
            continue
        if not isinstance(element, (int, float, str, decimal.Decimal, datetime)) or pd.isna(element):
            continue
        elif element in value_currency:
            continue
        elif element in excluded_terms:
            continue
        else:
            return element
def find_term(file, term):
    #takes a file and a term and returns col and row
    ws = file
    if isinstance(term, list):
        term = term
    else:
        term = [term]
    for row in range(500):
        for col in range(100):
            cv = ws[col][row]
            #try:
            #    cv = ' '.join(cv.split()).strip().lower()
            #except AttributeError:
            #    continue
            if cv in term:
                return col, row

#Fields for search and search parameters
col_fields_init = ['ACOGIDA A',
              'Antigüedad',
              'ANTIGÜEDAD',
              'AVALUO FISCAL ($)',
              'CLIENTE',
              'Codigo Banco',
              'Comuna:',
              'COMUNA  - CIUDAD',
              'COMUNA',
              'CONST. DE ADOBE',
              'CONST. DESMONTABLES',
              'COPROPIEDAD INMOB.',
              'COPROP. INMOB.',
              'DESTINO',
              'DESTINO SEGÚN SII',
              'DFL 2',
              'DFL Nº 2',
              'DIRECCIÓN',
              'Dirección',
              'DIRECCIÓN propiedad',
              'DESCRIPCION DEL BIEN',
              'EMPRESA',
              'EJECUTIVO SOLICITANTE',
              'EJECUTIVO Solicitante',
              'Estructura y Terminaciones :',
              'EXPROPIACION',
              'Latitud',
              'lat',
              'Longitud',
              'ln',
              'lon',
              'long',
              'Leyes que se Acoge',
              'MERCADO OBJETIVO',
              'N° de Informe'
              'N° Interno Tasador',
              'N° Lote°',
              'N° Rol (es) Sec.',
              'N° Rol Principal',
              'N°',
              'OCUPANTE',
              'PROPIEDAD ANALIZADA',
              'PROPIETARIO',
              'Permiso Edificación',
              'PERMISO EDIFICACIÓN N°',
              'P. EDIFICACIÓN       N°',
              'RECEPCION FINAL N°',
              'R. FINAL                  N°',
              'RECEPCIÓN  DEF (PARCIAL) N°',
              'REGION',
              'Renta Mensual (U.F.)',
              'RENTA PROMEDIO MENSUAL',
              'RENTA PROM. MENSUAL',
              'R. Liquida Anual (U.F.)',
              'RUT CLIENTE',
              'RUT TASADOR',
              'RUT propietario',
              'Sello de Gases',
              'SELLO VERDE',
              'Sub Total Construcciones',
              'Sub Total Terreno',
              'SUPERFICIE TERRENO',
              'SUPERFICIE EDIFICACION',
              'SOLICITANTE - SUCURSAL',
              'Superficie Construida',
              'Superficie Terreno',
              'SUPERFICIE TERRENO BRUTA',
              'TASADOR',
              'TIPO DE BIEN',
              'Tipo Propiedad',
              'Total Avalúo Fiscal',
              'USO ACTUAL',
              'USO FUTURO',
              'VALOR TASACION COMERCIAL UF',
              'VALOR TASACION LIQUIDEZ',
              'VALOR COMERCIAL TERRENO',
              'Vida Util',
              'VIDA UTIL REMANENTE',
              'VIVIENDA SOCIAL',
              'Cliente',
              'Propietario',
              'Ejecutivo Banco',
              'Nombre tasador',
              'Fecha de visita tasador',
              'FECHA',
              'Fecha',
              'Región / Provincia',
              'Dirección o nombre de la propiedad',
              'Número de Rol',
              'RUT O RUN cliente',
              'RUT O RUN propietario',
              'Sucursal',
              'RUT O RUN tasador',
              'Fecha de informe',
              'Comuna',
              'Destino de la propiedad(SII)',
              'Avaluo Fiscal($)'
              ]
row_fields_init = ['II. DESCRIPCIÓN GENERAL DEL BIEN TASADO',
              'DESCRIPCIÓN GENERAL',
              'DESCRIPCIÓN',
              'DESCRIPCION SECTOR',
              'Descripción, Expropiación, Plan Regulador :',
              'Estructura y Terminaciones :',
              'Programa :',
              'Programa',
              'SECTOR',
              'URBANIZACIÓN',
              'RECEPCION  FINAL',
              'NOTA']
value_fields_init = ['Valor Comercial',
                'VALOR COMERCIAL',
                'VALOR  TASACION  COMERCIAL',
                'VALOR  TASACION  LIQUIDEZ',
                'VALOR  SEGURO  RECOMENDADO',
                'VALOR TASACION COMERCIAL UF',
                'VALOR COMERCIAL TERRENO',
                'RENTA PROMEDIO MENSUAL',
                ]
all_sq_meters_terms_init = ['Terreno m²', 'Terreno', 'm² útiles terreno', 'Terreno m2','m² útiles edificación',
                       'Const. M²', 'Const. m2', 'm² Terrazas', 'm² terraza', 'm² Utiles', 'm² útiles', 'M² Útil',
                       'M² Terraza.']
col_fields = [' '.join(i.split()).strip().lower() for i in col_fields_init]
row_fields = [' '.join(i.split()).strip().lower() for i in row_fields_init]
value_fields = [' '.join(i.split()).strip().lower() for i in value_fields_init]
all_sq_meters_terms = [' '.join(i.split()).strip().lower() for i in all_sq_meters_terms_init]
value_currency = ['UF',
                  'UF.',
                  '$',
                  'U.F.',
                  'UF/m²',
                  'm²',
                  '$/m²',
                  'M $',
                  'Uf.',
                  'uf',
                  'uf.',
                  'u.f.',
                  'Uf./m2']
excluded_terms = [':', ' ', '', 'm²', 'UF/m²', 'm2','Uf./m2', '%']
sqm_table_terms = ['PROPIEDAD ANALIZADA', 'VALORES DE TASACION', 'ANALIZADA']
file_extensions = ['xls', 'xlsm', 'xlsb', 'xlsx']
StartRow = 1
EndRow = 500
StartCol = 1
EndCol = 100
bank = "Santander"   #for bank selection
category = 'Hipotecarias'
#If the file has multiple properties, set it True, else, set variable False
multiple = False



excel = win32com.client.DispatchEx('Excel.Application')
wb = excel.Workbooks.open(file)
ws = wb.Sheets(1)
excel.Visible=False
content = ws.Range(ws.Cells(StartRow, StartCol), ws.Cells(EndRow, EndCol)).Value
# Transfer content to pandas dataframe
df = pd.DataFrame(list(content))
# Transfer content to pandas dataframe

termis = find_term(df, "FECHA")
print(find_general_column(df, termis[0], termis[1]))

