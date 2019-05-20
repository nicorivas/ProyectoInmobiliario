from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from realestate.models import RealEstate, Asset
from house.models import House
from building.models import Building
from terrain.models import Terrain
#from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Photo, Document, Rol
from commune.models import Commune
from user.models import UserProfile
from .related import getSimilarRealEstate

from .related import getSimilarRealEstate

import reversion
from copy import deepcopy
from reversion.models import Version
from appraisal.data import getAppraisalFromRequest, getPropertyFromRequest

import pytz
import os
import csv

from .forms import FormRealEstate
from .forms import FormBuilding
from .forms import FormApartment
from .forms import FormHouse
from .forms import FormApartmentBuilding
from .forms import FormAppraisal
from .forms import FormComment
from .forms import FormPhotos
from .forms import FormDocuments
from .forms import FormAddProperty
from .forms import FormEditProperty
from .forms import FormAddApartment
from .forms import FormAddRol
from .forms import FormCreateRol
from create import create


import viz.maps as maps
import appraisal.related as related
from appraisal.export import *
from dbase.globals import *
from list.html_bits import *

from django.db.models import Avg, StdDev

import json

import datetime
import requests

def getRealEstate(request,id):
    '''
        Given building id, returns the building object.
        It checks for some errors and sends to the error page.
    '''
    try:
        realestate = RealEstate.objects.get(id=id)
        return realestate
    except RealEstate.DoesNotExist:
        context = {'error_message': 'No existe real estate'}
        return render(request, 'appraisal/error.html',context)
    except MultipleObjectsReturned:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)

def getBuilding(request,id):
    '''
        Given building id, returns the building object.
        It checks for some errors and sends to the error page.
    '''
    try:
        building = Building.objects.get(id=id)
        return building
    except Building.DoesNotExist:
        context = {'error_message': 'Building should exist by now'}
        return render(request, 'appraisal/error.html',context)
    except MultipleObjectsReturned:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)

def getHouse(request,id):
    '''
        Given building id, returns the building object.
        It checks for some errors and sends to the error page.
        TODO: Change this to proper try statements
    '''
    try:
        house = House.objects.get(id=id)
        return house
    except House.DoesNotExist:
        context = {'error_message': 'House should exist by now'}
        return render(request, 'appraisal/error.html',context)
    except MultipleObjectsReturned:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)

def getApartment(request,id):
    '''
        Given an appartment id, return the apartment object.
        It checks for errors and sends to the correct error page.
    '''
    try:
        apartment = Apartment.objects.get(id=id)
        return apartment
    except Apartment.DoesNotExist:
        context = {'error_message': 'Apartment should exist by now'}
        return render(request, 'appraisal/error.html',context)
    except MultipleObjectsReturned:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)

def finish(request,forms, appraisal):
    if forms['property'].is_valid() and \
       forms['realestate'].is_valid() and \
       forms['appraisal'].is_valid():
        appraisal.timeFinished = datetime.datetime.now()
        appraisal.state = Appraisal.STATE_FINISHED
        save_appraisal(request,forms,'Finished')
        return True
    else:
        print('errors',forms['property'].errors)
        print('errors',forms['realestate'].errors)
        print('errors',forms['appraisal'].errors)
        return False

def assign_visador(request,forms,appraisal):
    if forms['appraisal'].is_valid():
        appraisal.visadorUser = User.objects.get(pk=request.POST.dict()['visador'])
        save_appraisal(request, forms, 'Changed visador')
        return True

def assign_tasador(request,forms,appraisal):
    if forms['appraisal'].is_valid():
        appraisal.tasadorUser = User.objects.get(pk=request.POST.dict()['tasador'])
        save_appraisal(request, forms, 'Changed tasador')
        return True

def upload_document(request,forms,appraisal):
    if forms['documents'].is_valid() and forms['appraisal'].is_valid():
        for document_file in request.FILES.getlist('documents'):
            document = Document()
            document.document = document_file
            document.description = forms['documents'].cleaned_data['description']
            document.save()
            appraisal.documents.add(document)
        save_appraisal(request, forms, 'Added document(s)')

def delete_document(request,forms,appraisal):
    appraisal.documents.remove(request.POST['btn_delete_document'])
    if forms['appraisal'].is_valid():
        save_appraisal(request, forms, 'Removed document(s)')

def save_document(request,forms,appraisal):
    try:
        document_id = request.POST['btn_save_document']
        document = Document.objects.get(id=document_id)
        document.description = request.POST['document_description_'+str(document_id)]
        document.save()
        save_appraisal(request, forms, 'Chaged document description')
    except Document.DoesNotExist:
        return

def float_es(string):
    string = string.replace('.','')
    string = string.replace(',','.')
    try:
        return float(string)
    except ValueError:
        return ""

def getAppraisedProperties(appraisal):
    """
    Generate data structure used in templates
    """

    app_properties = {}
    for appprop in appraisal.appproperty_set.all():
        prop = appprop.get_property()
        try:
            real_estate = prop.building.real_estate
        except AttributeError:
            real_estate = prop.real_estate
        
        if real_estate not in app_properties.keys():
            app_properties[real_estate] = {}

        if appprop.property_class not in app_properties[real_estate].keys():
            app_properties[real_estate][appprop.property_class] = {}

        if appprop.property_class_object not in app_properties[real_estate][appprop.property_class].keys():
            app_properties[real_estate][appprop.property_class][appprop.property_class_object] = {}

        app_properties[real_estate][appprop.property_class][appprop.property_class_object]['properties'] = []
        app_properties[real_estate][appprop.property_class][appprop.property_class_object]['properties'].append({
            'appprop':appprop,
            'property_type':appprop.property_type,
            'property_id':prop.id,
            'class':appprop.get_building(),
            'property':prop
        })

        if appprop.property_type == Building.TYPE_DEPARTAMENTO:
            if 'apartments' not in app_properties[real_estate][appprop.property_class][appprop.property_class_object]:
                app_properties[real_estate][appprop.property_class][appprop.property_class_object]['apartments'] = []
            app_properties[real_estate][appprop.property_class][appprop.property_class_object]['apartments'].append(prop)

    return app_properties

def getAppraisedPropertyIds(appraisal):
    app_ids = {}
    for appprop in appraisal.appproperty_set.all():
        if appprop.property_type not in app_ids.keys():
            app_ids[appprop.property_type] = []
        app_ids[appprop.property_type].append(appprop.property_id)
    return app_ids

def view_appraisal(request, **kwargs):
    '''
    General view for appraisals. Gets a variable number of parameters depending
    on the type of realestate.
    '''

    try:
        appraisal = Appraisal.objects.prefetch_related('roles','documents','photos','real_estates','real_estates__buildings','real_estates__addressCommune','real_estates__addressRegion','real_estates__terrains','real_estates__neighborhood').get(pk=int(kwargs['appraisal_id'])) 
    except Appraisal.DoesNotExist:
        context = {'error_message': 'Appraisal not found?'}
        return render(request, 'appraisal/error.html', context)
    except MultipleObjectsReturned:
        context = {'error_message': 'More than one appraisal with the same ID?!'}
        return render(request, 'appraisal/error.html', context)

    
    # Reference real estate
    references = []

    '''
    refRealEstate = related.getSimilarRealEstate(realestate)
    for obj in refRealEstate:
        references.append({'realestate':obj})

    if realestate.propertyType == RealEstate.TYPE_APARTMENT:    
        valRealEstate = [x.apartment for x in appraisal.valuationRealEstate.all()]
        for ref in references:
            if ref['realestate'] in valRealEstate:
                ref['included_in_valuation'] = 1
            else:
                ref['included_in_valuation'] = 0
    else:
        valRealEstate = [x.house for x in appraisal.valuationRealEstate.all()]
        for ref in references:
            if ref['realestate'] in valRealEstate:
                ref['included_in_valuation'] = 1
            else:
                ref['included_in_valuation'] = 0
    '''

    '''
    plot_map = {}
    # Map of references
    if len(references) > 0:
        plot_map = maps.mapReferences(refRealEstate,realestate)
    '''
    
    # Derived properties from references
    '''
    averages = []
    stds = []
    if len(references) > 0:
        if realestate.propertyType == RealEstate.TYPE_DEPARTAMENTO:
            averages = refRealEstate.aggregate(
                Avg('marketPrice'),
                Avg('usefulSquareMeters'),
                Avg('terraceSquareMeters'))
            stds = refRealEstate.aggregate(
                StdDev('marketPrice'),
                StdDev('usefulSquareMeters'),
                StdDev('terraceSquareMeters'))
        elif realestate.propertyType == RealEstate.TYPE_CASA:
            averages = refRealEstate.aggregate(
                Avg('marketPrice'),
                Avg('builtSquareMeters'),
                Avg('terrainSquareMeters'))
            stds = refRealEstate.aggregate(
                StdDev('marketPrice'),
                StdDev('builtSquareMeters'),
                StdDev('terrainSquareMeters'))
    '''

    # Notifications
    notifications = request.user.user.notifications.all()
    notifications_comment_ids = notifications.values_list('comment_id', flat=True) 

    # Comments, for the logbook
    comments = []
    comments = appraisal.comments.select_related('user').all().order_by('-timeCreated')

    # Forms
    forms = {
        'appraisal': FormAppraisal(instance=appraisal,label_suffix=''),
        'comment':FormComment(label_suffix=''),
        'photos':FormPhotos(label_suffix=''),
        'documents':FormDocuments(label_suffix='docs')
        }

    forms['rol'] = []
    for i, rol in enumerate(appraisal.roles.all()):
        forms['rol'].append(FormCreateRol(instance=rol,prefix='r'))
    if len(appraisal.roles.all()) == 0:
        rol = Rol()
        rol.save()
        appraisal.roles.add(rol)
        forms['rol'].append(FormCreateRol(instance=rol,prefix='r'))

    # Select communes for create building
    '''
    communes = Commune.objects.only('name').filter(region=realestate.addressRegion).order_by('name')
    commune = Commune.objects.only('name').get(name__icontains=realestate.addressCommune)
    forms['createRealEstate'].fields['addressCommune'].queryset = communes
    forms['createRealEstate'].fields['addressCommune'].initial = commune
    '''

    # Disable fields if appraisal is finished
    if appraisal.state == appraisal.STATE_FINISHED or appraisal.state == appraisal.STATE_PAUSED:
        for key, form in forms.items():
            if isinstance(form,type([])):
                for f in form:
                    for field in f.fields:
                        f.fields[field].widget.attrs['readonly'] = True
                        f.fields[field].widget.attrs['disabled'] = True
            else:
                for field in form.fields:
                    form.fields[field].widget.attrs['readonly'] = True
                    form.fields[field].widget.attrs['disabled'] = True


    app_properties = getAppraisedProperties(appraisal)

    print(app_properties)

    print(appraisal.appproperty_set.all().values_list('property_id',flat=True))

    context = {
        'appraisal':appraisal,
        'app_properties':app_properties,
        'forms':forms,
        'references': references,
        'comments': comments,
        'htmlBits':htmlBits,
        'notifications_comment_ids':notifications_comment_ids
        }

    a = render(request, 'appraisal/main.html', context)
    return a

def ajax_computeValuations(request):
    '''

    '''
    dict = request.GET.dict()
    UF = 30623
    liquidez = 0.9
    valorComercialUF = float(dict['valor'].strip())
    valorComercialPesos = valorComercialUF*UF
    valorLiquidezUF = valorComercialUF*liquidez
    valorLiquidezPesos = valorComercialPesos*liquidez
    montoSeguroUF = valorLiquidezUF
    montoSeguroPesos = valorLiquidezPesos
    dict = {
        "valorComercialUF": valorComercialUF,
        "valorComercialPesos": valorComercialPesos,
        "valorLiquidezUF": valorLiquidezUF,
        "valorLiquidezPesos": valorLiquidezPesos,
        "montoSeguroUF": montoSeguroUF,
        "montoSeguroPesos": montoSeguroPesos
        }
    return HttpResponse(json.dumps(dict))

def ajax_save_appraisal(request):

    if request.POST['appraisal_id'] == '':
        return JsonResponse({})

    appraisal = getAppraisalFromRequest(request)

    if appraisal:
        form_appraisal = FormAppraisal(request.POST,instance=appraisal)
        form_appraisal.save()

    return JsonResponse({})

def ajax_upload_photo(request):
    print(request.POST)
    print(request.FILES)
    #for photo_file in request.FILES.getlist('photos'):
    #    photo = Photo()
    #    photo.photo = photo_file
    #    photo.description = forms['photos'].cleaned_data['description']
    #    photo.save()
    #    appraisal.photos.add(photo)
    return HttpResponse('')

def ajax_load_tab_value(request):
    pd = propertyData(request.GET)
    return render(request,'appraisal/value.html',{'appraisal':pd['appraisal'],'htmlBits':htmlBits})

def ajax_load_tab_value_comparable(request):
    appraisal = getAppraisalFromRequest(request)
    app_properties = getAppraisedProperties(appraisal)
    json_dict = {}
    json_dict["app_properties"] = app_properties
    json_dict["appraisal"] = appraisal
    json_dict["htmlBits"] = htmlBits
    json_dict["Building"] = Building
    return render(request,'appraisal/value/comparable/body.html',json_dict)

def ajax_load_realestate(request):

    pd = propertyData(request.GET)
    return propertyListHTML(request,pd['appraisal'],pd['real_estate'])

def ajax_add_rol_modal(request):

    form_add_rol = FormCreateRol(label_suffix='')
    pd = propertyData(request.GET)
    return render(request,'appraisal/modals_add_rol.html', 
        {'form_add_rol':form_add_rol,
         'appraisal':pd['appraisal'],
         'real_estate':pd['real_estate'],
         'building':pd['building'],
         'apartment':pd['apartment'],
         'add':1
        })

def ajax_add_rol(request):

    pd = propertyData(request.POST)
    json_dict = {}
    json_dict['roles'] = pd['current'].roles
    pd['current'].roles.create(code=request.POST['code'])
    return render(request,'building/roles.html',json_dict)

def ajax_edit_rol_modal(request):

    pd = propertyData(request.GET)
    rol = pd['current'].roles.get(code=request.GET['code'])
    form_add_rol = FormCreateRol(label_suffix='',instance=rol)
    return render(request,'appraisal/modals_add_rol.html', 
        {'form_add_rol':form_add_rol,
         'appraisal':pd['appraisal'],
         'real_estate':pd['real_estate'],
         'building':pd['building'],
         'apartment':pd['apartment'],
         'rol':rol,
         'edit':1
        })

def ajax_edit_rol(request):

    pd = propertyData(request.POST)
    rol = pd['current'].roles.get(id=request.POST['rol_id'])
    form_add_rol = FormCreateRol(request.POST,instance=rol)
    form_add_rol.save()

    json_dict = {}
    json_dict['roles'] = pd['current'].roles

    return render(request,'building/roles.html',json_dict)

def ajax_remove_rol(request):

    pd = propertyData(request.POST)
    rol = pd['current'].roles.get(id=request.POST['rol_id'])
    pd['current'].roles.remove(rol)
    pd['current'].save()

    json_dict = {}
    json_dict['roles'] = pd['current'].roles

    return render(request,'building/roles.html',json_dict)

def ajax_save_property(request):

    if request.POST['appraisal_id'] == '':
        return JsonResponse({})

    pd = propertyData(request.POST)

    if pd['terrain']:
        form_terrain = FormTerrain(request.POST,instance=pd['terrain'])
        form_terrain.save()

    if pd['house']:
        form_house = FormHouse(request.POST,instance=pd['house'])
        form_house.save()

    if pd['building']:
        form_building = FormBuilding(request.POST,instance=pd['building'])
        form_building.save()

    if pd['apartment']:
        form_apartment = FormApartment(request.POST,instance=pd['apartment'])
        form_apartment.save()

    return JsonResponse({})

def ajax_add_property_similar_modal(request):
    pd = propertyData(request.GET)
    print(pd)
    pd['form_real_estate'] = FormCreateRealEstate(label_suffix='')
    if pd['terrain']:
        pd['form_property'] = FormCreateTerrain(label_suffix='')
    elif pd['house']:
        pd['form_property'] = FormCreateHouse(label_suffix='')
    elif pd['apartment']:
        pd['form_property'] = FormCreateApartment(label_suffix='')
    elif pd['apartment_building']:
        pd['form_property'] = FormCreateApartmentBuilding(label_suffix='')
    pd['htmlBits'] = htmlBits
    references = getSimilarRealEstate(request)
    pd['references'] = references
    realestate = RealEstate.objects.get(pk=request.GET['real_estate_id'])
    pd['realestate'] = realestate
    print(references)
    return render(request, 'appraisal/modals_add_property_similar.html', pd)

def ajax_add_property_similar(request):

    pd = propertyData(request.POST)

    # Primero creamos el real estate

    if not pd['selected']:
        commune = Commune.objects.get(code=request.POST['addressCommune'])
        real_estate_new, existed = create.createOrGetRealEstate(
            addressNumber=request.POST['addressNumber'],
            addressStreet=request.POST['addressStreet'],
            addressCommune=commune,
            addressRegion=commune.region)
        if not existed:
            real_estate_new.sourceUrl = request.POST['sourceUrl']
            real_estate_new.sourceId = request.POST['sourceId']
            real_estate_new.sourceName = request.POST['sourceId']
            real_estate_new.sourceAddedManually = True
    else:
        if pd['terrain_selected']:
            real_estate = pd['terrain_selected'].real_estate
        elif pd['building_selected']:
            real_estate = pd['building_selected'].real_estate
        real_estate.addressNumber = request.POST['addressNumber']
        real_estate.addressStreet = request.POST['addressStreet']
        commune = Commune.objects.get(code=request.POST['addressCommune'])
        real_estate.addressCommune = commune
        real_estate.addressRegion = commune.region
        real_estate.sourceUrl = request.POST['sourceUrl']
        real_estate.sourceId = request.POST['sourceId']
        real_estate.sourceName = request.POST['sourceId']
        real_estate.save()

    if pd['terrain']:
        if not pd['terrain_selected']:
            propiedad, existed = real_estate_new.createOrGetTerrain(addressNumber2=request.POST['addressNumber2'])
        else:
            propiedad = pd['terrain_selected']
        propiedad.frente = request.POST['frente']
        propiedad.fondo = request.POST['fondo']
        propiedad.topography = request.POST['topography']
        propiedad.shape = request.POST['shape']
        propiedad.area = request.POST['area']
        propiedad.marketPrice = request.POST['marketPrice']
        propiedad.save()
        if not pd['terrain_selected']:
            pd['terrain'].terrain_set.add(propiedad) 
            pd['terrain'].save()
        return render(request,'appraisal/value_similar_selected_terrains.html', pd)
    if pd['house']:
        if not pd['house_selected']:
            propiedad, existed = real_estate_new.createOrGetHouse(addressNumber2=request.POST['addressNumber2'])
        else:
            propiedad = pd['house_selected']
        propiedad.bedrooms = request.POST['bedrooms']
        propiedad.bathrooms = request.POST['bathrooms']
        propiedad.builtSquareMeters = request.POST['builtSquareMeters']
        propiedad.terrainSquareMeters = request.POST['terrainSquareMeters']
        propiedad.marketPrice = request.POST['marketPrice']
        propiedad.save()
        #if not existed:
        pd['house'].house_set.add(propiedad)
        pd['house'].save()
        return render(request,'appraisal/value_similar_selected_buildings.html', pd)
    if pd['apartment']:
        if not pd['apartment_selected']:
            propiedad, existed = real_estate_new.createOrGetApartment(
                apartment_building=pd['apartment_building_selected'],
                addressNumber3=request.POST['addressNumber2'])
        else:
            propiedad = pd['apartment_selected']
        propiedad.floor = request.POST['floor']
        propiedad.bedrooms = request.POST['bedrooms']
        propiedad.bathrooms = request.POST['bathrooms']
        propiedad.usefulSquareMeters = request.POST['usefulSquareMeters']
        propiedad.terraceSquareMeters = request.POST['terraceSquareMeters']
        propiedad.marketPrice = request.POST['marketPrice']
        propiedad.save()
        pd['apartment'].apartment_set.add(propiedad)
        pd['apartment'].save()
        print(pd['apartment'].apartment_set.all())
        return render(request,'appraisal/value_similar_selected_buildings.html', pd)
    if pd['apartment_building']:
        if not pd['apartment_building']:
            propiedad, existed = real_estate_new.createOrGetApartmentBuilding(addressNumber2=request.POST['addressNumber2'])
        else:
            propiedad = pd['apartment_building_selected']
        propiedad.builtSquareMeters = request.POST['builtSquareMeters']
        propiedad.marketPrice = request.POST['marketPrice']
        propiedad.save()
        pd['apartment_building'].apartmentbuilding_set.add(propiedad)
        pd['apartment_building'].save()
        return render(request,'appraisal/value_similar_selected_buildings.html', pd)

def ajax_edit_property_similar_modal(request):
    
    if request.GET['appraisal_id'] == '':
        return JsonResponse({})

    pd = propertyData(request.GET)
    if pd['terrain']:
        pd['form_real_estate'] = FormCreateRealEstate(label_suffix='',instance=pd['terrain_selected'].real_estate)
        pd['form_property'] = FormCreateTerrain(label_suffix='',instance=pd['terrain_selected'])
    if pd['house']:
        pd['form_real_estate'] = FormCreateRealEstate(label_suffix='',instance=pd['house_selected'].building.real_estate)
        pd['form_property'] = FormCreateHouse(label_suffix='',instance=pd['house_selected'])
    if pd['apartment_building']:
        pd['form_real_estate'] = FormCreateRealEstate(label_suffix='',instance=pd['apartment_building_selected'].building.real_estate)
        pd['form_property'] = FormCreateApartmentBuilding(label_suffix='',instance=pd['apartment_building_selected'])

    return render(request,'appraisal/modals_add_property_similar.html', pd)

def ajax_edit_property_similar(request):

    pd = propertyData(request.POST)
    pd['form_real_estate'] = FormCreateRealEstate(request.POST,instance=pd['real_estate'])
    if pd['terrain']:
        pd['form_property'] = FormCreateTerrain(request.POST,instance=pd['terrain'])

    return render(request,'appraisal/modals_add_property_similar.html', pd) 

def ajax_remove_property_similar(request):

    pd = propertyData(request.GET)

    if pd['terrain']:
        pd['terrain'].terrain_set.remove(pd['terrain_selected'])
        return render(request,'appraisal/realestate_value_similar_selected_terrains.html', pd)
    elif pd['house']:
        pd['house'].house_set.remove(pd['house_selected'])
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)
    elif pd['apartment']:
        pd['apartment'].apartment_set.remove(pd['apartment_selected'])
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)
    elif pd['apartment_building']:
        pd['apartment_building'].apartmentbuilding_set.remove(pd['apartment_building_selected'])
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)

def ajax_photo_modal(request):
    
    data = {}
    appraisal = Appraisal.objects.get(id=request.GET['appraisal_id'])
    if 'photo_id' in request.GET:
        photo = appraisal.photos.get(id=request.GET['photo_id'])
        data['form'] = FormPhotos(label_suffix='',initial={'category':photo.category,'description':photo.description})
        data['photo'] = photo
        if photo.fixed:
            data['form'].fields['category'].widget.attrs['disabled'] = True
        return render(request,'appraisal/modals_photo.html', data)
    else:
        data['form'] = FormPhotos(label_suffix='')
        return render(request,'appraisal/modals_photo.html', data)

def ajax_photo_save(request):
    appraisal = Appraisal.objects.get(id=request.POST['appraisal_id'])
    if 'photo_id' in request.POST and request.POST['photo_id'] != '':
        photo = appraisal.photos.get(id=request.POST['photo_id'])
        for photo_file in request.FILES.getlist('photos'):
            photo.photo = photo_file
        photo.description = request.POST['description']
        photo.save()
        return render(request,'appraisal/annex_photo.html',{'photo':photo})
    else:
        photo = appraisal.photos.create(
            category=request.POST['category'],
            description=request.POST['description'],
            fixed=False)
        for photo_file in request.FILES.getlist('photos'):
            photo.photo = photo_file
        photo.save()
        return render(request,'appraisal/annex_photo_container.html',{'appraisal':appraisal})

def ajax_photo_remove(request):

    appraisal = Appraisal.objects.get(id=request.GET['appraisal_id'])
    photo = appraisal.photos.get(id=request.GET['photo_id'])
    if photo.fixed:
        photo.photo = None
        photo.description = None
        photo.save()
    else:
        appraisal.photos.remove(photo)
        appraisal.save()

    return render(request,'appraisal/annex_photo.html',{'photo':photo})