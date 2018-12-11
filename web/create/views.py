from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from .forms import AppraisalCreateForm

from region.models import Region
from commune.models import Commune

from realestate.models import RealEstate
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal
from . import create

from openpyxl import drawing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import load_workbook

import datetime

import requests # to call the API of Google to get lat-lon
import reversion # to save the first version when creating an appraisal
from io import BytesIO

import fitz
import re

@login_required(login_url='/user/login')
def view_create(request):

    if request.method == 'POST':
        request_post = request.POST.copy()
        request_post['appraisalTimeRequest'] = datetime.datetime.strptime(request_post['appraisalTimeRequest'],'%d/%m/%Y %H:%M')

        form = AppraisalCreateForm(request_post)
        if form.is_valid():

            propertyType = int(form.cleaned_data['propertyType'])
            realEstate = None
            if propertyType == RealEstate.TYPE_HOUSE:

                addressRegion = form.cleaned_data['addressRegion']
                addressCommune = form.cleaned_data['addressCommune']
                addressStreet = form.cleaned_data['addressStreet']
                addressNumber = form.cleaned_data['addressNumber']
                addressNumber2 = form.cleaned_data['addressNumber2']

                try:
                    # get house if it exists
                    realEstate = House.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        addressNumber2=addressNumber2)
                except House.DoesNotExist:
                    # house does not exist, so create it
                    realEstate = create.house_create(request,addressRegion,addressCommune,addressStreet,addressNumber,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'House is repeated'}
                    return render(request, 'create/error.html', context)

            elif propertyType == RealEstate.TYPE_BUILDING:

                addressRegion = form.cleaned_data['addressRegion']
                addressCommune = form.cleaned_data['addressCommune']
                addressStreet = form.cleaned_data['addressStreet']
                addressNumber = form.cleaned_data['addressNumber']
                addressNumber2 = form.cleaned_data['addressNumber2']

                # check if building exists
                try:
                    realEstate = Building.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_BUILDING)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    realEstate = create.building_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    realEstate = Building.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_BUILDING)
                    realEstate = buildings.first()
                    #context = {'error_message': 'Building is repeated'}
                    #return render(request, 'create/error.html',context)

            elif propertyType == RealEstate.TYPE_CONDOMINIUM:

                addressRegion = form.cleaned_data['addressRegion']
                addressCommune = form.cleaned_data['addressCommune']
                addressStreet = form.cleaned_data['addressStreet']
                addressNumber = form.cleaned_data['addressNumber']
                addressNumber2 = form.cleaned_data['addressNumber2']

                try:
                    realEstate = RealEstate.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_CONDOMINIUM)
                except RealEstate.DoesNotExist:
                    realEstate = create.real_estate_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    realEstate = RealEstate.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_CONDOMINIUM)
                    realEstate = realEstate.first()

            elif propertyType == RealEstate.TYPE_APARTMENT:

                addressRegion = form.cleaned_data['addressRegion']
                addressCommune = form.cleaned_data['addressCommune']
                addressStreet = form.cleaned_data['addressStreet']
                addressNumber = form.cleaned_data['addressNumber']
                addressNumber2 = form.cleaned_data['addressNumber2']

                # check if building exists
                building = None
                try:
                    building = Building.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_BUILDING)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = create.building_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    buildings = Building.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_BUILDING)
                    building = buildings.first()
                    #context = {'error_message': 'Building is repeated'}
                    #return render(request, 'create/error.html',context)

                # check if flat exists
                realEstate = None
                try:
                    realEstate = Apartment.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        addressNumber2=addressNumber2,
                        propertyType=RealEstate.TYPE_APARTMENT)
                except Apartment.DoesNotExist:
                    # flat does not exist, so create it
                    realEstate = create.apartment_create(request,building,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Apartment is repeated'}
                    return render(request, 'create/error.html',context)

            elif propertyType == RealEstate.TYPE_OTHER:

                pass

            else:

                context = {'error_message': 'Tipo de propiedad no ha sido implementado'}
                return render(request, 'create/error.html',context)


            # create new appraisal
            #appraisalPrice = form.cleaned_data['appraisalPrice']
            price = None

            solicitante = form.cleaned_data['solicitante']
            if solicitante == "0":
                solicitanteOtro = form.cleaned_data['solicitanteOther']
            else:
                solicitanteOtro = None
            solicitanteSucursal = form.cleaned_data['solicitanteSucursal']
            solicitanteCodigo = form.cleaned_data['solicitanteCodigo']
            solicitanteEjecutivo = form.cleaned_data['solicitanteEjecutivo']
            solicitanteEjecutivoEmail = form.cleaned_data['solicitanteEjecutivoEmail']
            solicitanteEjecutivoTelefono = form.cleaned_data['solicitanteEjecutivoTelefono']

            appraisalTimeDue = form.cleaned_data['appraisalTimeDue']
            appraisalTimeRequest = form.cleaned_data['appraisalTimeRequest']

            rol = form.cleaned_data['rol']

            tipoTasacion = form.cleaned_data['tipoTasacion']
            finalidad = form.cleaned_data['finalidad']
            visita = form.cleaned_data['visita']

            cliente = form.cleaned_data['cliente']
            clienteRut = form.cleaned_data['clienteRut']
            clienteEmail = form.cleaned_data['clienteEmail']
            clienteTelefono = form.cleaned_data['clienteTelefono']

            contacto = form.cleaned_data['contacto']
            contactoEmail = form.cleaned_data['contactoEmail']
            contactoTelefono = form.cleaned_data['contactoTelefono']

            commentsOrder = form.cleaned_data['comments']

            if request.FILES:
                orderFile = request.FILES['archivo']
            else:
                orderFile = None

            if realEstate == None:
                rsptr = None
            if propertyType == RealEstate.TYPE_CONDOMINIUM:
                rsptr = realEstate
            else:
                rsptr = realEstate.realestate_ptr
            
            # ToDO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
            appraisal = create.appraisal_create(request,rsptr,
                solicitante=solicitante,
                solicitanteOtro=solicitanteOtro,
                solicitanteSucursal=solicitanteSucursal,
                solicitanteCodigo=solicitanteCodigo,
                solicitanteEjecutivo=solicitanteEjecutivo,
                solicitanteEjecutivoEmail=solicitanteEjecutivoEmail,
                solicitanteEjecutivoTelefono=solicitanteEjecutivoTelefono,
                timeDue=appraisalTimeDue,
                timeRequest=appraisalTimeRequest,
                rol=rol,
                tipoTasacion=tipoTasacion,
                finalidad=finalidad,
                visita=visita,
                cliente=cliente,
                clienteRut=clienteRut,
                clienteEmail=clienteEmail,
                clienteTelefono=clienteTelefono,
                contacto=contacto,
                contactoEmail=contactoEmail,
                contactoTelefono=contactoTelefono,
                price=price,
                commentsOrder=commentsOrder,
                orderFile=orderFile,
                user=request.user)

            # go to appraisal url
            return HttpResponseRedirect(appraisal.url)
        else:
            errordata = form.errors.as_data()
            print(errordata)
            message = {'error_message':'Validation Error, for now is price appraisal'}
            context = {'form': form, 'message': message}
            if '__all__' in errordata.keys():
                message = errordata['__all__'][0].message
            else:
                message = ""
            context = {'form':form,'message':message}            
            return render(request, 'create/error.html', context)

    else:

        # Sort communes
        communes = Commune.objects.only('name').order_by('name')
        regions = Region.objects.only('name').order_by('code')

        # Set initial values
        form = AppraisalCreateForm(label_suffix='')
        form.fields['addressRegion'].queryset = regions
        form.fields['addressCommune'].queryset = communes

        context = {'form': form}

        return render(request, 'create/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})

def parse_email(string):
    if '<' in string:
        iii = string.index('<')+1
        iif = string.index('>')
        return string[iii:iif].strip().lower()
    else:
        return string.strip().lower()

def populate_from_file(request):

    data = {}

    if 'archivo' not in request.FILES.keys():
        data['error'] = 'Debe elegir un archivo antes de importar.'
        return JsonResponse(data)

    file = request.FILES['archivo']
    filetype = file._name.split('.')[1]

    if filetype == 'xls':
        data['error'] = "No es posible importar de archivo excel 'xls'. Se recomienda guardar el excel en el formato 'xlsx'."
        return JsonResponse(data)

    if filetype == 'xlsx':
        wb = load_workbook(filename=file,read_only=True,data_only=True)
        ws = wb.worksheets[0]
        if ws['C1'].value != None and 'SOLICITUD DE TASACIÓN' in ws['C1'].value:
            # ----
            # ITAU
            # ----
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Itaú':
                    data['solicitante'] = c[0]

            solicitanteEjecutivo = ws['C7'].value
            if isinstance(solicitanteEjecutivo,type('')):
                if solicitanteEjecutivo != '':
                    data['solicitanteEjecutivo'] = ws['C7'].value.strip().title()

            solicitanteSucursal = ws['C9'].value
            if isinstance(solicitanteSucursal,type('')):
                if solicitanteSucursal != '':
                    data['solicitanteSucursal'] = ws['C9'].value.strip().title()

            solicitanteEjecutivoEmail = ws['J7'].value
            if isinstance(solicitanteEjecutivoEmail,type('')):
                if solicitanteEjecutivoEmail != '':
                    data['solicitanteEjecutivoEmail'] = parse_email(solicitanteEjecutivoEmail)

            solicitanteEjecutivoTelefono = ws['O7'].value
            if isinstance(solicitanteEjecutivoTelefono,type('')):
                if solicitanteEjecutivoTelefono != '':
                    data['solicitanteEjecutivoTelefono'] = ws['O7'].value.strip().replace(' ','')

            tipoTasacion = ws['G9'].value.strip()
            if tipoTasacion == 'CRÉDITO HIPOTECARIO':
                data['tipoTasacion'] = Appraisal.HIPOTECARIA
                data['finalidad'] = Appraisal.CREDITO
            finalidad = ws['G9'].value.strip()
            if finalidad == 'ACTUALIZAR GARANTÍA':
                data['finalidad'] = Appraisal.GARANTIA
            elif finalidad == 'COMPRA INMUEBLE':
                data['finalidad'] = Appraisal.CREDITO
            elif finalidad == 'LIQUIDACIÓN FORZADA':
                data['finalidad'] = Appraisal.LIQUIDACION

            appraisalTimeRequest = ws['M3'].value
            if isinstance(appraisalTimeRequest,type('')):
                if appraisalTimeRequest != '':
                    data['appraisalTimeRequest'] = appraisalTimeRequest.strip().replace('-','/')+' 00:00'
                    try:
                        a = datetime.datetime.strptime(data['appraisalTimeRequest'],'%d/%m/%Y %H:%M')
                    except ValueError:
                        try:
                            a = datetime.datetime.strptime(data['appraisalTimeRequest'],'%d/%m/%y %H:%M')
                            data['appraisalTimeRequest'] = data['appraisalTimeRequest'][0:6]+'20'+data['appraisalTimeRequest'][6:]
                        except ValueError:
                            data['appraisalTimeRequest'] = ''

            cliente = ws['C14'].value
            if isinstance(cliente,type('')):
                if cliente != '':
                    data['cliente'] = ws['C14'].value.strip().title()

            clienteRut = ws['C16'].value
            clienteRutDF = ws['F16'].value
            if isinstance(clienteRut,type('')) and isinstance(clienteRutDF,type('')):
                if clienteRut != '' and clienteRutDF != '':
                    data['clienteRut'] = ws['C16'].value.strip()+''+ws['F16'].value.strip().lower()
            
            clienteEmail = ws['C22'].value
            if isinstance(clienteEmail,type('')):
                if clienteEmail != '':
                    data['clienteEmail'] = parse_email(clienteEmail)
            
            clienteTelefono = ws['C24'].value
            if isinstance(clienteTelefono,type('')):
                if clienteTelefono != '':
                    data['clienteTelefono'] = ws['C24'].value.strip().replace(' ','')
            
            contacto = ws['C26'].value
            if isinstance(contacto,type('')):
                if contacto != '':
                    data['contacto'] = ws['C26'].value.strip().title()

            contactoEmail = ws['C28'].value
            if isinstance(contactoEmail,type('')):
                if contactoEmail != '':
                    data['contactoEmail'] = parse_email(contactoEmail)

            contactoTelefono = ws['C30'].value
            if isinstance(contactoTelefono,type('')):
                if contactoTelefono != '':
                    data['contactoTelefono'] = ws['C30'].value.strip().replace(' ','')

            tipo = ws['C37'].value
            if isinstance(tipo,type('')):
                tipo = tipo.strip()
            if tipo == 'CASAS':
                data['propertyType'] = RealEstate.TYPE_HOUSE
            elif tipo == 'DEPARTAMENTOS':
                data['propertyType'] = RealEstate.TYPE_APARTMENT
            else:
                data['propertyType'] = RealEstate.TYPE_OTHER

            addressStreet = ws['C41'].value
            if isinstance(addressStreet,type('')):
                if addressStreet != '':
                    data['addressStreet'] = ws['C41'].value.strip()
                    try :
                        commune = Commune.objects.get(name=ws['C45'].value.strip().title())
                        data['addressCommune'] = commune.id
                        data['addressRegion'] = commune.region.code
                    except Commune.DoesNotExist:
                        pass

            rol = ws['C43'].value
            if isinstance(rol,type('')):
                if rol != '':
                    data['rol'] = ws['C43'].value.strip()

            comments = ws['B54'].value
            if isinstance(comments,type('')):
                if comments != '':
                    data['comments'] = comments.strip()

        elif 'SOLICITUD DE INFORME' in ws['B5'].value.strip():
            # ---------------------------------
            # Banco de Chile: Informe de avance
            # ---------------------------------
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Banco de Chile':
                    data['solicitante'] = c[0]

            solicitanteEjecutivo = ws['E61'].value
            if isinstance(solicitanteEjecutivo,type('')):
                if solicitanteEjecutivo != '':
                    data['solicitanteEjecutivo'] = solicitanteEjecutivo.strip().title()

            solicitanteSucursal = ws['E62'].value
            if isinstance(solicitanteSucursal,type('')):
                if solicitanteSucursal != '':
                    data['solicitanteSucursal'] = solicitanteSucursal.strip().title()

            solicitanteEjecutivoEmail = ws['E63'].value
            if isinstance(solicitanteEjecutivoEmail,type('')):
                if solicitanteEjecutivoEmail != '':
                    data['solicitanteEjecutivoEmail'] = solicitanteEjecutivoEmail.strip().lower()

            solicitanteEjecutivoTelefono = ws['M62'].value
            if solicitanteEjecutivoTelefono != '':
                data['solicitanteEjecutivoTelefono'] = str(solicitanteEjecutivoTelefono)

            solicitanteEjecutivoRut = ws['M61'].value
            if isinstance(solicitanteEjecutivoRut,type('')):
                if solicitanteEjecutivoRut != '':
                    data['solicitanteEjecutivoRut'] = solicitanteEjecutivoRut.replace(',','')+ws['N61'].value.replace('-','').strip().lower()

            cliente = ws['H9'].value
            if isinstance(cliente,type('')):
                if cliente != '':
                    data['cliente'] = cliente.strip().title()

            clienteRut = ws['H10'].value
            clienteRutDF = ws['J10'].value
            if clienteRut != '' and clienteRutDF != '':
                data['clienteRut'] = str(clienteRut)+''+clienteRutDF

            contacto = ws['E56'].value
            if isinstance(contacto,type('')):
                if contacto != '':
                    data['contacto'] = contacto.strip().title()

            contactoEmail = ws['E58'].value
            if isinstance(contactoEmail,type('')):
                if contactoEmail != '':
                    data['contactoEmail'] = contactoEmail.strip().lower()

            contactoTelefono = ws['M56'].value
            if contactoTelefono != '':
                data['contactoTelefono'] = str(contactoTelefono)

            tipoTasacion = ws['I12'].value.strip()
            if 'ESTADO de AVANCE' in tipoTasacion:
                data['tipoTasacion'] = Appraisal.AVANCE_DE_OBRA
                data['finalidad'] = Appraisal.OTRO
                data['visita'] = Appraisal.COMPLETA


            tipo = ws['H17'].value
            if isinstance(tipo,type('')):
                tipo = tipo.strip()
                if tipo == 'CASA':
                    data['propertyType'] = RealEstate.TYPE_HOUSE
                elif tipo == 'DEPARTAMENTO':
                    data['propertyType'] = RealEstate.TYPE_APARTMENT
                else:
                    data['propertyType'] = RealEstate.TYPE_OTHER

            addressStreet = ws['K17'].value
            if isinstance(addressStreet,type('')):
                if addressStreet != '':
                    data['addressStreet'] = addressStreet.strip()

            try :
                commune = Commune.objects.get(name=ws['M17'].value.strip().title())
                data['addressCommune'] = commune.id
                data['addressRegion'] = commune.region.code
            except Commune.DoesNotExist:
                pass

            data['appraisalTimeRequest'] = ws['N6'].value.strftime('%d/%m/%Y %H:%M')

            ws = wb.worksheets[1]

            data['appraisalTimeDue'] = ws['J41'].value.strftime('%d/%m/%Y %H:%M')

            data['solicitanteCodigo'] = ws['E37'].value

    elif file._name.split('.')[1] == 'pdf':
        # Santander o Chile
        file = file.read()
        doc = fitz.open(filetype="pdf",stream=file)
        page = doc.loadPage(0)
        text = page.getText("text").splitlines()

        if 'Solicito a usted' in text[0]:
            # --------------
            # Banco de Chile
            # --------------
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Banco de Chile':
                    data['solicitante'] = c[0]
            for i, line in enumerate(text):
                if 'ID' in line.strip():
                    data['solicitanteCodigo'] = text[i+6].strip()
                if 'TIPO OPERACION' in line.strip():
                    if text[i+6].strip() == "Crédito Hipotecario":
                        data['tipoTasacion'] = Appraisal.HIPOTECARIA
                        data['finalidad'] = Appraisal.CREDITO
                if 'TIPO DE BIEN' in line.strip():
                    if text[i+6].strip() == "DEPARTAMENTO":
                        data['propertyType'] = RealEstate.TYPE_APARTMENT
                if 'COMUNA' in line.strip():
                    comuna = text[i+6].strip().title()
                    commune = Commune.objects.get(name=comuna)
                    data['addressCommune'] = commune.id
                    data['addressRegion'] = commune.region.code
                if 'DIRECCION' in line.strip():
                    data['addressStreet'] = text[i+6].strip().title()
                if 'Cliente' in line.strip():
                    data['cliente'] = text[i+2].strip().title()
                if 'Rut' == line.strip():
                    data['clienteRut'] = text[i+2].strip().replace('.','').replace('-','').lower()
                if 'Nombre' == line.strip():
                    data['solicitanteEjecutivo'] = text[i+2].strip().title()
                if 'Teléfono' == line.strip():
                    data['solicitanteEjecutivoTelefono'] = text[i+2].strip().replace(' ','')
                if 'E - Mail' == line.strip():
                    data['solicitanteEjecutivoEmail'] = text[i+2].strip().lower()
                if 'Unidad' in line.strip():
                    data['solicitanteSucursal'] = text[i+2].strip().title()
                if 'INFORMACION ADICIONAL' in line.strip():
                    data['comments'] = ''
                    c = 1
                    while not 'Antecedentes' in text[i+c].strip() or 'Información de Contacto' in text[i+c].strip():
                        data['comments'] += text[i+c].strip()
                        c += 1
                if 'Información de Contacto' in line.strip():
                    line = text[i+1]
                    if '@' in text[i+2]:
                        line += text[i+2]
                        data['appraisalTimeRequest'] = text[i+3]+' '+text[i+4]
                    else:
                        data['appraisalTimeRequest'] = text[i+2]+' '+text[i+3]
                    c = line.split('/')
                    data['contacto'] = c[0]
                    for cc in c[1:]:
                        print(cc)
                        if 'Fono' in cc:    
                            data['contactoTelefono'] = cc.split(':')[1].strip().replace(' ','')
                        elif 'E-Mail' in cc:
                            data['contactoEmail'] = cc.split(':')[1].strip()
                
        else:
            # ---------
            # Santander
            # ---------
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Santander':
                    data['solicitante'] = c[0]
            for i, line in enumerate(text):
                print(line.strip())
                print('Nombre Contacto' in line.strip())
                if 'Nº Req' in line.strip():
                    data['solicitanteCodigo'] = line.split(':')[1].strip()
                elif 'Fecha de asignación' in line.strip():
                    data['appraisalTimeRequest'] = text[i+5].strip()
                elif 'Entregar informe de' in line.strip():
                    data['appraisalTimeDue'] = text[i+5].strip()
                elif 'Nombre Cliente' in line.strip():
                    data['cliente'] = line.split(':')[1].strip().title()
                    c = 1
                    while not 'RUT Cliente' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['cliente'] += ' '+text[i+c].strip().title()
                        c += 1
                elif 'RUT Cliente' in line.strip():
                    data['clienteRut'] = line.split(':')[1].strip().replace('-','').replace('.','').lower()
                elif 'Nombre Propietario' in line.strip():
                    data['propietario'] = line.split(':')[1].strip().title()
                    c = 1
                    while not 'RUT Propietario' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['propietario'] += ' '+text[i+c].strip().title()
                        c += 1
                elif 'RUT Propietario' in line.strip():
                    data['propietarioRut'] = line.split(':')[1].strip().replace('-','').replace('.','').lower()
                elif 'Nombre Contacto' in line.strip():
                    data['contacto'] = line.split(':')[1].strip().title()
                elif 'Telefono movil' in line.strip():
                    data['contactoTelefono'] = text[i+1].split(':')[1].strip().replace(' ','')
                elif 'Direccion' in line.strip():
                    address = line.split(':')[1].strip()
                    data['addressStreet'] = address
                    address = address.lower()
                    if 'dpto' in address or 'depto' in address or 'departamento' in address:
                        data['propertyType'] = RealEstate.TYPE_APARTMENT   
                elif 'Rubro :' in line.strip():
                    tipoTasacion = line.split(':')[1].strip()
                    if tipoTasacion == "HIPOTECARIO":
                        data['tipoTasacion'] = Appraisal.HIPOTECARIA
                elif 'Grupo :' in line.strip():
                    propertyType = line.split(':')[1].strip()
                    if propertyType == 'DEPARTAMENTO':
                        data['propertyType'] = RealEstate.TYPE_APARTMENT
                elif 'Rol :' in line.strip():
                    data['rol'] = line.split(':')[1].strip()
                elif 'Comuna' in line.strip():
                    comuna = line.split(':')[1].strip().title()
                    comuna = comuna.split('(')[0].strip()
                    if comuna == "Nunoa":
                        comuna = "Ñuñoa"
                    try:
                        commune = Commune.objects.get(name=comuna)
                        data['addressCommune'] = commune.id
                        data['addressRegion'] = commune.region.code
                    except Commune.DoesNotExist:
                        # In case name was not in standar format, we just don't fill
                        # commune and region.
                        pass
                elif 'Nombre Ejecutivo' in line.strip():
                    data['solicitanteEjecutivo'] = line.split(':')[1].strip().title()
                    c = 1
                    while not 'E-Mail Ejecutivo' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['solicitanteEjecutivo'] += ' '+text[i+c].strip().title()
                        c += 1
                elif 'Telefono Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoTelefono'] = line.split(':')[1].strip().replace(' ','')
                elif 'E-Mail Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoEmail'] = line.split(':')[1].strip()
                elif 'Sucursal' in line.strip():
                    data['solicitanteSucursal'] = line.split(':')[1].strip().title()

    return JsonResponse(data)
