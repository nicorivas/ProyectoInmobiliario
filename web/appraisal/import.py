from openpyxl import load_workbook
import re
import sys
import os
import django
sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/web/')
#sys.path.append('/Users/pabloferreiro/ProyectoInmobiliario/web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date

from realestate.models import RealEstate, Construction, Terrain, Asset
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document
from commune.models import Commune
from region.models import Region
from user.models import UserProfile


def get_clean_address(rawaddress):
    data = {}
    address = rawaddress.strip()
    n = re.findall('\d+', address)
    regex = r'\b(#\w*[^#\W]|[^#\W]\w*#)\b'.replace('#', "D")
    d = re.split(regex, rawaddress, re.I)
    if len(d) >= 1:
        data['addressNumber2'] = d[-1].strip(". ")
    if len(n) == 3:
        data['addressStreet'] = address.split(n[0])[0].strip().strip("N°n° ")
        data['addressNumber'] = n[0]
        data['addressNumber2'] = d[0]
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
    return data

def importAppraisalSantander(file):

    def convert(tude):
        #convert degrees, minutes, secods coordiantes into decimals
        try:
            multiplier = 1 if tude[-1] in ['N', 'E'] else -1
            d = float(tude[:-1].split('°')[0])
            m = float(tude[:-1].split('°')[1].split("'")[0])/60
            s = float(tude[:-1].split('°')[1].split("'")[1].split('"')[0])/3600
            return (d + m + s)*multiplier
        except ValueError:
            return tude

    def get_commune_name(commune):
        #gets commune name with first capital letter "la florida" ->"La Florida"
        name = ""
        for word in commune.split(" "):
            name += word.capitalize() + " "
        return name.strip(" ")

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
        finalDate = rawdate.split('//')[-1].strip(' ').split('-')[-1] + '-' + \
                             rawdate.split('//')[-1].strip(' ').split('-')[-2] + \
                             '-' + rawdate.split('//')[-1].strip(' ').split('-')[-3]
        return parse_date(finalDate)

    def boolean_null_choices(choice):
        options={
            "S/A":1, "S/Ant.":1,
            "Si":2, "SI":2,
            "No":3, "NO":3}
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
            'Ley 6071':7,
            'Ninguna':8,
            'Antigüedad':9
        }
        return law[text]

    def green_stamp(text):
        colors = {
            'Verde':'V',
            'Amarillo':'A',
            'Rojo':'R',
            'No Aplica':'NA',
            'Verde vencido':'VV',
            'Sin antecedentes':'SA'}
        return colors[text]

    def excel_find_import(workbook1, workbook2, term):
        #finds data of appraisal of Santander xlxs file using santander template file
        for sheet in workbook1.sheetnames:
            for row in range(1, 400):
                for col in range(1, 100):
                    cv = workbook1.get_sheet_by_name(sheet).cell(row=row, column=col).value
                    if cv == term:
                        value = workbook2.get_sheet_by_name(sheet).cell(row=row, column=col).value
                        return value




    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static/appraisal/santander-template.xlsx')
    wb = load_workbook(filename=file_path)
    wb2 = load_workbook(filename=file, read_only=True, data_only=True)

    solicitanteCodigo = excel_find_import(wb, wb2, "solicitanteCodigo")
    id = excel_find_import(wb, wb2, "id")
    timeModified = excel_find_import(wb, wb2, "timeModified")
    solicitanteSucursal = excel_find_import(wb, wb2, "solicitanteSucursal")
    solicitanteEjecutivo = excel_find_import(wb, wb2, "solicitanteEjecutivo")
    cliente = excel_find_import(wb, wb2, "cliente")
    clienteRut = excel_find_import(wb, wb2, "clienteRut")
    propietario = excel_find_import(wb, wb2, "propietario")
    propietarioRut = excel_find_import(wb, wb2, "propietarioRut")
    address = get_clean_address(excel_find_import(wb, wb2, "address"))
    addressCommune = get_commune_name(excel_find_import(wb, wb2, "addressCommune"))
    addressRegion = excel_find_import(wb, wb2, "addressRegion")
    tasadorUser = excel_find_import(wb, wb2, "tasadorUser")
    tasadorUserrut = excel_find_import(wb, wb2, "tasadorUser.rut")
    lat = convert(excel_find_import(wb, wb2, "lat"))
    lng = convert(excel_find_import(wb, wb2, "lng"))
    mercadoObjetivo = boolean_null_choices(excel_find_import(wb, wb2, "mercadoObjetivo"))
    antiguedad = excel_find_import(wb, wb2, "antiguedad")
    vidaUtil = excel_find_import(wb, wb2, "vidaUtil")
    avaluoFiscal = excel_find_import(wb, wb2, "avaluoFiscal")
    acogidaLey = law_to_database(excel_find_import(wb, wb2, "acogidaLey"))
    dfl2 = boolean_null_choices(excel_find_import(wb, wb2, "dfl2"))
    selloVerde = green_stamp(excel_find_import(wb, wb2, "selloVerde"))
    copropiedadInmobiliaria = boolean_null_choices(excel_find_import(wb, wb2, "copropiedadInmobiliaria"))
    ocupante = ocupantes_choices(excel_find_import(wb, wb2, "ocupante"))
    tipoBien = excel_find_import(wb, wb2, "tipoBien")
    destinoSII = destinoSII_modified(excel_find_import(wb, wb2, "destinoSII"))
    usoActual = destinoSII_modified(excel_find_import(wb, wb2, "usoActual"))
    usoFuturo = destinoSII_modified(excel_find_import(wb, wb2, "usoFuturo"))
    permisoEdificacion = excel_find_import(wb, wb2, "permisoEdificacion")
    recepcionFinal = excel_find_import(wb, wb2, "recepcionFinal")
    expropiacion = boolean_null_choices(excel_find_import(wb, wb2, "expropiacion"))
    viviendaSocial = boolean_null_choices(excel_find_import(wb, wb2, "viviendaSocial"))
    adobe = boolean_null_choices(excel_find_import(wb, wb2, "adobe"))
    desmontable = boolean_null_choices(excel_find_import(wb, wb2, "desmontable"))
    generalDescription = excel_find_import(wb, wb2, "generalDescription")
    descripcionSectorAll = excel_find_import(wb, wb2, "descripcionSectorAll")
    programa = excel_find_import(wb, wb2, "programa")
    estructuraTerminaciones = excel_find_import(wb, wb2, "estructuraTerminaciones")
    print(avaluoFiscal)

    #hardcoded for now
    ws2= wb2.worksheets[0]
    valorUF = round(ws2['BB84'].value,2)
    propertyType = ws2['U5'].value
    print(valorUF)

    if propertyType == "Casa":
        try:
            house = House.objects.get(addressStreet=address['addressStreet'],
                                      addressNumber=address['addressNumber'],
                                      addressNumber2=address['addressNumber2'],
                                      addressCommune=Commune.objects.get(name=addressCommune))
            house.copropiedadInmobiliaria = copropiedadInmobiliaria
            house.ocupante = ocupante
            house.tipoBien = tipoBien
            house.destinoSII = destinoSII
            house.usoActual = usoActual
            house.usoFuturo = usoFuturo
            house.permisoEdificacionNo = permisoEdificacion
            house.permisoEdificacionFecha = date_to_datetimefield(permisoEdificacion)
            house.recepcionFinalNo = recepcionFinal
            house.recepcionFinalFecha = date_to_datetimefield(recepcionFinal)
            house.expropiacion = expropiacion
            house.viviendaSocial = viviendaSocial
            house.adobe = adobe
            house.desmontable = desmontable
            house.generalDescription = generalDescription
            house.programa = programa
            house.estructuraTerminaciones = estructuraTerminaciones
            house.avaluoFiscal = avaluoFiscal
            house.marketPrice = valorUF
            house.mercadoObjetivo = mercadoObjetivo
            house.antiguedad = antiguedad
            house.vidaUtil = vidaUtil
            house.acogidaLey = acogidaLey
            house.dfl2 = dfl2
            house.save
            print("existe")
        except ObjectDoesNotExist:
            house = House(name=address['addressStreet']+' '+address['addressNumber']+' '+address['addressNumber2'],
                            addressStreet=address['addressStreet'],
                            addressNumber=address['addressNumber'],
                            addressNumber2=address['addressNumber2'],
                            addressCommune=Commune.objects.get(name=addressCommune),
                            propertyType=RealEstate.TYPE_HOUSE,
                            lat=lat,
                            lng=lng,
                            copropiedadInmobiliaria=copropiedadInmobiliaria,
                            ocupante=ocupante,
                            tipoBien=tipoBien,
                            destinoSII=destinoSII,
                            usoActual=usoActual,
                            usoFuturo=usoFuturo,
                            permisoEdificacionNo=permisoEdificacion,
                            permisoEdificacionFecha=date_to_datetimefield(permisoEdificacion),
                            recepcionFinalNo=recepcionFinal,
                            recepcionFinalFecha=date_to_datetimefield(recepcionFinal),
                            expropiacion=expropiacion,
                            viviendaSocial=viviendaSocial,
                            adobe=adobe,
                            desmontable=desmontable,
                            generalDescription=generalDescription,
                            programa=programa,
                            estructuraTerminaciones=estructuraTerminaciones,
                            avaluoFiscal=avaluoFiscal,
                            marketPrice=valorUF,
                            mercadoObjetivo=mercadoObjetivo,
                            antiguedad=antiguedad,
                            vidaUtil=vidaUtil,
                            acogidaLey=acogidaLey,
                            dfl2=dfl2
                               )
            house.save()

            print("no existe")
            try:
                appraisal = Appraisal.objects.get(realEstate=house,
                                                  valorUF=valorUF,
                                                  tipoTasacion=1,
                                                  state=0,
                                                  source=1,
                                                  solicitanteCodigo=solicitanteCodigo,
                                                  timeFinished=timeModified
                                                  )
                appraisal.solicitante = 2
                appraisal.solicitanteOtro = id
                appraisal.solicitanteSucursal = solicitanteSucursal
                appraisal.solicitanteEjecutivo = solicitanteEjecutivo
                appraisal.cliente = cliente
                appraisal.clienteRut = clienteRut
                appraisal.propietario = propietario
                appraisal.propietarioRut = propietarioRut
                # appraisal.tasadorUser=tasadorUser
                appraisal.descripcionSector = descripcionSectorAll
                appraisal.save()

            except ObjectDoesNotExist:
                appraisal = Appraisal(state=0,
                                      source=1,
                                      tipoTasacion=1,
                                      solicitante=2,
                                      realEstate=house,
                                      solicitanteCodigo=solicitanteCodigo,
                                      solicitanteOtro=id,
                                      timeFinished=timeModified,
                                      solicitanteSucursal=solicitanteSucursal,
                                      solicitanteEjecutivo=solicitanteEjecutivo,
                                      cliente=cliente,
                                      clienteRut=clienteRut,
                                      propietario=propietario,
                                      propietarioRut=propietarioRut,
                                      #tasadorUser=tasadorUser,
                                      descripcionSector=descripcionSectorAll,
                                      valorUF=valorUF
                                      )
                appraisal.save()

    if propertyType == "Departamento":
        try:
            apartment = Apartment.objects.get(addressStreet=address['addressStreet'],
                            addressNumber=address['addressNumber'],
                            addressNumber2=address['addressNumber2'],
                            addressCommune=Commune.objects.get(name=addressCommune))
        except ObjectDoesNotExist:
            apartment = Apartment(addressStreet=address['addressStreet'],
                                    addressNumber=address['addressNumber'],
                                    addressNumber2=address['addressNumber2'],
                                    addressCommune=Commune.objects.get(name=addressCommune)
                                    )



file = 'G:/Mi unidad/ProyectoInmobiliario/Datos/tasaciones/N-1775585 (15930247-4) Av. La Florida 9650 Casa 60 Altos de Santa Amalia La Florida inc min promesa 19-10-18.xlsx'
file_mac = '/Volumes/GoogleDrive/Mi unidad/ProyectoInmobiliario/Datos/tasaciones/N-1775585 (15930247-4) Av. La Florida 9650 Casa 60 Altos de Santa Amalia La Florida inc min promesa 19-10-18.xlsx'


#importAppraisalSantander(file)

def excel_find_general(file, term):
    # finds data by term in appraisal file
    wb = load_workbook(filename=file, read_only=True, data_only=True)
    for sheet in wb.sheetnames:
        print(sheet)
        for row in range(120, 200):
            print(row)
            for col in range(1, 100):
                print(col)
                cv = wb.get_sheet_by_name(sheet).cell(row=row, column=col).value
                if cv == term:
                    print('Found it')
                    return cv

excel_find_general(file, "PROPIEDAD ANALIZADA")