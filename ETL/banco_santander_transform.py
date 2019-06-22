from __future__ import print_function
from openpyxl import load_workbook
import openpyxl
import xlrd
import pyexcel
import re
import sys
import os
import django
import json
import pandas as pd
sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/') #para pc


def get_clean_address(rawaddress):
    data = {}
    address = rawaddress.strip()
    n = re.findall('\d+', address)
    regex = r'\b(#\w*[^#\W]|[^#\W]\w*#)\b'.replace('#', "D")
    d = re.split(regex, rawaddress, re.I)
    if len(d) >= 1:
        data['addressNumber2'] = d[-1].strip(". ")
        if len(d[0])>30:
            data['addressNumber2'] = d[-1].strip(". ").split('(')[-1].strip(")")
    print(n)
    if len(n) == 3:
        data['addressStreet'] = address.split(n[0])[0].strip().strip("N°n° ")
        data['addressNumber'] = n[0]
        print(data['addressNumber2'])
        print(2)
    elif len(n)== 2:
        data['addressStreet'] = address.split(n[0])[0].strip().strip("N°n° ")
        data['addressNumber'] = n[0]
        data['addressNumber2'] = n[1]

    else:
        print(len(d))
        data['addressStreet'] = address.split(n[0])[0].strip().strip("N°n° ")
        data['addressNumber'] = n[0]
        data['addressNumber2'] = None
        if len(d) > 1:
            data['addressNumber2'] = d[-1].strip(". ")
    if data['addressNumber2']==None:
        data['addressNumber2'] = ' '
    return data

def get_commune_name(commune):
    #gets commune name with first capital letter "la florida" ->"La Florida"
    name = ""
    for word in commune.split(" "):
        name += word.capitalize() + " "
    return name.strip(" ")

def green_stamp(text):
    colors = {
        'Verde':'V',
        'Amarillo':'A', 'Amarillo Vencido':'AV',
        'Rojo':'R',
        'No Aplica':'NA',
        'Verde vencido':'VV', 'Verde Vencido':'VV',
        'Sin antecedentes':'SA',
        'Sin Antecedentes':'SA',
        'No procede': 'SA', 'No encontrado':'SA'}
    return colors[text]

def convert(tude):
        #convert degrees, minutes, secods coordiantes into decimals
        try:
            multiplier = 1 if tude[-1] in ['N', 'E'] else -1
            d = float(tude[:-1].split('°')[0].replace(',','.'))
            m = float(tude[:-1].split('°')[1].split("'")[0].replace(',','.'))/60
            s =tude[:-1].split('°')[1].split("'")[1].split("''")[0].replace(',','.')
            s = re.sub('[^\d\.]', '', s)
            s = float(s)/3600
            print((d + m + s)*multiplier)
            return (d + m + s)*multiplier
        except ValueError:
            return 0.0

def tipoPropiedad(text):
        tipos ={
            'Casa': Building.TYPE_CASA,
            'Pc. Agrado - Eriazo': Building.TYPE_PARCELA,
            'Departamento': Building.TYPE_DEPARTAMENTO,
            'Pc. Agrorresidencial': Building.TYPE_TERRENO,
        }
        return tipos[text]

def ocupantes_choices(ocupante):
        #converts from file format to database format
        ocupante = ocupante.capitalize()
        if ocupante=='Propietario':
            ocupanteFinal='P'
        elif ocupante=='Arrendatario':
            ocupanteFinal='A'
        elif ocupante=='Sin ocupante':
            ocupanteFinal='SO'
        else:
            ocupanteFinal='O'
        return ocupanteFinal

def destinoSII_modified(destino):
        # converts from file format to database format
        listaSII= {'H-Habitacional':'H','HABITACIONAL':'H',
                'O-Oficina':'O', 'OFICINA':'O',
                'C-Comercio':'C', 'COMERCIO':'C', 'COMERCIAL':'C',
                'I-Industria':'I', 'INDUSTRIA':'I',
                'L-Bodega':'L', 'BODEGA':'L',
                'Z-Estacionamiento':'Z', 'ESTACIONAMIENTO':'Z',
                'D-Deportes y Recreación':'D','DEPORTES Y RECREACIÓN':'D',
                'E-Educación y Cultura':'E','EDUCACIÓN Y CULTURA':'E',
                'G-Hotel, Motel':'G','HOTEL, MOTEL':'G',
                'P-Administración pública':'P','ADMINISTRACIÓN PÚBLICA':'P',
                'Q-Culto':'Q', 'CULTO':'Q',
                'S-Salud':'S', 'SALUD':'S',
                'SITIO ERIAZO': 'SO',
                'PROFESIONAL (oficina)':'O'   }
        return(listaSII[destino])

def date_to_datetimefield(rawdate):
        try:
            finalDate = rawdate.split('//')[-1].strip(' ').split('-')[-1] + '-' + \
                                 rawdate.split('//')[-1].strip(' ').split('-')[-2] + \
                                 '-' + rawdate.split('//')[-1].strip(' ').split('-')[-3]
        except IndexError:
            finalDate = "1" + "-" + "1" + "-" +rawdate.split(' ')[-1]
        return parse_date(finalDate)

def boolean_null_choices(choice):
        choice = choice.strip()
        options={
            "S/A":1, "S/Ant.":1,
            "Si":2, "SI":2,
            "No":3, "NO":3,
            "No Aplica":1, " ":1, "":1}
        return options[choice]

def law_to_database(text):
        law ={
            'O.G.U. y C.':0,
            'P.R.C.':1,
            'Ley Pereira':2,
            'Ley 19583': 3,
            'Ley 19667':4,
            'Ley 19727':5,
            'Ley 20251':6,
            'Ley 6071':7, 'Ley N° 6071':7,
            'Ninguna':8,
            'Antigüedad':9
        }
        return law[text]

def convert(tude):
        #convert degrees, minutes, secods coordiantes into decimals
        try:
            multiplier = 1 if tude[-1] in ['N', 'E'] else -1
            d = float(tude[:-1].split('°')[0].replace(',','.'))
            m = float(tude[:-1].split('°')[1].split("'")[0].replace(',','.'))/60
            s =tude[:-1].split('°')[1].split("'")[1].split("''")[0].replace(',','.')
            s = re.sub('[^\d\.]', '', s)
            s = float(s)/3600
            print((d + m + s)*multiplier)
            return (d + m + s)*multiplier
        except ValueError:
            return 0.0

def tipoPropiedad(text):
        tipos ={
            'Casa': Building.TYPE_CASA,
            'Pc. Agrado - Eriazo': Building.TYPE_PARCELA,
            'Departamento': Building.TYPE_DEPARTAMENTO,
            'Pc. Agrorresidencial': Building.TYPE_TERRENO,
        }
        return tipos[text]

def ocupantes_choices(ocupante):
        #converts from file format to database format
        ocupante = ocupante.capitalize()
        if ocupante=='Propietario':
            ocupanteFinal='P'
        elif ocupante=='Arrendatario':
            ocupanteFinal='A'
        elif ocupante=='Sin ocupante':
            ocupanteFinal='SO'
        else:
            ocupanteFinal='O'
        return ocupanteFinal

def destinoSII_modified(destino):
        # converts from file format to database format
        listaSII= {'H-Habitacional':'H','HABITACIONAL':'H',
                'O-Oficina':'O', 'OFICINA':'O',
                'C-Comercio':'C', 'COMERCIO':'C', 'COMERCIAL':'C',
                'I-Industria':'I', 'INDUSTRIA':'I',
                'L-Bodega':'L', 'BODEGA':'L',
                'Z-Estacionamiento':'Z', 'ESTACIONAMIENTO':'Z',
                'D-Deportes y Recreación':'D','DEPORTES Y RECREACIÓN':'D',
                'E-Educación y Cultura':'E','EDUCACIÓN Y CULTURA':'E',
                'G-Hotel, Motel':'G','HOTEL, MOTEL':'G',
                'P-Administración pública':'P','ADMINISTRACIÓN PÚBLICA':'P',
                'Q-Culto':'Q', 'CULTO':'Q',
                'S-Salud':'S', 'SALUD':'S',
                'SITIO ERIAZO': 'SO',
                'PROFESIONAL (oficina)':'O'   }
        return(listaSII[destino])

def date_to_datetimefield(rawdate):
        try:
            finalDate = rawdate.split('//')[-1].strip(' ').split('-')[-1] + '-' + \
                                 rawdate.split('//')[-1].strip(' ').split('-')[-2] + \
                                 '-' + rawdate.split('//')[-1].strip(' ').split('-')[-3]
        except IndexError:
            finalDate = "1" + "-" + "1" + "-" +rawdate.split(' ')[-1]
        return parse_date(finalDate)

def boolean_null_choices(choice):
        choice = choice.strip()
        options={
            "S/A":1, "S/Ant.":1,
            "Si":2, "SI":2,
            "No":3, "NO":3,
            "No Aplica":1, " ":1, "":1}
        return options[choice]

def law_to_database(text):
        law ={
            'O.G.U. y C.':0,
            'P.R.C.':1,
            'Ley Pereira':2,
            'Ley 19583': 3,
            'Ley 19667':4,
            'Ley 19727':5,
            'Ley 20251':6,
            'Ley 6071':7, 'Ley N° 6071':7,
            'Ninguna':8,
            'Antigüedad':9
        }
        return law[text]