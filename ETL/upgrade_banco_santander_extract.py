from __future__ import print_function
import xlrd
import decimal
import sys
import json
import pandas as pd
import pendulum
import win32com.client
from datetime import datetime
import re
sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/') #para pc


def pendulum_to_pandas(pend_dt):
    """Converts a Pendulum datetime to a Pandas datetime

    Parameters
    -----------
    pend_dt (Pendulum.datetime): Any Pendulum datetime. Pendulum datetimes include
        nanoseconds that Pandas does not support.

    Returns
    --------
    results (Pandas friendly datetime): A Pandas friendly datetime excluding nanoseconds.
    """

    # Drop nanoseconds
    results = pend_dt.strftime("%Y-%m-%d %H:%M:%S %z")

    return results

class MultipleEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()


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

def find_general_row(file, col, row):
    #Search for value through rows
    ws = file
    for i in range(50):
        try:
            element = ws[col][row + 1 + i]
        except KeyError:
            continue
        if not isinstance(element, (int, float, str, decimal.Decimal)) or pd.isna(element):
            continue
        elif element in value_currency:
            continue
        elif element in excluded_terms:
            continue
        else:
            return element

def multiple_properties(file):
    #get values for appraisals with multiple properties
    initial_row = int(input("Indique numero de fila: "))
    initial_col = int(input("Indique numero de columna: "))
    final_row = int(input("Indique numero final de fila: "))
    ws = file
    terms_column = {}
    for col in range(17):
        term1 = str(ws[initial_col+col][initial_row])
        term2 = str(ws[initial_col+col][initial_row + 1])
        term3 = str(ws[initial_col+col][initial_row + 2])
        if term1==None:
            term1 = ''
        if term2==None:
            term2 = ''
        if term3==None:
            term3 = ''
        final_term = term1 + ' ' + term2+ ' ' + term3
        terms_column[final_term] = initial_col+col
    properties = []
    for row in range(initial_row, final_row):
        property = {}
        for term in terms_column:
            property[term] = ws[terms_column[term]][row]
        properties.append(property)
    return properties

def findFromDescription(text):
    baños = 0
    dormitorios = 0
    counter = True
    numbers = {'un':1, 'uno':1, 'dos':2, 'tres':3, 'cuatro':4,'cinco':5,
               'seis':6, 'siete':7, 'ocho':8, 'nueve':9, 'dies':10}
    bath_keyword = ['baño', 'baños', 'baño.', 'baños.']
    bedroom_keywords = ['dormitorio', 'dormitorios', 'dormitorio.', 'dormitorios.']
    for i in range(len(text.split(' '))):
        word = text.split(' ')[i].lower().strip(',').strip('.').strip(' ')
        counter = True
        try:
            wd = word.split(',')
            if wd[0] in bath_keyword or wd[0] in bedroom_keywords:
                word = wd[0]
            elif wd[1] in bath_keyword or wd[0] in bedroom_keywords:
                word = wd[1]
            else:
                pass
        except IndexError:
            pass
        if word in bath_keyword:
            try:
                baños += int(text.split(' ')[i-1].lower().strip(',').strip('.'))
                counter = False
                continue
            except ValueError:
                if text.split(' ')[i-1].lower().strip(',').strip('.') in numbers.keys():
                    baños += numbers[text.split(' ')[i-1].lower().strip(',').strip('.')]
                    counter = False
                    continue
            except IndexError:
                pass
            try:
                baños += int(text.split(' ')[i+1])
                counter = False
                continue
            except ValueError:
                if text.split(' ')[i+1].lower().strip(',').strip('.') in numbers.keys():
                    baños += numbers[text.split(' ')[i+1].lower().strip(',').strip('.')]
                    counter = False
                    continue
            except IndexError:
                pass
            if counter:
                baños += 1

        elif word in bedroom_keywords:
            try:
                dormitorios += int(text.split(' ')[i - 1].lower().strip(',').strip('.'))
                counter = False
                continue
            except ValueError:
                if text.split(' ')[i - 1].lower().strip(',').strip('.') in numbers.keys():
                    dormitorios += numbers[text.split(' ')[i - 1].lower().strip(',').strip('.')]
                    counter = False
                    continue
            except IndexError:
                pass
            try:
                dormitorios += int(text.split(' ')[i + 1])
                counter = False
                continue
            except ValueError:
                if text.split(' ')[i + 1].lower().strip(',').strip('.') in numbers.keys():
                    dormitorios += numbers[text.split(' ')[i + 1].lower().strip(',').strip('.')]
                    counter = False
                    continue
            except IndexError:
                pass
            if counter:
                dormitorios += 1

    return baños, dormitorios

def get_values_col(file, col, row):
    #Toma un archivo y busca el valor según termino.
    ws = file
    elements = {}
    currency = ""
    for i in range(50):
        element = ws[col + 1 + i][row]
        if not isinstance(element, (int, float, str, decimal.Decimal)) or pd.isna(element):
            continue
        elif element in value_currency:
            currency = element
            continue
        elif element in excluded_terms:
            continue
        else:
            if len(elements) == 0:
                elements[term+'_'+ currency +'_valor_1_col'] = element
            elif len(elements) == 1:
                elements[term+'_'+ currency +'_valor_2_col'] = element
                return elements
            else:
                return elements

def get_values_row(file, col, row):
    #Toma un archivo y busca el valor según termino.
    ws = file
    elements = {}
    currency = ""
    for i in range(50):
        element = ws[col][row + 1 + i]
        if not isinstance(element, (int, float, str, decimal.Decimal)) or pd.isna(element):
            continue
        elif element in value_currency:
            currency = element
            continue
        elif element in excluded_terms:
            continue
        else:
            if len(elements) == 0:
                elements[term+'_'+ currency +'_valor_1_row'] = element
            elif len(elements) == 1:
                elements[term+'_'+ currency +'_valor_2_row'] = element
                return elements
            else:
                return elements

def find_total_cell(file, cl, rw):
    ws = file
    for row in range(10):
        for col in range(25):
            cv = ws[col][row + rw]
            try:
                cv = ' '.join(cv.split()).strip().lower()
            except AttributeError:
                continue
            if cv == 'total' or 'Total':
                return col + cl, row + rw
    return False

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

def get_square_meters(file, col, row):
    ws = file
    sq_meters = ws[col][row]
    return sq_meters



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


#open list with files and start iteration

file_list_= pd.read_excel(r'D:/TASACIONES GENERALES CHILE/lista_tasaciones.xlsx', encoding = 'utf8')
file_list = file_list_.to_dict(orient='records')


for j, i in enumerate(file_list):
    if i['extencion'] in file_extensions and not i['extracted'] and i['banco']==bank and i['categoria']==category:
        app_meta = i
        #print(i)
        file = i['dir']
        print(file)
        name = i['archivo'].split('.')[0]

        #Open excel with pandas. Script trys to avoid encrypted file error


        excel = win32com.client.DispatchEx('Excel.Application')
        wb = excel.Workbooks.open(file)
        ws = wb.Sheets(1)
        if ws.Name == "CHECK LIST":
            ws = wb.Sheets(2)
        excel.Visible=False
        content = ws.Range(ws.Cells(StartRow, StartCol), ws.Cells(EndRow, EndCol)).Value
        # Transfer content to pandas dataframe
        content = list(content)
        for tuple in range(len(content)):
            content[tuple] = list(content[tuple])
            for x in range(len(content[tuple])):
                if isinstance(content[tuple][x], datetime):
                    content[tuple][x] = pendulum_to_pandas(content[tuple][x])
                    break

        #content.apply(lambda x: pd.to_datetime(x, utc=True) if isinstance(x,datetime) else False)
        df = pd.DataFrame(content)


        #Data Dictionary
        app_data = {}
        app_data['multiple'] = 0

        #search file for all parameters
        mark = True
        for row in range(EndRow):
            for col in range(EndCol):
                init_term = df[col][row]
                if not isinstance(init_term, (type(None), float, int, decimal.Decimal, datetime)):
                    term = ' '.join(init_term.split()).strip().lower()
                    if term in col_fields:
                        column = int(col)
                        row_ = int(row)
                        value = find_general_column(df, column, row_)
                        if isinstance(value, datetime):
                            value = pd.to_datetime(value, utc=True)
                        app_data[term] = value
                    elif term in row_fields:
                        column = int(col)
                        row_ = int(row)
                        app_data[term] = find_general_row(df, column, row_)
                    elif term in all_sq_meters_terms:
                        if mark == True:
                            try:
                                property = find_term(df, sqm_table_terms)
                                if not isinstance(property, (str, int, float, tuple)):
                                    property = find_term(df, 'VALORES DE TASACION')
                                row2 = property[1]
                                mark = False
                                app_data[term] = get_square_meters(df, col, row2)
                            except TypeError:
                                pass
                    elif term  in value_fields:
                        column = col
                        row_ = row
                        try:
                            dic =  get_values_col(df, column, row_)
                            for key in dic:
                                app_data[key] = dic[key]
                            dic = get_values_row(df, column, row_)
                            for key in dic:
                                app_data[key] = dic[key]
                        except (KeyError, TypeError):
                            pass
        try:
            app_data['banos'] = findFromDescription(app_data['programa :'].replace('\n',' '))[0]
        except (AttributeError, KeyError):
            app_data['banos'] = "NA"
        try:
            app_data['dormitorios'] = findFromDescription(app_data['programa :'].replace('\n',' '))[1]
        except (AttributeError, KeyError):
            app_data['dormitorios']  = "NA"

        #If file has multiple properties
        if multiple:
            mult_prop = multiple_properties(df)
            app_data['multiple'] = 1
            app_data['properties'] = mult_prop

        appraisal = [{'metadata': app_meta, 'appraisal_data': app_data}]
        json_file = open( 'D:/TASACIONES GENERALES CHILE/extracted files/'+bank+'/'+ name +'.json', 'w')
        json_file.write(json.dumps(appraisal, cls=MultipleEncoder, indent=4, sort_keys=True, ensure_ascii=False))
        json_file.close()
        #file_list_['extracted'][j]=True
        #writer = pd.ExcelWriter('D:/TASACIONES GENERALES CHILE/lista_tasaciones.xlsx')
        #file_list_.to_excel(writer, sheet_name='Sheet1', index=None)
        #writer.save()
        #writer.close()
        ws = None
        wb = None
        excel.Application.Quit()
        #print(file_list_.loc[j]['extracted'])
        #print(appraisal)

