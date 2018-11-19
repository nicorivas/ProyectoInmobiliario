
from django.http import HttpResponse
from django.core import files

import requests
import tempfile

from realestate.models import RealEstate, Construction, Terrain, Asset
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document
from commune.models import Commune
from user.models import UserProfile

import os

from openpyxl import drawing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import load_workbook

from django.db.models import ManyToOneRel, ManyToManyRel

import datetime

def export(request,forms,appraisal,realEstate):

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir,'static/appraisal/santander-template.xlsx')

    def excel_find(workbook,term):
        for sheet in workbook:
            for row in range(1,400):
                for col in range(1,100):
                   cv = sheet.cell(row=row,column=col).value

    def excel_find_replace(workbook,term,rep):
        for sheet in workbook:
            for row in range(1,400):
                for col in range(1,100):
                   cv = sheet.cell(row=row,column=col).value
                   if cv == term:
                       sheet.cell(row=row,column=col).value = rep

    wb = load_workbook(filename=file_path)

    fields = Appraisal._meta.get_fields()
    for field in fields:
        if not isinstance(field,ManyToOneRel):
            field_name = field.deconstruct()[0]
            if field_name == 'tasadorUser':
                if isinstance(appraisal.tasadorUser,type(None)):
                    excel_find_replace(wb,field_name,'')
                else:
                    userProfile = UserProfile.objects.get(user=appraisal.tasadorUser)
                    excel_find_replace(wb,field_name,userProfile.full_name)
                    excel_find_replace(wb,field_name+'.rut',userProfile.rut_verbose)
                continue
            if len(field.choices) == 0:
                excel_find_replace(wb,field_name,getattr(appraisal,field_name))
            else:
                value = getattr(appraisal,field_name)
                for a in field.choices:
                    if a[0] == value:
                        excel_find_replace(wb,field_name,a[1])
                        break

    fields = RealEstate._meta.get_fields()
    for field in fields:
        if not isinstance(field,ManyToOneRel) and not isinstance(field,ManyToManyRel):
            field_name = field.deconstruct()[0]
            if field_name == 'tasadorUser':
                continue
            if field_name == 'antiguedad':
                continue
            if len(field.choices) == 0:
                excel_find_replace(wb,field_name,getattr(realEstate,field_name))
            else:
                value = getattr(realEstate,field_name)
                for a in field.choices:
                    if a[0] == value:
                        excel_find_replace(wb,field_name,a[1])
                        break

    year = datetime.datetime.now().year
    antiguedad = year-realEstate.anoConstruccion
    excel_find_replace(wb,'antiguedad','± '+str(antiguedad)+' años')
    excel_find_replace(wb,'vidaUtil','± '+str(realEstate.vidaUtil)+' años')
    if not isinstance(realEstate.permisoEdificacionFecha,type(None)):
        excel_find_replace(wb,'permisoEdificacion',realEstate.permisoEdificacionNo+' del año '+str(realEstate.permisoEdificacionFecha.year))
    else:
        excel_find_replace(wb,'permisoEdificacion',realEstate.permisoEdificacionNo)
    if not isinstance(realEstate.recepcionFinalFecha,type(None)):
        excel_find_replace(wb,'recepcionFinal',realEstate.recepcionFinalNo+' del año '+str(realEstate.recepcionFinalFecha.year))
    else:
        excel_find_replace(wb,'recepcionFinal',realEstate.recepcionFinalNo)

    if realEstate.is_house:
        excel_find_replace(wb,'generalDescription',realEstate.house.generalDescription)
    else:
        excel_find_replace(wb,'generalDescription',realEstate.apartment.generalDescription)

    excel_find_replace(wb,'descripcionSectorAll',appraisal.descripcionSector+'\n'+appraisal.descripcionPlanoRegulador+'\n'+appraisal.descripcionExpropiacion)

    ws = wb.worksheets[0]

    # Find where valuation table starts
    for i, row in enumerate(ws.rows):
        if row[2].value == "propertyAddress":
            ws.insert_rows(i,1)
            break
            #ws.append((cell.value for cell in row[1:100]))

    # Map image
    r = requests.get("https://maps.googleapis.com/maps/api/staticmap?center="+\
    	realEstate.addressStreet+" "+\
    	realEstate.addressNumber+"&zoom=16&size=900x530&maptype=roadmap&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E&markers=color:blue%7Clabel:A%7C"+\
    	str(realEstate.lat)+","+str(realEstate.lng))
    lf = tempfile.NamedTemporaryFile()
    lf.write(r.content)
    img = drawing.image.Image(lf)
    print(img)
    print(wb.worksheets)
    print(wb.worksheets[0])
    img.anchor = "D31"
    wb.worksheets[0].add_image(img)

    response = HttpResponse(
        content=save_virtual_workbook(wb),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="somefilename.xlsx"'

    return response