from openpyxl import load_workbook
import os

from realestate.models import RealEstate, Construction, Terrain, Asset
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document
from commune.models import Commune
from user.models import UserProfile


file = 'G:/Mi unidad/ProyectoInmobiliario/Datos/tasaciones/N-1775585 (15930247-4) Av. La Florida 9650 Casa 60 Altos de Santa Amalia La Florida inc min promesa 19-10-18.xlsx'

def importAppraisalSantander(request):

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
    wb2 = load_workbook(filename=file, read_only=True)

    solicitanteCodigo = excel_find_import(wb, wb2, "solicitanteCodigo")
    id = excel_find_import(wb, wb2, "id")
    timeModified = excel_find_import(wb, wb2, "timeModified")
    solicitanteSucursal = excel_find_import(wb, wb2, "solicitanteSucursal")
    solicitanteEjecutivo = excel_find_import(wb, wb2, "solicitanteEjecutivo")
    cliente = excel_find_import(wb, wb2, "cliente")
    clienteRut = excel_find_import(wb, wb2, "clienteRut")
    propietario = excel_find_import(wb, wb2, "propietario")
    propietarioRut = excel_find_import(wb, wb2, "propietarioRut")
    address = excel_find_import(wb, wb2, "address")
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
    print(wb2.cel['BB84'])

importAppraisalSantander(file)
