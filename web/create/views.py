from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from .forms import AppraisalCreateForm, AppraisalFileForm

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

import PyPDF2
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
                    realEstate = create.house_create(addressRegion,addressCommune,addressStreet,addressNumber,addressNumber2)
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
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = create.building_create(addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    context = {'error_message': 'Building is repeated'}
                    return render(request, 'create/error.html',context)

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
                    realEstate = create.apartment_create(building,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Apartment is repeated'}
                    return render(request, 'create/error.html',context)

            else:

                context = {'error_message': 'Property type has not been implemented'}
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
            
            # ToDO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
            appraisal = create.appraisal_create(realEstate.realestate_ptr,
                solicitante=solicitante,
                solicitanteOtro=solicitanteOtro,
                solicitanteSucursal=solicitanteSucursal,
                solicitanteCodigo=solicitanteCodigo,
                solicitanteEjecutivo=solicitanteEjecutivo,
                solicitanteEjecutivoEmail=solicitanteEjecutivoEmail,
                solicitanteEjecutivoTelefono=solicitanteEjecutivoTelefono,
                timeDue=appraisalTimeDue,
                timeRequest=appraisalTimeRequest,
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

        form_file = AppraisalFileForm()

        context = {'form': form, 'form_file':form_file}

        return render(request, 'create/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})

def populate_from_file(request):
    form_file = AppraisalFileForm(request.POST,request.FILES)
    if form_file.is_valid():
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
                data['solicitanteEjecutivo'] = ws['C7'].value.strip()
                data['solicitanteSucursal'] = ws['C9'].value.strip()
                data['solicitanteEjecutivoEmail'] = ws['J7'].value.strip()
                data['solicitanteEjecutivoTelefono'] = ws['O7'].value.strip()
                data['appraisalTimeRequest'] = ws['M3'].value.strip().replace('-','/')+' 00:00'
                data['cliente'] = ws['C14'].value.strip()
                data['clienteRut'] = ws['C16'].value.strip()+''+ws['F16'].value.strip()
                data['clienteEmail'] = ws['C22'].value.strip()
                data['clienteTelefono'] = ws['C24'].value.strip()
                data['contacto'] = ws['C26'].value.strip()
                data['contactoEmail'] = ws['C28'].value.strip()
                data['contactoTelefono'] = ws['C30'].value.strip()
                tipo = ws['C37'].value
                if isinstance(tipo,type('')):
                    tipo = tipo.strip()
                if tipo == 'CASAS':
                    data['propertyType'] = RealEstate.TYPE_HOUSE
                elif tipo == 'DEPARTAMENTOS':
                    data['propertyType'] = RealEstate.TYPE_APARTMENT
                else:
                    data['propertyType'] = RealEstate.TYPE_OTHER
                data['addressStreet'] = ws['C41'].value.strip()
                data['commune_data'] = [[a.code,a.name] for a in list(Commune.objects.all().order_by('name').only('name','code'))]
                try :
                    commune = Commune.objects.get(name=ws['C45'].value.strip().title())
                    data['addressCommune'] = commune.code
                    data['addressRegion'] = commune.region.code
                except Commune.DoesNotExist:
                    pass
        elif file._name.split('.')[1] == 'pdf':
            # Santander
            for c in Appraisal.petitioner_choices:
                if c[1] == 'Santander':
                    data['solicitante'] = c[0]
            pdfReader = PyPDF2.PdfFileReader(file)
            pageObj = pdfReader.getPage(0) 
            text = pageObj.extractText().splitlines()
            for i, line in enumerate(text):
                print(line)
                if 'Req' in line.strip():
                    data['solicitanteCodigo'] = text[i+1].strip()
                elif 'Fecha de asignación' in line.strip():
                    data['appraisalTimeRequest'] = text[i+5].strip()
                elif 'Entregar informe de' in line.strip():
                    data['appraisalTimeDue'] = text[i+5].strip()
                elif 'Nombre Cliente' in line.strip():
                    data['cliente'] = text[i+1].strip()
                    c = 2
                    while not 'RUT Cliente' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['cliente'] += ' '+text[i+c]
                        c += 1
                elif 'RUT Cliente' in line.strip():
                    data['clienteRut'] = text[i+1].strip()
                elif 'Nombre Propietario' in line.strip():
                    data['propietario'] = text[i+1].strip()
                elif 'RUT Propietario' in line.strip():
                    data['propietarioRut'] = text[i+1].strip()
                elif 'Nombre Contacto' in line.strip():
                    data['contacto'] = text[i+1].strip()
                elif 'Telefono movil' in line.strip():
                    data['contactoTelefono'] = text[i+2].strip()
                elif 'Direccion' in line.strip():
                    address = text[i+1].strip()
                    n = re.findall('\d+', address)
                    data['addressStreet'] = address.split(n[0])[0].strip()
                    data['addressNumber'] = n[0]
                elif 'Comuna' in line.strip():
                    data['commune_data'] = [[a.code,a.name] for a in list(Commune.objects.all().order_by('name').only('name','code'))]
                    comuna = text[i+1].strip().title()
                    comuna = comuna.split('(')[0].strip()
                    commune = Commune.objects.get(name=comuna)
                    data['addressCommune'] = commune.code
                    data['addressRegion'] = commune.region.code
                elif 'Nombre Ejecutivo' in line.strip():
                    data['solicitanteEjecutivo'] = text[i+1].strip()
                    c = 2
                    while not 'E-Mail Ejecutivo' in text[i+c].strip():
                        if text[i+c].strip() == '':
                            c += 1
                            continue
                        data['solicitanteEjecutivo'] += ' '+text[i+c].strip()
                        c += 1
                elif 'Nombre Ejecutivo' in line.strip():
                    data['solicitanteEjecutivo'] = text[i+1].strip()
                elif 'Telefono Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoTelefono'] = text[i+1].strip()
                elif 'E-Mail Ejecutivo' in line.strip():
                    data['solicitanteEjecutivoEmail'] = text[i+1].strip()
                elif 'Sucursal' in line.strip():
                    data['solicitanteSucursal'] = text[i+1].strip()

    return JsonResponse(data)
