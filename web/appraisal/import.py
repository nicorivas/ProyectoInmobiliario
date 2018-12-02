from openpyxl import load_workbook
import re
import sys
import os
import django
#sys.path.append('/Users/Pablo Ferreiro/ProyectoInmobiliario/web/')
sys.path.append('/Users/pabloferreiro/ProyectoInmobiliario/web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

from realestate.models import RealEstate, Construction, Terrain, Asset
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document
from commune.models import Commune
from region.models import Region
from user.models import UserProfile


file = 'G:/Mi unidad/ProyectoInmobiliario/Datos/tasaciones/N-1775585 (15930247-4) Av. La Florida 9650 Casa 60 Altos de Santa Amalia La Florida inc min promesa 19-10-18.xlsx'
file_mac = '/Volumes/GoogleDrive/Mi unidad/ProyectoInmobiliario/Datos/tasaciones/N-1775585 (15930247-4) Av. La Florida 9650 Casa 60 Altos de Santa Amalia La Florida inc min promesa 19-10-18.xlsx'


addresses = ["Las Violetas 2152, Dpto. 407", "Av. La Florida N° 9650 Casa 60","Luis Pereira 1621, Dpto E",
"Manuel Calro Vial N° 8549", "Lo Lopez N° 1469", "Río Teno n1069 (Sitio 12 Manzana 35)", "Santa Isabel n° 797, dp 1016","diogenes 332",
             "dos tristes de tigres 222, departamento 34e"]


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

def importAppraisalSantander(request):
    def convert(tude):
        try:
            multiplier = 1 if tude[-1] in ['N', 'E'] else -1
            d = float(tude[:-1].split('°')[0])
            m = float(tude[:-1].split('°')[1].split("'")[0])/60
            s = float(tude[:-1].split('°')[1].split("'")[1].split('"')[0])/3600
            return (d + m + s)*multiplier
        except ValueError:
            return tude

    def get_commune_name(commune):
        name = commune
        return name

    def excel_find_import(workbook1, workbook2, term, once=False):
        for sheet in workbook1.sheetnames:
            for row in range(1, 400):
                for col in range(1, 100):
                    cv = workbook1.get_sheet_by_name(sheet).cell(row=row, column=col).value
                    if cv == term:
                        value = workbook2.get_sheet_by_name(sheet).cell(row=row, column=col).value
                        if once: return value
                        return value


    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static/appraisal/santander-template.xlsx')
    #file = request.FILES['archivo']
    file = request
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
    addressCommune = excel_find_import(wb, wb2, "addressCommune")
    addressRegion = excel_find_import(wb, wb2, "addressRegion")
    tasadorUser = excel_find_import(wb, wb2, "tasadorUser")
    tasadorUserrut = excel_find_import(wb, wb2, "tasadorUser.rut")
    lat = excel_find_import(wb, wb2, "lat")
    lng = excel_find_import(wb, wb2, "lng")
    copropiedadInmobiliaria = excel_find_import(wb, wb2, "copropiedadInmobiliaria")
    ocupante = excel_find_import(wb, wb2, "ocupante")
    tipoBien = excel_find_import(wb, wb2, "tipoBien")
    destinoSII = excel_find_import(wb, wb2, "destinoSII")
    usoActual = excel_find_import(wb, wb2, "usoActual")
    usoFuturo = excel_find_import(wb, wb2, "usoFuturo")
    permisoEdificacion = excel_find_import(wb, wb2, "permisoEdificacion")
    recepcionFinal = excel_find_import(wb, wb2, "recepcionFinal")
    expropiacion = excel_find_import(wb, wb2, "expropiacion")
    viviendaSocial = excel_find_import(wb, wb2, "viviendaSocial")
    adobe = excel_find_import(wb, wb2, "adobe")
    desmontable = excel_find_import(wb, wb2, "desmontable")
    generalDescription = excel_find_import(wb, wb2, "generalDescription")
    descripcionSectorAll = excel_find_import(wb, wb2, "descripcionSectorAll")
    programa = excel_find_import(wb, wb2, "programa")
    estructuraTerminaciones = excel_find_import(wb, wb2, "estructuraTerminaciones")
    avaluoFiscal = excel_find_import(wb, wb2, "avaluoFiscal")

    #hardcoded for now
    ws2= wb2.worksheets[0]
    valorUF = ws2['BB84'].value
    propertyType = ws2['U5'].value



    if propertyType == "Casa":
        house = House.objects.get(addressStreet=address['addressStreet'],
                                  addressNumber=address['addressNumber'],
                                  addressNumber2=address['addressNumber2'],
                                  addressCommune=Commune.objects.get(name=addressCommune.lower()))
        print(house)
    ''' 
    appraisal = Appraisal(state=0,
                          source=1,
                          tipoTasacion=1,
                          solicitante=2,
                          )
        '''
    print(solicitanteCodigo,
    id,
    timeModified,
    solicitanteSucursal,
    solicitanteEjecutivo,
    cliente,
    clienteRut,
    propietario,
    propietarioRut,
    address,
    addressCommune,
    addressRegion,
    tasadorUser,
    tasadorUserrut,
    convert(lat),
    convert(lng),
    copropiedadInmobiliaria,
    ocupante,
    tipoBien,
    destinoSII,
    usoActual,
    usoFuturo,
    permisoEdificacion,
    recepcionFinal,
    expropiacion,
    viviendaSocial,
    adobe,
    desmontable,
    generalDescription,
    descripcionSectorAll,
    programa,
    estructuraTerminaciones,
    avaluoFiscal,
    valorUF)

importAppraisalSantander(file_mac)
''' 
for address in addresses:
    print(address)
    print(get_clean_address(address))
'''
