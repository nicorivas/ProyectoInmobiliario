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
from dbase.globals import *

from realestate.models import RealEstate
from house.models import House
#from building.models import Building
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
import zipfile

@login_required(login_url='/user/login')
def view_create(request):

    if request.method == 'POST':
        request_post = request.POST.copy()
        request_post['appraisalTimeRequest'] = datetime.datetime.strptime(request_post['appraisalTimeRequest'],'%d/%m/%Y %H:%M')

        form = AppraisalCreateForm(request_post)
        if form.is_valid():

            propertyType = int(form.cleaned_data['propertyType'])
            realEstate = None
            if propertyType == RealEstate.TYPE_CASA:

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

            elif propertyType == RealEstate.TYPE_EDIFICIO:

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
                        propertyType=RealEstate.TYPE_EDIFICIO)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    realEstate = create.building_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    realEstate = Building.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_EDIFICIO)
                    realEstate = buildings.first()
                    #context = {'error_message': 'Building is repeated'}
                    #return render(request, 'create/error.html',context)

            elif propertyType == RealEstate.TYPE_CONDOMINIO:

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
                        propertyType=RealEstate.TYPE_CONDOMINIO)
                except RealEstate.DoesNotExist:
                    realEstate = create.real_estate_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    realEstate = RealEstate.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_CONDOMINIO)
                    realEstate = realEstate.first()

            elif propertyType == RealEstate.TYPE_DEPARTAMENTO:

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
                        propertyType=RealEstate.TYPE_EDIFICIO)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = create.building_create(request,addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    buildings = Building.objects.filter(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_EDIFICIO)
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
                        propertyType=RealEstate.TYPE_DEPARTAMENTO)
                except Apartment.DoesNotExist:
                    # flat does not exist, so create it
                    realEstate = create.apartment_create(request,building,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Apartment is repeated'}
                    return render(request, 'create/error.html',context)

            elif propertyType == RealEstate.TYPE_OTRO:

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
            if propertyType == RealEstate.TYPE_CONDOMINIO:
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

def parseAddress(address,commune=None):
    addressNumber2 = None
    addressNumber = None

    address = address.lower().strip()

    if commune:
        if address.endswith(commune):
            address = address[:address.find(commune)].strip()

    dpto_strings = ["dpto.","dpto","depto.","depto","departamento"]
    for dpto_string in dpto_strings:
        if dpto_string in address:
            match = re.search(dpto_string+' ?(\d+)', address)
            if match:
                addressNumber2 = match.group(1)
                address = address[:address.index(dpto_string)]
                break

    casa_strings = ["casa.","casa"]
    for casa_string in casa_strings:
        if casa_string in address:
            match = re.search(casa_string+' ?[a-zA-Z0-9]', address)
            if match:
                addressNumber2 = match.group(0).title()
                address = address[:address.index(casa_string)]
                break

    address = address.strip()
    if address[-1] == ',' or address[-1] == '.' or address[-1] == '-':
        address = address[:-1].strip()
    match = re.search('(\d+)$', address) 
    if match:
        addressNumber = match.group(0)
        address = address[:address.index(addressNumber)]
    address = address.strip()
    address.replace('avenida','av.')
    address.replace('aven','av.')
    address.replace('avnda','av.')

    addressStreet = address

    no_strings = ["no.","nº"]
    for no_string in no_strings:
        if address.endswith(no_string):
            addressStreet = address[:address.find(no_string)]

    if addressStreet.startswith('calle'):
        addressStreet = addressStreet[5:].strip()

    addressStreet = addressStreet.title()

    return [addressStreet,addressNumber,addressNumber2]

def parseRut(rut):
    rut = rut.replace('.','').replace(',','').replace('-','').lower()
    return rut[:-1]+'-'+rut[-1]

def parseCommune(string):
    commune = string.strip().title()
    if '(' in commune:
        commune = commune[:commune.index('(')].strip()
    commune = COMMUNE_NAME_ASCII__UTF[commune]
    commune = Commune.objects.get(name=commune)
    region = commune.region.code
    commune = commune.id
    return [commune, region]

def populate_from_file(request):

    data = {}

    if 'archivo' not in request.FILES.keys():
        data['error'] = 'Debe elegir un archivo antes de importar.'
        return JsonResponse(data)

    file = request.FILES['archivo']
    filetype = file._name.split('.')[1]

    if filetype == 'xls':
        data['error'] = "No es posible importar archivos excel '.xls'. Se recomienda guardar el archivo en formato '.xlsx'."
        return JsonResponse(data)

    if filetype == 'xlsx':
        try:
            wb = load_workbook(filename=file,read_only=True,data_only=True)
        except zipfile.BadZipFile:
            data['error'] = "Archivo parece estar asegurado. Se recomienda abrir y volver a guardar el archivo."
            return JsonResponse(data)            
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

            tipoTasacion = ws['G9'].value
            if tipoTasacion:
                tipoTasacion = tipoTasacion.strip()
                if tipoTasacion == 'CRÉDITO HIPOTECARIO':
                    data['tipoTasacion'] = Appraisal.HIPOTECARIA
                    data['finalidad'] = Appraisal.CREDITO
                if tipoTasacion == 'CRÉDITO COMERCIAL':
                    data['tipoTasacion'] = Appraisal.COMERCIAL
                    data['finalidad'] = Appraisal.CREDITO

            finalidad = ws['J9'].value
            if finalidad:
                finalidad = finalidad.strip()
                if finalidad == 'ACTUALIZAR GARANTÍA':
                    data['finalidad'] = Appraisal.GARANTIA
                elif finalidad == 'COMPRA INMUEBLE':
                    data['finalidad'] = Appraisal.CREDITO
                elif finalidad == 'LIQUIDACIÓN FORZADA':
                    data['finalidad'] = Appraisal.LIQUIDACION
                elif finalidad == 'DACIÓN EN PAGO':
                    data['finalidad'] = Appraisal.DACION_EN_PAGO

            appraisalTimeRequest = ws['M3'].value
            if isinstance(appraisalTimeRequest,type('')):
                if appraisalTimeRequest != '':
                    if appraisalTimeRequest.endswith(',') or appraisalTimeRequest.endswith('.'):
                        appraisalTimeRequest = appraisalTimeRequest[:-1]
                    if '-' in appraisalTimeRequest:
                        data['appraisalTimeRequest'] = appraisalTimeRequest.strip().replace('-','/')+' 00:00'
                    elif '.' in appraisalTimeRequest:
                        data['appraisalTimeRequest'] = appraisalTimeRequest.strip().replace('.','/')+' 00:00'
                    elif '/' in appraisalTimeRequest:
                        data['appraisalTimeRequest'] = appraisalTimeRequest.strip()+' 00:00'
                    else:
                        pass
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

            if '-' in ws['C16'].value:
                data['clienteRut'] = parseRut(ws['C16'].value)
            else:
                data['clienteRut'] = parseRut(ws['C16'].value+ws['F16'].value)
            
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
                data['propertyType'] = RealEstate.TYPE_CASA
            elif tipo == 'DEPARTAMENTOS':
                data['propertyType'] = RealEstate.TYPE_DEPARTAMENTO
            elif tipo == 'OFICINAS':
                data['propertyType'] = RealEstate.TYPE_OFICINA
            elif tipo == 'TERRENO PROYECTO INMOBILIARIO':
                data['propertyType'] = RealEstate.TYPE_TERRENO
            elif tipo == 'SITIOS Y TERRENOS URBANOS':
                data['propertyType'] = RealEstate.TYPE_TERRENO
            elif tipo == 'LOCALES COMERCIALES':
                data['propertyType'] = RealEstate.TYPE_LOCAL_COMERCIAL
            elif tipo == 'CONSTRUCCIONES INDUSTRIALES':
                data['propertyType'] = RealEstate.TYPE_INDUSTRIA
            elif 'BODEGAS' in tipo:
                data['propertyType'] = RealEstate.TYPE_BODEGA
            elif 'ESTACIONAMIENTOS' in tipo:
                data['propertyType'] = RealEstate.TYPE_ESTACIONAMIENTO
            elif 'BIENES RAICES RURALES' in tipo:
                data['propertyType'] = RealEstate.TYPE_PARCELA
            else:
                data['propertyType'] = RealEstate.TYPE_OTRO

            try :
                commune, region = parseCommune(ws['C45'].value)
                data['addressCommune'] = commune
                data['addressRegion'] = region
            except Commune.DoesNotExist:
                pass

            addressStreet = ws['C41'].value
            if isinstance(addressStreet,type('')):
                if addressStreet != '':
                    addressStreet, addressNumber, addressNumber2 = parseAddress(addressStreet,
                        commune=Commune.objects.get(id=data.get('addressCommune')).name.lower())
                    data['addressStreet'] = addressStreet
                    if addressNumber:
                        data['addressNumber'] = addressNumber
                    if addressNumber2:
                        data['addressNumber2'] = addressNumber2

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

            solicitanteEjecutivoRut = ws['M61'].value+ws['N61'].value
            if isinstance(solicitanteEjecutivoRut,type('')):
                if solicitanteEjecutivoRut != '':
                    data['solicitanteEjecutivoRut'] = parseRut(solicitanteEjecutivoRut)

            cliente = ws['H9'].value
            if isinstance(cliente,type('')):
                if cliente != '':
                    data['cliente'] = cliente.strip().title()

            clienteRut = ws['H10'].value
            clienteRutDF = ws['J10'].value
            if clienteRut != '' and clienteRutDF != '':
                data['clienteRut'] = parseRut(str(clienteRut)+''+clienteRutDF)

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
                    data['propertyType'] = RealEstate.TYPE_CASA
                elif tipo == 'DEPARTAMENTO':
                    data['propertyType'] = RealEstate.TYPE_DEPARTAMENTO
                else:
                    data['propertyType'] = RealEstate.TYPE_OTRO

            address = ws['K17'].value
            if isinstance(address,type('')):
                if address != '':
                    addressStreet, addressNumber, addressNumber2 = parseAddress(address)
                    data['addressStreet'] = addressStreet
                    if addressNumber:
                        data['addressNumber'] = addressNumber
                    if addressNumber2:
                        data['addressNumber2'] = addressNumber2

            try :
                commune = ws['M17'].value
                if commune == 'EST. CENTRAL':
                    commune = "Estación Central"
                commune = Commune.objects.get(name=commune.strip().title())
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
                print(line)
                if 'ID' in line.strip():
                    data['solicitanteCodigo'] = text[i+6].strip()
                if 'TIPO OPERACION' in line.strip():
                    if text[i+6].strip() == "Crédito Hipotecario":
                        data['tipoTasacion'] = Appraisal.HIPOTECARIA
                        data['finalidad'] = Appraisal.CREDITO
                if 'TIPO DE BIEN' in line.strip():
                    if text[i+6].strip() == "DEPARTAMENTO":
                        data['propertyType'] = RealEstate.TYPE_DEPARTAMENTO
                    if text[i+6].strip() == "CASA":
                        data['propertyType'] = RealEstate.TYPE_CASA
                if 'COMUNA' in line.strip():
                    comuna = text[i+6].strip().title()
                    commune = Commune.objects.get(name=comuna)
                    data['addressCommune'] = commune.id
                    data['addressRegion'] = commune.region.code
                if 'ROL' in line.strip():
                    data['rol'] = text[i+6+c-1].strip()
                if 'DIRECCION' in line.strip():
                    address = ''
                    c = 0
                    while not 'De propiedad de' in text[i+6+c+1].strip():
                        address += text[i+6+c].strip().title()
                        c += 1
                    addressStreet, addressNumber, addressNumber2 = parseAddress(address)
                    data['addressStreet'] = addressStreet
                    if addressNumber:
                        data['addressNumber'] = addressNumber
                    if addressNumber2:
                        data['addressNumber2'] = addressNumber2
                if 'Cliente' in line.strip():
                    data['cliente'] = text[i+2].strip().title()
                if 'Rut' == line.strip():
                    data['clienteRut'] = parseRut(text[i+2])
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
                print(line)
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
                    data['clienteRut'] = parseRut(line.split(':')[1])
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
                    data['propietarioRut'] = parseRut(line.split(':')[1])
                elif 'Nombre Contacto' in line.strip():
                    data['contacto'] = line.split(':')[1].strip().title()
                elif 'Telefono movil' in line.strip():
                    data['contactoTelefono'] = text[i+1].split(':')[1].strip().replace(' ','')
                elif 'Direccion' in line.strip():
                    address = line.split(':')[1].strip()
                    addressStreet, addressNumber, addressNumber2 = parseAddress(address)
                    data['addressStreet'] = addressStreet
                    if addressNumber:
                        data['addressNumber'] = addressNumber
                    if addressNumber2:
                        data['addressNumber2'] = addressNumber2
                elif 'Rubro :' in line.strip():
                    tipoTasacion = line.split(':')[1].strip()
                    if tipoTasacion == "HIPOTECARIO":
                        data['tipoTasacion'] = Appraisal.HIPOTECARIA
                        data['finalidad'] = Appraisal.CREDITO
                    elif tipoTasacion == "GARANTIAS GENERALES":
                        data['finalidad'] = Appraisal.GARANTIA
                elif 'Grupo :' in line.strip():
                    propertyType = line.split(':')[1].strip()
                    if 'DEPARTAMENTO' in propertyType:
                        data['propertyType'] = RealEstate.TYPE_DEPARTAMENTO
                    elif 'VIVIENDA' in propertyType:
                        data['propertyType'] = RealEstate.TYPE_CASA
                    elif 'TERRENO' in propertyType:
                        data['propertyType'] = RealEstate.TYPE_TERRENO
                    elif 'LOCAL COMERCIAL' in propertyType:
                        data['propertyType'] = RealEstate.TYPE_LOCAL_COMERCIAL
                        data['tipoTasacion'] = Appraisal.COMERCIAL
                    elif 'AVANCE' in propertyType:
                        data['tipoTasacion'] = Appraisal.AVANCE_DE_OBRA
                elif 'Rol :' in line.strip():
                    data['rol'] = line.split(':')[1].strip()
                elif 'Comuna' in line.strip():
                    commune = line.split(':')[1].strip().title()
                    commune, region = parseCommune(commune)
                    data['addressCommune'] = commune
                    data['addressRegion'] = region
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
                elif 'Centro de Costo' in line.strip():
                    c = 1
                    data['comments'] = ''
                    while not 'Página 1 de 2' in text[i+c].strip():
                        if len(text[i+c]) > 1 and text[i+c].strip()[1:-1] not in data['comments']:
                            data['comments'] += text[i+c].strip()
                        c += 1


    return JsonResponse(data)
