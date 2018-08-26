from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal

from .forms import AppraisalApartmentForm

import datetime

def get_building(request,id):
    '''
        Given building id, returns the building object.
        It checks for some errors and sends to the error page.
    '''
    building = Building.objects.filter(id=id)
    # This must be only one building
    if len(building) == 0:
        context = {'error_message': 'Building should exist by now'}
        return render(request, 'appraisal/error.html',context)
    elif len(building) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)
    building = building[0]
    return building

def get_apartment(request,id):
    '''
        Given an appartment id, return the apartment object.
        It checks for errors and sends to the correct error page.
    '''
    apartment = Apartment.objects.filter(id=id)
    # This must be only one apartment
    if len(apartment) == 0:
        context = {'error_message': 'Apartment should exist by now'}
        return render(request, 'appraisal/error.html',context)
    elif len(apartment) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)
    apartment = apartment[0]
    return apartment

def get_appraisal(request,id):
    '''
        Given an appraisal id, returns the apraisal object.
        It checks for errors and sends to the correct error page.
    '''
    appraisal = Appraisal.objects.filter(id=id)
    if len(appraisal) == 0:
        context = {'error_message': 'Appraisal not found?'}
        return render(request, 'appraisal/error.html',context)
    appraisal = appraisal[0]
    return appraisal

def form_process(request,form,building,apartment,appraisal):

    def form_do_delete(form):
        print('form_do_delete')
        appraisal.delete()
        context = {}
        return render(request, 'appraisal/deleted.html',context)

    def form_do_save(form):
        print('form_do_save')
        apartment.floor = form.cleaned_data['general_floor']
        apartment.bedrooms = form.cleaned_data['general_bedrooms']
        apartment.bathrooms = form.cleaned_data['general_bathrooms']
        apartment.totalSquareMeters = form.cleaned_data['general_totalSquareMeters']
        apartment.usefulSquareMeters = form.cleaned_data['general_usefulSquareMeters']
        apartment.orientation = form.cleaned_data['general_orientation']
        apartment.generalDescription = form.cleaned_data['general_generalDescription']
        apartment.save()

        appraisal.solicitante = form.cleaned_data['app_solicitante']
        appraisal.solicitanteSucursal = form.cleaned_data['app_solicitanteSucursal']
        appraisal.solicitanteEjecutivo = form.cleaned_data['app_solicitanteEjecutivo']
        appraisal.cliente = form.cleaned_data['app_cliente']
        appraisal.clienteRut = form.cleaned_data['app_clienteRut']
        appraisal.propietario = form.cleaned_data['app_propietario']
        appraisal.propietarioRut = form.cleaned_data['app_propietarioRut']
        appraisal.rolAvaluo = form.cleaned_data['app_rolAvaluo']
        appraisal.tasadorNombre = form.cleaned_data['app_tasadorNombre']
        appraisal.tasadorRut = form.cleaned_data['app_tasadorRut']
        appraisal.visadorEmpresa = form.cleaned_data['app_visadorEmpresa']
        appraisal.visadorEmpresaMail = form.cleaned_data['app_visadorEmpresaMail']
        appraisal.timeModified = datetime.datetime.now()
        appraisal.save()
        return

    if form.is_valid():
        if 'save' in request.POST:
            ret = form_do_save(form)
            '''
            '''
        elif 'delete' in request.POST:
            ret = form_do_delete(form)
        else:
            return

    return ret

def appraisal(request,region="",commune="",street="",number="",id_b=0,
              numbera="",id_a=0,id_appraisal=0):
    '''
    '''
    # Get current building
    building = get_building(request,id_b)
    if isinstance(building,HttpResponse): return building
    # Get current flat
    apartment = get_apartment(request,id_a)
    if isinstance(apartment,HttpResponse): return apartment
    # Get current appraisal
    appraisal = get_appraisal(request,id_appraisal)
    if isinstance(appraisal,HttpResponse): return appraisal

    # DA FORM

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AppraisalApartmentForm(request.POST)
        ret = form_process(request,form,building,apartment,appraisal)
        if isinstance(ret,HttpResponse): return ret

    form = AppraisalApartmentForm(
        initial={
            'general_floor':apartment.floor,
            'general_bedrooms':apartment.bedrooms,
            'general_bathrooms':apartment.bathrooms,
            'general_totalSquareMeters':apartment.totalSquareMeters,
            'general_usefulSquareMeters':apartment.usefulSquareMeters,
            'general_orientation':apartment.orientation,
            'general_generalDescription':apartment.generalDescription,
            'app_solicitante':appraisal.solicitante,
            'app_solicitanteSucursal':appraisal.solicitanteSucursal,
            'app_solicitanteEjecutivo':appraisal.solicitanteEjecutivo,
            'app_cliente':appraisal.cliente,
            'app_clienteRut':appraisal.clienteRut,
            'app_propietario':appraisal.propietario,
            'app_propietarioRut':appraisal.propietarioRut,
            'app_rolAvaluo':appraisal.rolAvaluo,
            'app_tasadorNombre':appraisal.tasadorNombre,
            'app_tasadorRut':appraisal.tasadorRut,
            'app_visadorEmpresa':appraisal.visadorEmpresa,
            'app_visadorEmpresaMail':appraisal.visadorEmpresaMail
        })

    context = {'building': building, 'apartment': apartment, 'form': form}

    return render(request, 'appraisal/apartment.html',context)
