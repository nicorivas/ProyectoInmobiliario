from __future__ import print_function
import xlrd
import decimal
import sys
import json
import pandas as pd
import win32com.client
from datetime import datetime
import re
sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/') #para pc


class MultipleEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return super(MultipleEncoder, self).default(o)

def excel_find_general(file, term):
    # finds data by term in appraisal file
    print(term)
    ws = file
    if term == "PROPIEDAD ANALIZADA":
        for row in range(120, 200):
            for col in range(1, 10):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print('Found it')
                    for i in range(15):
                        terrainSquareMeters = ws.cell(row=row, column=col +15 + i).value
                        if not isinstance(terrainSquareMeters,(int, float)):
                            continue
                        else:
                            builtSquareMeters = ws.cell(row=row, column=col + 21+ i).value
                            print(terrainSquareMeters, builtSquareMeters)
                            return terrainSquareMeters, builtSquareMeters
    elif term == "VALOR COMERCIAL":
        for row in range(74, 120):
            for col in range(25, 60):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    col = 60
                    for i in range(15):
                        try:
                            valorUF = round(ws.cell(row=row, column=col-i).value,2)
                        except TypeError:
                            continue
                        if not isinstance(valorUF,(int, float)):
                            continue
                        else:
                            print(valorUF)
                            return valorUF
    elif term == "DESCRIPCIÓN GENERAL":
        for row in range(20, 50):
            for col in range(20, 50):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = " ".join(cv.split())
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    for i in range(15):
                        valor = ws.cell(row=row+1+i, column=col).value
                        if valor is not None:
                            print(valor)
                            return valor
    elif term == "DESCRIPCION SECTOR":
        for row in range(90, 120):
            for col in range(1, 50):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = " ".join(cv.split())
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    for i in range(15):
                        valor = ws.cell(row=row+4-i, column=col).value
                        if valor is not None:
                            print(valor)
                            return valor
    elif term == "Programa :":
        for row in range(100, 120):
            for col in range(1, 50):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = " ".join(cv.split())
                except AttributeError:
                    continue
                if cv == term or cv == "Programa:":
                    print("found it!")
                    for i in range(15):
                        valor = ws.cell(row=row+i+1, column=col).value
                        if valor is not None:
                            print(valor)
                            return valor
    elif term == "Estructura y Terminaciones :":
        for row in range(103, 120):
            for col in range(1, 50):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = " ".join(cv.split())
                except AttributeError:
                    continue
                if cv == term or cv == "Estructura y Terminaciones:":
                    print("found it!")
                    for i in range(15):
                        valor = ws.cell(row=row+i+1, column=col).value
                        if valor is not None:
                            print(valor)
                            return valor
    elif term == "Antigüedad" or term == "Vida Util" or term == "Sello de Gases" or term == "Tipo Propiedad":
        for row in range(35, 70):
            for col in range(1, 30):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    col = 6
                    feature = ws.cell(row=row, column=col).value
                    return feature
    elif term == "Total Avalúo Fiscal" or term == "N° Rol Principal" or term== "N° Rol (es) Sec.":
        for row in range(35, 70):
            for col in range(10, 30):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    col = 17
                    avaluo = ws.cell(row=row, column=col).value
                    return avaluo
    elif term == "Leyes que se Acoge":
        print(term)
        for row in range(35, 70):
            for col in range(5, 20):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    col = 10
                    ley1 = ws.cell(row=row, column=col).value
                    ley2 = ws.cell(row=row + 1, column=col).value
                    return ley1, ley2
    elif term == "Permiso Edificación":
        print(term)
        for row in range(35, 70):
            for col in range(5, 20):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    col = 10
                    permiso = ws.cell(row=row, column=col).value
                    fecha  = ws.cell(row=row, column=col + 1).value
                    return permiso, fecha
    elif term == "II. DESCRIPCIÓN GENERAL DEL BIEN TASADO":
        print(term)
        for row in range(14, 20):
            for col in range(1, 10):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    descripcion = ws.cell(row=row + 1, column=col).value
                    return descripcion
    elif term == "Sub Total Terreno" or term == "Sub Total Construcciones":
        print(term)
        for row in range(40, 70):
            for col in range(8, 15):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    metros = ws.cell(row=row, column=col - 4).value
                    return metros
    elif term == "Valor Comercial":
        for row in range(85, 100):
            for col in range(11, 20):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    valorUf = ws.cell(row=row, column=col + 3).value
                    liquidacion = ws.cell(row=row + 1, column=col + 2).value
                    return valorUf, liquidacion
    elif term == "RECEPCION FINAL N°" or term == "EXPROPIACION" or term == "VIVIENDA SOCIAL" or term == "CONST. DE ADOBE" \
            or term == "CONST. DESMONTABLES":
        if term == "RECEPCION FINAL N°":
            for row in range(20, 50):
                for col in range(30, 50):
                    cv = ws.cell(row=row, column=col).value
                    try:
                        cv = " ".join(cv.split())
                    except AttributeError:
                        continue
                    if cv == term or cv == "R. FINAL N°":
                        print("found it!")
                        valor = ws.cell(row=row, column=col + 9).value
                        return valor
        else:
            for row in range(20, 50):
                for col in range(30, 50):
                    cv = ws.cell(row=row, column=col).value
                    try:
                        cv = " ".join(cv.split())
                    except AttributeError:
                        continue
                    if cv == term:
                        print("found it!")
                        valor = ws.cell(row=row, column=col + 9).value
                        return valor
    elif term == "N°":
        for row in range(7, 35):
            for col in range(11, 20):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    numero = ws.cell(row=row, column=col + 1).value
                    return numero
    elif term == "N° Lote°":
        for row in range(7, 35):
            for col in range(11, 20):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    numero = ws.cell(row=row, column=col + 1).value
                    return numero
    elif term == "Dirección" or term =="Comuna:":
        for row in range(12, 20):
            for col in range(1, 10):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    for i in range(15):
                        word = ws.cell(row=row, column=col+1+i).value
                        if not isinstance(word,(str,)):
                            continue
                        else:
                            print(word)
                            return word
    elif term == "N° Interno Tasador" or term =="N° de Informe":
        for row in range(2, 20):
            for col in range(16, 25):
                cv = ws.cell(row=row, column=col).value
                try:
                    cv = cv.strip()
                except AttributeError:
                    continue
                if cv == term:
                    print("found it!")
                    for i in range(15):
                        id = ws.cell(row=row, column=col+1+i).value
                        if not isinstance(id,(str,int)):
                            continue
                        print(id)
                        return id

def find_general_column(file, term):
    #Search for value through columns
    ws = file
    for row in range(500):
        for col in range(100):
            cv = ws[col][row]
            try:
                cv = ' '.join(cv.split()).strip().lower()
                term = ' '.join(term.split()).strip().lower()
            except AttributeError:
                continue
            if cv == term:
                for i in range(50):
                    try:
                        element = ws[col+ 1 + i][row]
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

def find_general_row(file, term):
    #Search for value through rows
    ws = file
    for row in range(500):
        for col in range(100):
            cv = ws[col][row]
            try:
                cv = ' '.join(cv.split()).strip().lower()
                term = ' '.join(term.split()).strip().lower()
            except AttributeError:
                continue
            if cv == term:
                for i in range(50):
                    try:
                        element = ws[col][row + 1 + i]
                    except KeyError:
                        continue
                    if not isinstance(element, (int, float, str, decimal.Decimal)) or pd.isna(element):
                        continue
                    elif element in value_currency:
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

def get_values_col(file, term):
    #Toma un archivo y busca el valor según termino.
    ws = file
    elements = {}
    for row in range(500):
        for col in range(100):
            cv = ws[col][row]
            try:
                cv = ' '.join(cv.split()).strip().lower()
                term = ' '.join(term.split()).strip().lower()
            except AttributeError:
                continue
            if cv == term:
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

def get_values_row(file, term):
    #Toma un archivo y busca el valor según termino.
    ws = file
    elements = {}
    for row in range(500):
        for col in range(100):
            cv = ws[col][row]
            try:
                cv = ' '.join(cv.split()).strip().lower()
                term = ' '.join(term.split()).strip().lower()
            except AttributeError:
                continue
            if cv == term:
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
                        value = find_total_cell(file, col, row)
                        if value == False:
                            pass
                        elif not isinstance(value, bool):
                            element = ws[col][value[1]]
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

def get_square_meters(file, terrain, built):
    ws = file

    property = find_term(file, 'PROPIEDAD ANALIZADA')
    if not isinstance(property, (str, int, float, tuple)):
        property = find_term(file, 'VALORES DE TASACION')

    terrain_ = find_term(file, terrain)
    built_ = find_term(file, built)

    terrain_sq = ws[terrain_[0]][property[1]]
    built_sq = ws[built_[0]][property[1]]

    print(terrain_sq)
    return terrain_sq, built_sq



#Fields for search and search parameters
col_fields = ['ACOGIDA A',
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
row_fields = ['II. DESCRIPCIÓN GENERAL DEL BIEN TASADO',
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
value_fields = ['Valor Comercial',
                'VALOR COMERCIAL',
                'VALOR  TASACION  COMERCIAL',
                'VALOR  TASACION  LIQUIDEZ',
                'VALOR  SEGURO  RECOMENDADO',
                'VALOR TASACION COMERCIAL UF',
                'VALOR COMERCIAL TERRENO',
                'RENTA PROMEDIO MENSUAL',
                ]
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
terrain_terms = ['Terreno m²', 'Terreno', 'm² útiles terreno', 'Terreno m2']
built_terms = ['m² útiles edificación', 'Const. M²', 'Const. m2']
terrace_terms = ['m² Terrazas', 'm² terraza']
useful_terms = ['m² Utiles', 'm² útiles']

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
        print(i)
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
        df = pd.DataFrame(list(content))


        #Data Dictionary
        app_data = {}
        app_data['multiple'] = 0

        #search file for all parameters


        for field in col_fields:
            term = ' '.join(field.split()).strip().lower()
            try:
                value = find_general_column(df, term)
                app_data[term] = value
            except TypeError:
                continue

        for field in row_fields:
            term = ' '.join(field.split()).strip().lower()
            try:
                value = find_general_row(df, term)
                app_data[term] = value
            except TypeError:
                continue

        for field in value_fields:
            term = ' '.join(field.split()).strip().lower()
            try:
                dic = get_values_row(df, term)
                for key in dic:
                    app_data[key] = dic[key]
            except TypeError:
                pass
            try:
                dic = get_values_col(df, term)
                for key in dic:
                    app_data[key] = dic[key]
            except TypeError:
                continue

        try:
            sq_meters = get_square_meters(df, terrain_terms, built_terms)
            app_data['terreno'] = sq_meters[0]
            app_data['construido'] = sq_meters[1]
        except TypeError:
            pass
        try:
            sq_meters2 = get_square_meters(df, useful_terms, terrace_terms)
            app_data['terreno util'] = sq_meters2[0]
            app_data['terraza'] = sq_meters2[1]
        except TypeError:
            pass

        try:
            app_data['banos'] = findFromDescription(app_data['programa :'].replace('\n',' '))[0]
        except AttributeError:
            app_data['banos'] = "NA"
        try:
            app_data['dormitorios'] = findFromDescription(app_data['programa :'].replace('\n',' '))[1]
        except AttributeError:
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
        file_list_['extracted'][j]=True
        writer = pd.ExcelWriter('D:/TASACIONES GENERALES CHILE/lista_tasaciones.xlsx')
        file_list_.to_excel(writer, sheet_name='Sheet1', index=None)
        writer.save()
        writer.close()
        ws = None
        wb = None
        excel.Application.Quit()
        print(file_list_.loc[j]['extracted'])
        print(appraisal)

