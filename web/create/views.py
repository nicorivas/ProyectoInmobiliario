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

                context = {'error_message': 'Cannot create buildings yet'}
                return render(request, 'create/error.html',context)

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
                    print(building)
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

            if request.FILES:
                orderFile = request.FILES['archivo']
            else:
                orderFile = None
            
            # ToDO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
            appraisal = create.appraisal_create(request,realEstate.realestate_ptr,
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

def populate_from_file(request):

    data = {}
    file = request.FILES['archivo']
    if file._name.split('.')[1] == 'xlsx':
        wb = load_workbook(filename=file,read_only=True)
        ws = wb.worksheets[0]
        if ws['C1'].value.strip() == 'SOLICITUD DE TASACIÓN':
            # ITAU
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Itaú':
                    data['solicitante'] = c[0]

            solicitanteEjecutivo = ws['C7'].value
            if isinstance(solicitanteEjecutivo,type('')):
                if solicitanteEjecutivo != '':
                    data['solicitanteEjecutivo'] = ws['C7'].value.strip()

            solicitanteSucursal = ws['C9'].value
            if isinstance(solicitanteSucursal,type('')):
                if solicitanteSucursal != '':
                    data['solicitanteSucursal'] = ws['C9'].value.strip()

            solicitanteEjecutivoEmail = ws['J7'].value
            if isinstance(solicitanteEjecutivoEmail,type('')):
                if solicitanteEjecutivoEmail != '':
                    data['solicitanteEjecutivoEmail'] = ws['J7'].value.strip()

            solicitanteEjecutivoTelefono = ws['O7'].value
            if isinstance(solicitanteEjecutivoTelefono,type('')):
                if solicitanteEjecutivoTelefono != '':
                    data['solicitanteEjecutivoTelefono'] = ws['O7'].value.strip().replace(' ','')

            tipoTasacion = ws['G9'].value.strip()
            if tipoTasacion == 'CRÉDITO HIPOTECARIO':
                data['tipoTasacion'] = Appraisal.INMOBILIARIA
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
                        print(a)
                    except ValueError:
                        try:
                            a = datetime.datetime.strptime(data['appraisalTimeRequest'],'%d/%m/%y %H:%M')
                            data['appraisalTimeRequest'] = data['appraisalTimeRequest'][0:6]+'20'+data['appraisalTimeRequest'][6:]
                        except ValueError:
                            data['appraisalTimeRequest'] = ''

            cliente = ws['C14'].value
            if isinstance(cliente,type('')):
                if cliente != '':
                    data['cliente'] = ws['C14'].value.strip()

            clienteRut = ws['C16'].value
            clienteRutDF = ws['F16'].value
            if isinstance(clienteRut,type('')) and isinstance(clienteRutDF,type('')):
                if clienteRut != '' and clienteRutDF != '':
                    data['clienteRut'] = ws['C16'].value.strip()+''+ws['F16'].value.strip().lower()
            
            clienteEmail = ws['C22'].value
            if isinstance(clienteEmail,type('')):
                if clienteEmail != '':
                    data['clienteEmail'] = ws['C22'].value.strip()
            
            clienteTelefono = ws['C24'].value
            if isinstance(clienteTelefono,type('')):
                if clienteTelefono != '':
                    data['clienteTelefono'] = ws['C24'].value.strip().replace(' ','')
            
            contacto = ws['C26'].value
            if isinstance(contacto,type('')):
                if contacto != '':
                    data['contacto'] = ws['C26'].value.strip()

            contactoEmail = ws['C28'].value
            if isinstance(contactoEmail,type('')):
                if contactoEmail != '':
                    data['contactoEmail'] = ws['C28'].value.strip()

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

    elif file._name.split('.')[1] == 'pdf':
        # Santander o Chile
        file = file.read()
        doc = fitz.open(filetype="pdf",stream=file)
        page = doc.loadPage(0)
        text = page.getText("text").splitlines()

        if 'Solicito a usted' in text[0]:
            # Banco de Chile
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Banco de Chile':
                    data['solicitante'] = c[0]
            for i, line in enumerate(text):
                print(line)
                if 'ID' in line.strip():
                    data['solicitanteCodigo'] = text[i+6].strip()
                if 'TIPO OPERACION' in line.strip():
                    if text[i+6].strip() == "Crédito Hipotecario":
                        data['tipoTasacion'] = Appraisal.INMOBILIARIA
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
                    data['clienteRut'] = text[i+2].strip()
                if 'Nombre' == line.strip():
                    data['solicitanteEjecutivo'] = text[i+2].strip()
                if 'Teléfono' == line.strip():
                    data['solicitanteEjecutivoTelefono'] = text[i+2].strip()
                if 'E - Mail' == line.strip():
                    data['solicitanteEjecutivoEmail'] = text[i+2].strip()
                if 'Unidad' in line.strip():
                    data['solicitanteSucursal'] = text[i+2].strip().title()
                if 'Información de Contacto' in line.strip():
                    c = text[i+1].split('/')
                    data['contacto'] = c[0]
                    data['contactoTelefono'] = c[1].split(':')[1].strip().replace(' ','')
                    data['appraisalTimeRequest'] = text[i+2]+' '+text[i+3]
                
        else:
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Santander':
                    data['solicitante'] = c[0]
            for i, line in enumerate(text):
                if 'Req' in line.strip():
                    data['solicitanteCodigo'] = line.split(':')[1].strip()
                elif 'Fecha de asignación' in line.strip():
                    data['appraisalTimeRequest'] = text[i+5].strip()
                elif 'Entregar informe de' in line.strip():
                    data['appraisalTimeDue'] = text[i+5].strip()
                elif 'Nombre Cliente' in line.strip():
                    data['cliente'] = line.split(':')[1].strip()
                elif 'RUT Cliente' in line.strip():
                    data['clienteRut'] = line.split(':')[1].strip()
                elif 'Nombre Propietario' in line.strip():
                    data['propietario'] = line.split(':')[1].strip()
                    c = 1
                    while not 'RUT Propietario' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['propietario'] += ' '+text[i+c].strip()
                        c += 1
                elif 'RUT Propietario' in line.strip():
                    data['propietarioRut'] = line.split(':')[1].strip()
                elif 'Nombre Contacto' in line.strip():
                    data['contacto'] = line.split(':')[1].strip()
                elif 'Telefono movil' in line.strip():
                    data['contactoTelefono'] = text[i+1].split(':')[1].strip()
                elif 'Direccion' in line.strip():
                    address = line.split(':')[1].strip()
                    data['addressStreet'] = address
                elif 'Comuna' in line.strip():
                    comuna = line.split(':')[1].strip().title()
                    comuna = comuna.split('(')[0].strip()
                    commune = Commune.objects.get(name=comuna)
                    data['addressCommune'] = commune.id
                    data['addressRegion'] = commune.region.code
                elif 'Nombre Ejecutivo' in line.strip():
                    data['solicitanteEjecutivo'] = line.split(':')[1].strip()
                    c = 1
                    while not 'E-Mail Ejecutivo' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['solicitanteEjecutivo'] += ' '+text[i+c].strip()
                        c += 1
                elif 'Telefono Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoTelefono'] = line.split(':')[1].strip()
                elif 'E-Mail Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoEmail'] = line.split(':')[1].strip()
                elif 'Sucursal' in line.strip():
                    data['solicitanteSucursal'] = line.split(':')[1].strip()

    return JsonResponse(data)
