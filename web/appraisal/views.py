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

import reversion
from copy import deepcopy
from reversion.models import Version

import os
import csv

from .forms import FormRealEstate
from .forms import FormTerrain
from .forms import FormBuilding
from .forms import FormApartment
from .forms import FormHouse
from .forms import FormApartmentBuilding
from .forms import FormAppraisal
from .forms import FormComment
from .forms import FormPhotos
from .forms import FormDocuments
from .forms import FormEditAddress
from .forms import FormAddAddress
from .forms import FormAddProperty
from .forms import FormEditProperty
from .forms import FormAddApartment
from .forms import FormAddRol
from .forms import FormCreateProperty
from .forms import FormCreateTerrain
from .forms import FormCreateApartmentBuilding
from .forms import FormCreateApartment
from .forms import FormCreateHouse
from .forms import FormCreateAsset
from .forms import FormCreateRol
from .forms import FormCreateRealEstate
from create import create


import viz.maps as maps
import appraisal.related as related
from appraisal.export import *
from dbase.globals import *
from main.html_bits import *

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

def getAppraisal(request,id):
    '''
        Given an appraisal id, returns the apraisal object.
        It checks for errors and sends to the correct error page.
    '''
    try:
        appraisal = Appraisal.objects.get(pk=id)
        return appraisal
    except Appraisal.DoesNotExist:
        context = {'error_message': 'Appraisal not found?'}
        return render(request, 'appraisal/error.html', context)
    except MultipleObjectsReturned:
        context = {'error_message': 'More than one appraisal of the same property'}
        return render(request, 'appraisal/error.html', context)


def save_appraisal(request,forms,comment):
    with reversion.create_revision():
        forms['appraisal'].save()
        reversion.set_user(request.user)
        reversion.set_comment(comment)
        return

def save(request,forms,appraisal,realEstate):
    if realEstate.propertyType == RealEstate.TYPE_APARTMENT:
        if forms['building'].is_valid() and \
           forms['property'].is_valid() and \
           forms['realestate'].is_valid() and \
           forms['appraisal'].is_valid():

            # The order of these saves is important, real estate should be last, such that
            # the common variables don't get overwritten by defaults when saving the derived
            # objects.
            forms['building'].save()
            forms['property'].save()
            forms['realestate'].save()
            save_appraisal(request,forms,'Saved')

            # Check roles

            rol_codes = request.POST.getlist('r-code')
            rol_states = request.POST.getlist('r-state')
            rol_ids = request.POST.getlist('r-id')
            rol_deletes = request.POST.getlist('r-delete')
            print(request.POST)
            for i, rol_code in enumerate(rol_codes):
                if int(rol_ids[i]) > 0:
                    rol = appraisal.roles.all().get(id=rol_ids[i])
                    if int(rol_deletes[i]):
                        rol.delete()
                    else:
                        rol.code = rol_code
                        rol.state = rol_states[i]
                        rol.save()
                else:
                    if int(rol_deletes[i]): continue
                    rol = Rol(code=rol_code,state=rol_states[i])
                    rol.save()
                    appraisal.roles.add(rol)
                    appraisal.save()

            re_ids = request.POST.getlist('valuationRealEstateRow')
            re_ids_re = request.POST.getlist('valuationRealEstateRemove')
            for i, re_id in enumerate(re_ids):
                if not int(re_ids_re[i]):
                    valuation_add_realestate(request,forms,appraisal,re_id)
                else:
                    valuation_remove_realestate(request,forms,appraisal,re_id)
            return True
        else:
            print('errors',forms['building'].errors)
            print('errors',forms['property'].errors)
            print('errors',forms['realestate'].errors)
            print('errors',forms['appraisal'].errors)
    elif realEstate.propertyType == RealEstate.TYPE_HOUSE:
        if forms['realestate'].is_valid() and \
           forms['property'].is_valid() and \
           forms['appraisal'].is_valid():
            
            forms['property'].save()
            forms['realestate'].save()
            save_appraisal(request,forms,'Saved')

            # Check roles
            rol_codes = request.POST.getlist('r-code')
            rol_states = request.POST.getlist('r-state')
            rol_ids = request.POST.getlist('r-id')
            rol_deletes = request.POST.getlist('r-delete')
            print(request.POST)
            for i, rol_code in enumerate(rol_codes):
                if int(rol_ids[i]) > 0:
                    rol = appraisal.roles.all().get(id=rol_ids[i])
                    if int(rol_deletes[i]):
                        rol.delete()
                    else:
                        rol.code = rol_code
                        rol.state = rol_states[i]
                        rol.save()
                else:
                    if int(rol_deletes[i]): continue
                    rol = Rol(code=rol_code,state=rol_states[i])
                    rol.save()
                    appraisal.roles.add(rol)
                    appraisal.save()

            re_ids = request.POST.getlist('valuationRealEstateRow')
            re_ids_re = request.POST.getlist('valuationRealEstateRemove')
            for i, re_id in enumerate(re_ids):
                if not int(re_ids_re[i]):
                    valuation_add_realestate(request,forms,appraisal,re_id)
                else:
                    valuation_remove_realestate(request,forms,appraisal,re_id)
            return True
        else:
            print('errors',forms['property'].errors)
            print('errors',forms['realestate'].errors)
            print('errors',forms['appraisal'].errors)
    else:
        return False

def delete(request,appraisal):
    appraisal.delete()
    context = {}
    return render(request,'appraisal/deleted.html',context)

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

def restore(request,forms, appraisal):
    appraisal.timeFinished = None
    appraisal.state = Appraisal.STATE_ACTIVE
    save_appraisal(request,forms,'Restored')
    return True

def comment(request,forms,appraisal):
    '''
    Create comment based on the field commentText of the form.
    '''
    if forms['comment'].is_valid():
        print('comment')
        text = forms['comment'].cleaned_data['commentText']
        conflict = forms['comment'].cleaned_data['commentConflict']
        if conflict:
            appraisal.state = appraisal.STATE_PAUSED
            appraisal.timePaused = datetime.datetime.now()
            appraisal.save()
        comment = Comment(
            user=request.user,
            text=text,
            timeCreated=datetime.datetime.now(),
            appraisal=appraisal,
            conflict=conflict)
        comment.save()
    else:
        print(forms['comment'].errors)
    return True

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

def delete_photo(request,forms,appraisal):
    appraisal.photos.remove(request.POST['btn_delete_photo'])
    if forms['appraisal'].is_valid():
        save_appraisal(request, forms, 'Removed picture(s)')

def delete_document(request,forms,appraisal):
    appraisal.documents.remove(request.POST['btn_delete_document'])
    if forms['appraisal'].is_valid():
        save_appraisal(request, forms, 'Removed document(s)')

def save_photo(request,forms,appraisal):
    try:
        photo_id = request.POST['btn_save_photo']
        photo = Photo.objects.get(id=photo_id)
        photo.description = request.POST['photo_description_'+str(photo_id)]
        photo.save()
        save_appraisal(request, forms, 'Chaged photo description')
    except Photo.DoesNotExist:
        return

def save_document(request,forms,appraisal):
    try:
        document_id = request.POST['btn_save_document']
        document = Document.objects.get(id=document_id)
        document.description = request.POST['document_description_'+str(document_id)]
        document.save()
        save_appraisal(request, forms, 'Chaged document description')
    except Document.DoesNotExist:
        return

def add_realestate(request,forms,appraisal,realestate):
    form = forms['createRealEstate']
    if realestate.propertyType == RealEstate.TYPE_APARTMENT:
        if form.is_valid():

            building = create.building_create(
                realestate.addressRegion,
                form.cleaned_data['addressCommune'],
                form.cleaned_data['addressStreet'],
                form.cleaned_data['addressNumber'])
            building.sourceUrl = form.cleaned_data['sourceUrl']
            building.sourceId = form.cleaned_data['sourceId']
            building.sourceName = form.cleaned_data['sourceName']
            building.fromApartment = True
            building.save()

            apartment = create.apartment_create(building,0)
            apartment.sourceUrl = form.cleaned_data['sourceUrl']
            apartment.sourceId = form.cleaned_data['sourceId']
            apartment.sourceName = form.cleaned_data['sourceName']
            apartment.marketPrice = form.cleaned_data['marketPrice']
            apartment.bedrooms = form.cleaned_data['bedrooms']
            apartment.bathrooms = form.cleaned_data['bathrooms']
            apartment.usefulSquareMeters = form.cleaned_data['usefulSquareMeters']
            apartment.terraceSquareMeters = form.cleaned_data['terraceSquareMeters']
            apartment.marketPrice = form.cleaned_data['marketPrice']
            apartment.save()

            valuation_add_realestate(request,forms,appraisal,apartment.realestate_ptr.id)
        else:
            print(forms['createRealEstate'].errors)
    elif realestate.propertyType == RealEstate.TYPE_HOUSE:
        if form.is_valid():
            house = create.house_create(
                realestate.addressRegion,
                form.cleaned_data['addressCommune'],
                form.cleaned_data['addressStreet'],
                form.cleaned_data['addressNumber'],
                form.cleaned_data['addressNumber2'])
            house.sourceUrl = form.cleaned_data['sourceUrl']
            house.sourceId = form.cleaned_data['sourceId']
            house.sourceName = form.cleaned_data['sourceName']
            house.marketPrice = form.cleaned_data['marketPrice']
            house.bedrooms = form.cleaned_data['bedrooms']
            house.bathrooms = form.cleaned_data['bathrooms']
            house.builtSquareMeters = form.cleaned_data['builtSquareMeters']
            house.terrainSquareMeters = form.cleaned_data['terrainSquareMeters']
            house.marketPrice = form.cleaned_data['marketPrice']
            house.save()
            valuation_add_realestate(request,forms,appraisal,house.realestate_ptr.id)
        else:
            print(forms['createRealEstate'].errors)
    else:
        return False

def valuation_add_realestate(request,forms,appraisal,realestate_id):
    try:
        realestate = RealEstate.objects.get(id=realestate_id)
        if realestate in appraisal.valuationRealEstate.all():
            print('Already existed')
        else:
            print('New new new')
            appraisal.valuationRealEstate.add(realestate)
            appraisal.save()
    except RealEstate.DoesNotExist:
        return

def valuation_remove_realestate(request,forms,appraisal,realestate_id):
    try:
        realestate = RealEstate.objects.get(id=realestate_id)
        if realestate in appraisal.valuationRealEstate.all():
            appraisal.valuationRealEstate.remove(realestate_id)
    except RealEstate.DoesNotExist:
        return

def valuation_add_asset(request,forms,appraisal,realestate):
    '''
    Create asset based on forms. A bit complicated because some fields
    of the form are always active ('area', 'UFPerArea'), but we need to add
    only those that have been activated to be edited. The button edit
    changes the hidden inout construction_edited. All of the rows have
    'construction_id'.
    '''
    print('valuation_add_asset')
    c = 0
    for i, cid in enumerate(request.POST.getlist('asset_id')):
        if int(request.POST.getlist('asset_edited')[i]):
            request_post = request.POST.copy()
            # These are not always active, so count with c.
            request_post['a-name'] = request_post.getlist('a-name')[c]
            request_post['a-value'] = request_post.getlist('a-value')[i]
            forms['createAsset'] = FormCreateAsset(request_post,prefix='a')
            if forms['createAsset'].is_valid():
                # Does the terrain exist?
                try:
                    asset = Asset.objects.get(id=cid)
                    # It exists, so update.
                    form = FormCreateAsset(request_post,instance=asset,prefix='a')
                    form.save()
                except Asset.DoesNotExist:
                    # It's a new one, so create.
                    asset = forms['createAsset'].save()
                    realestate.assets.add(asset)
                    realestate.save()
            else:
                print(forms['createAsset'].errors)
            c =+ 1

def valuation_add_terrain(request,forms,appraisal,realestate):
    '''
    Create terrain based on forms. A bit complicated because some fields
    of the form are always active ('area', 'UFPerArea'), but we need to add
    only those that have been activated to be edited. The button edit
    changes the hidden inout construction_edited. All of the rows have
    'construction_id'.
    '''
    print('valuation_add_terrain')
    c = 0
    for i, cid in enumerate(request.POST.getlist('terrain_id')):
        if int(request.POST.getlist('terrain_edited')[i]):
            request_post = request.POST.copy()
            # These are not always active, so count with c.
            request_post['t-name'] = request_post.getlist('t-name')[c]
            request_post['t-frente'] = request_post.getlist('t-frente')[c]
            request_post['t-fondo'] = request_post.getlist('t-fondo')[c]
            request_post['t-topography'] = request_post.getlist('t-topography')[c]
            request_post['t-shape'] = request_post.getlist('t-shape')[c]
            request_post['t-rol'] = request_post.getlist('t-rol')[c]
            request_post['t-area'] = request_post.getlist('t-area')[i]
            request_post['t-UFPerArea'] = request_post.getlist('t-UFPerArea')[i]
            #forms['createTerrain'] = FormCreateTerrain(request_post,prefix='t')
            '''
            if forms['createTerrain'].is_valid():
                # Does the terrain exist?
                try:
                    terrain = Terrain.objects.get(id=cid)
                    # It exists, so update.
                    form = FormCreateTerrain(request_post,instance=terrain,prefix='t')
                    form.save()
                except Terrain.DoesNotExist:
                    # It's a new one, so create.
                    terrain = forms['createTerrain'].save()
                    realestate.terrains.add(terrain)
                    realestate.save()
            else:
                print(forms['createTerrain'].errors)
            '''
            c =+ 1

def valuation_add_construction(request,forms,appraisal,realestate):
    '''
    Create constructions based on forms. A bit complicated because some fields
    of the form are always active ('area', 'UFPerArea'), but we need to add
    only those that have been activated to be edited. The button edit
    changes the hidden inout construction_edited. All of the rows have
    'construction_id'.
    '''
    print('valuation_add_construction')
    c = 0
    for i, cid in enumerate(request.POST.getlist('construction_id')):
        if int(request.POST.getlist('construction_edited')[i]):
            requestpost = request.POST.copy()
            # These are not always active, so count with c.
            requestpost['c-name'] = requestpost.getlist('c-name')[c]
            requestpost['c-material'] = requestpost.getlist('c-material')[c]
            requestpost['c-year'] = requestpost.getlist('c-year')[c]
            if len(requestpost['c-year']) == 4:
                requestpost['c-year'] = requestpost['c-year']+'-01-01'
            requestpost['c-prenda'] = requestpost.getlist('c-prenda')[c]
            requestpost['c-recepcion'] = requestpost.getlist('c-recepcion')[c]
            requestpost['c-state'] = requestpost.getlist('c-state')[c]
            requestpost['c-quality'] = requestpost.getlist('c-quality')[c]
            requestpost['c-rol'] = requestpost.getlist('c-rol')[c]
            # These are always active, so count with i
            requestpost['c-area'] = requestpost.getlist('c-area')[i]
            requestpost['c-UFPerArea'] = requestpost.getlist('c-UFPerArea')[i]
            #forms['createConstruction'] = FormCreateConstruction(requestpost,prefix='c')
            '''
            if forms['createConstruction'].is_valid():
                # Does the construction exist?
                try:
                    construction = Construction.objects.get(id=cid)
                    # It exists, so update.
                    form = FormCreateConstruction(requestpost,instance=construction,prefix='c')
                    form.save()
                except Construction.DoesNotExist:
                    # It's a new one, so create.
                    construction = forms['createConstruction'].save()
                    realestate.constructions.add(construction)
                    realestate.save()
            else:
                print(forms['createConstruction'].errors)
            '''
            c =+ 1

'''
def valuation_remove_construction(request,forms,appraisal,realestate):
    try:
        construction = Construction.objects.get(id=int(request.POST['btn_valuation_remove_construction']))
        construction.delete()
    except Construction.DoesNotExist:
        print('Error')
'''
'''
def valuation_remove_terrain(request,forms,appraisal,realestate):
    try:
        terrain = Terrain.objects.get(id=int(request.POST['btn_valuation_remove_terrain']))
        terrain.delete()
    except Terrain.DoesNotExist:
        print('Error')
'''

def float_es(string):
    string = string.replace('.','')
    string = string.replace(',','.')
    try:
        return float(string)
    except ValueError:
        return ""

def clean_request_post(request_post):

    if 'valorUF' in request_post.keys():
        request_post['valorUF'] = float_es(request_post['valorUF'])
    if 'c-year' in request_post.keys():
        request_post['c-year'] = request_post['c-year']+'-01-01'

    return request_post


def view_appraisal(request, **kwargs):
    '''
    General view for appraisals. Gets a variable number of parameters depending
    on the type of realestate.
    '''
    appraisal = getAppraisal(request,kwargs['appraisal_id'])
    if isinstance(appraisal,HttpResponse):
        return appraisal

    if request.method == 'POST':

        request_post = clean_request_post(request.POST.copy())

        # Process forms
        forms = {}
        forms['appraisal'] = FormAppraisal(request_post,request.FILES,instance=appraisal)
        forms['comment'] = FormComment(request_post)
        forms['realestate'] = FormRealEstate(request_post,instance=realestate)
        #forms['createConstruction'] = FormCreateConstruction(request_post,prefix='c')
        forms['createTerrain'] = FormCreateTerrain(request_post,prefix='t')
        forms['createAsset'] = FormCreateAsset(request_post,prefix='a')
        forms['photos'] = FormPhotos(request_post,request.FILES)
        forms['documents'] = FormDocuments(request_post,request.FILES,prefix='docs')
        forms['rol'] = FormCreateRol(request_post,prefix='r')
        if realestate.propertyType == RealEstate.TYPE_APARTMENT:
            forms['property'] = FormApartment(request_post,instance=realestate.apartment)
            forms['building'] = FormBuilding(request_post,instance=realestate.apartment.building_in)
            apartment_new = Apartment()
            forms['createRealEstate'] = FormCreateApartment(request_post,prefix='vc',instance=apartment_new)
        if realestate.propertyType == RealEstate.TYPE_HOUSE:
            forms['property'] = FormHouse(request_post,instance=realestate.house)
            house_new = House()
            forms['createRealEstate'] = FormCreateHouse(request_post,prefix='vc',instance=house_new)

        # Switch to action
        if 'btn_save' in request_post.keys():
            ret = save(request,forms,appraisal,realestate)
        elif 'btn_export' in request_post.keys():
            ret = export(request,forms,appraisal,realestate)
        elif 'btn_delete' in request_post.keys():
            ret = delete(request,appraisal)
        elif 'btn_finish' in request_post.keys():
            ret = finish(request,forms,appraisal)
        elif 'btn_restore' in request_post.keys():
            ret = restore(request,forms,appraisal)
        elif 'btn_comment' in request_post.keys():
            ret = comment(request,forms,appraisal)
        elif 'btn_add_realestate' in request_post.keys():
            ret = add_realestate(request,forms,appraisal,realestate)
        elif 'btn_valuation_add_realestate' in request_post.keys():
            ret = valuation_add_realestate(request,forms,appraisal,request_post['btn_valuation_add_realestate'])
        elif 'btn_valuation_add_construction' in request_post.keys():
            ret = valuation_add_construction(request,forms,appraisal,realestate)
        elif 'btn_valuation_add_terrain' in request_post.keys():
            ret = valuation_add_terrain(request,forms,appraisal,realestate)
        elif 'btn_valuation_add_asset' in request_post.keys():
            ret = valuation_add_asset(request,forms,appraisal,realestate)
        elif 'btn_valuation_remove_construction' in request_post.keys():
            ret = valuation_remove_construction(request,forms,appraisal,realestate)
        elif 'btn_valuation_remove_terrain' in request_post.keys():
            ret = valuation_remove_terrain(request,forms,appraisal,realestate)
        elif 'btn_assign_tasador' in request_post.keys():
            ret = assign_tasador(request,forms,appraisal)
        elif 'btn_assign_visador' in request_post.keys():
            ret = assign_visador(request,forms,appraisal)
        elif 'btn_upload_photo' in request_post.keys():
            ret = upload_photo(request,forms,appraisal)
        elif 'btn_upload_document' in request_post.keys():
            ret = upload_document(request,forms,appraisal)
        elif 'btn_delete_photo' in request_post.keys():
            ret = delete_photo(request,forms,appraisal)
        elif 'btn_delete_document' in request_post.keys():
            ret = delete_document(request,forms,appraisal)
        elif 'btn_save_photo' in request_post.keys():
            ret = save_photo(request,forms,appraisal)
        elif 'btn_save_document' in request_post.keys():
            ret = save_document(request,forms,appraisal)
        else:
            ret = False

        if isinstance(ret, HttpResponse): return ret

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

    # Visadores and tasadores for the modals where you can select them.
    tasadores = User.objects.filter(groups__name__in=['tasador'])
    visadores = User.objects.filter(groups__name__in=['visador'])

    # Comments, for the logbook
    comments = []
    comments = Comment.objects.filter(appraisal=appraisal).order_by('-timeCreated')

    # Forms
    forms = {
        'appraisal': FormAppraisal(instance=appraisal,label_suffix=''),
        'comment':FormComment(label_suffix=''),
        'photos':FormPhotos(label_suffix=''),
        'documents':FormDocuments(label_suffix='docs')
        }

    '''
    if realestate.propertyType == Building.TYPE_DEPARTAMENTO:
        forms['property'] = FormApartment(instance=realestate.buildings.first(),label_suffix='')
        #forms['building'] = FormBuilding(instance=realestate.buildings.first().apartment_building,label_suffix='')
        forms['createRealEstate'] = FormCreateApartment(prefix='vc',label_suffix='')
        #forms['createConstruction'] = FormCreateConstruction(prefix='c',label_suffix='')
        forms['createTerrain'] = FormCreateTerrain(prefix='t',label_suffix='')
        forms['createAsset'] = FormCreateAsset(prefix='a',label_suffix='')
    elif realestate.propertyType == Building.TYPE_CASA:
        forms['property'] = FormHouse(instance=realestate.buildings.first(),label_suffix='')
        forms['createRealEstate'] = FormCreateHouse(prefix='vc',label_suffix='')
        #forms['createConstruction'] = FormCreateConstruction(prefix='c',label_suffix='')
        forms['createTerrain'] = FormCreateTerrain(prefix='t',label_suffix='')
        forms['createAsset'] = FormCreateAsset(prefix='a',label_suffix='')
    elif realestate.propertyType == Building.TYPE_EDIFICIO:
        #forms['createConstruction'] = FormCreateConstruction(prefix='c',label_suffix='')
        forms['createTerrain'] = FormCreateTerrain(prefix='t',label_suffix='')
        forms['createAsset'] = FormCreateAsset(prefix='a',label_suffix='')
    elif realestate.propertyType == Building.TYPE_CONDOMINIO:
        #forms['createConstruction'] = FormCreateConstruction(prefix='c',label_suffix='')
        forms['createTerrain'] = FormCreateTerrain(prefix='t',label_suffix='')
        forms['createAsset'] = FormCreateAsset(prefix='a',label_suffix='')
    '''

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

    context = {
        'appraisal':appraisal,
        'forms':forms,
        #'realestate': realestate,
        'references': references,
        #'averages': averages,
        #'stds': stds,
        'tasadores':tasadores,
        'visadores':visadores,
        'comments': comments,
        #'plot_map':plot_map,
        'htmlBits':htmlBits
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

def propertyData(rd):

    current = None
    appraisal = None
    if 'appraisal_id' in rd:
        try:
            appraisal_id = int(rd['appraisal_id'])
            try:
                appraisal = Appraisal.objects.get(id=appraisal_id)
            except Appraisal.DoesNotExist:
                appraisal = None
        except ValueError:
            appraisal = None

    real_estate = None
    if 'real_estate_id' in rd:
        try:
            real_estate_id = int(rd['real_estate_id'])
            try:
                real_estate = RealEstate.objects.get(id=real_estate_id)
            except RealEstate.DoesNotExist:
                real_estate = None
        except ValueError:
            real_estate = None

    building = None
    if 'building_id' in rd:
        try:
            building_id = int(rd['building_id'])
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                building = None
        except ValueError:
            building = None

    house = None
    apartment = None
    apartment_building = None

    if building:

        if building.propertyType == Building.TYPE_CASA:
            house = building.house
            current = house

        if building.propertyType == Building.TYPE_EDIFICIO:
            apartment_building = building.apartmentbuilding
            if 'apartment_id' in rd:
                try:
                    apartment_id = int(rd['apartment_id'])
                    try:
                        apartment = apartment_building.apartment_set.get(id=apartment_id)
                        current = apartment
                    except:
                        apartment = None
                        current = apartment_building
                except ValueError:
                    apartment = None
                    current = apartment_building
            else:
                apartment = None
                current = apartment_building
        else:
            apartment_building = None

    terrain = None
    if 'terrain_id' in rd and real_estate:
        try:
            terrain_id = int(rd['terrain_id'])
            try:
                terrain = real_estate.terrains.get(id=terrain_id)
                current = terrain
            except Terrain.DoesNotExist:
                terrain = None
        except ValueError:
            terrain = None  

    selected = None
    terrain_selected = None
    if terrain and 'property_selected_id' in rd:
        try:
            terrain_selected_id = int(rd['property_selected_id'])
            try:
                terrain_selected = terrain.terrain_set.get(id=terrain_selected_id)
                selected = terrain_selected
            except Terrain.DoesNotExist:
                terrain_selected = None
        except ValueError:
            terrain_selected = None

    building_selected = None
    house_selected = None
    if house and 'property_selected_id' in rd:
        try:
            house_selected_id = int(rd['property_selected_id'])
            try:
                house_selected = house.house_set.get(id=house_selected_id)
                selected = house_selected
                building_selected = house_selected.building
            except Terrain.DoesNotExist:
                house_selected = None
        except ValueError:
            house_selected = None

    apartment_building_selected = None
    if apartment_building and not apartment and 'property_selected_id' in rd:
        try:
            apartment_building_selected_id = int(rd['property_selected_id'])
            try:
                apartment_building_selected = apartment_building.apartmentbuilding_set.get(id=apartment_building_selected_id)
                selected = apartment_building_selected
                building_selected = apartment_building_selected.building
            except Terrain.DoesNotExist:
                apartment_building_selected = None
        except ValueError:
            apartment_building_selected = None

    apartment_selected = None
    if apartment and 'property_selected_id' in rd:
        try:
            apartment_selected_id = int(rd['property_selected_id'])
            try:
                apartment_selected = apartment.apartment_set.get(id=apartment_selected_id)
                selected = apartment_selected
                building_selected = apartment_selected.apartment_building.building
            except Terrain.DoesNotExist:
                apartment_selected = None
        except ValueError:
            apartment_selected = None

    return {
        'appraisal':appraisal,
        'real_estate':real_estate,
        'building':building,
        'house':house,
        'apartment_building':apartment_building,
        'apartment':apartment,
        'terrain':terrain,
        'current':current,
        'terrain_selected':terrain_selected,
        'building_selected':building_selected,
        'house_selected':house_selected,
        'apartment_building_selected':apartment_building_selected,
        'apartment_selected':apartment_selected,
        'selected':selected
        }


def propertyListHTML(request,real_estate):

    buildings = real_estate.buildings.all()
    print(buildings)
    terrains = real_estate.terrains.all()
    print(terrains)
    return render(request,'appraisal/property_list.html',
        {'real_estate':real_estate,
         'terrains':terrains,
         'buildings':buildings})

def ajax_load_tab_value(request):
    pd = propertyData(request.GET)
    return render(request,'appraisal/value.html',{'appraisal':pd['appraisal'],'htmlBits':htmlBits})

def ajax_edit_address_modal(request):

    pd = propertyData(request.GET)
    json_dict = {}
    json_dict['form_edit_address'] = FormEditAddress(label_suffix='',
        initial={
            'addressNumber': pd['real_estate'].addressNumber,
            'addressStreet': pd['real_estate'].addressStreet,
            'addressCommune': pd['real_estate'].addressCommune.code,
            'addressRegion': pd['real_estate'].addressRegion.code })

    return render(request,'appraisal/modals_edit_address.html',{**pd,**json_dict})

def ajax_add_address_modal(request):

    pd = propertyData(request.GET)
    real_estate = pd['appraisal'].real_estates.first()
    form_add_address = FormAddAddress(label_suffix='',
        initial={
            'addressNumber': '',
            'addressStreet': '',
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code })

    return render(request,'appraisal/modals_add_address.html',
        {'appraisal':pd['appraisal'],'form_add_address':form_add_address})

def ajax_remove_address_modal(request):

    pd = propertyData(request.GET)
    return render(request,'appraisal/modals_remove_address.html', pd)

def ajax_edit_address(request):

    pd = propertyData(request.POST)
    commune = Commune.objects.get(code=request.POST['addressCommune'])
    # Check if there is already a real estate with this address
    try:
        real_estate = pd['appraisal'].real_estates.get(
            addressNumber=request.POST['addressNumber'],
            addressStreet=request.POST['addressStreet'],
            addressCommune=commune,
            addressRegion=commune.region)
        return JsonResponse({'error':'La dirección especificada ya es parte de esta tasación'})
    except RealEstate.DoesNotExist:
        pd['real_estate'].addressNumber = request.POST['addressNumber']
        pd['real_estate'].addressStreet = request.POST['addressStreet']
        pd['real_estate'].addressCommune = commune
        pd['real_estate'].addressRegion = commune.region
        pd['real_estate'].save()
        return JsonResponse({'address':pd['real_estate'].address})

def ajax_add_address(request):

    pd = propertyData(request.POST)
    commune = Commune.objects.get(code=request.POST['addressCommune'])
    real_estate, created = create.createOrGetRealEstate(
        addressNumber=request.POST['addressNumber'],
        addressStreet=request.POST['addressStreet'],
        addressCommune=commune,
        addressRegion=commune.region)

    try:
        pd['appraisal'].real_estates.get(id=real_estate.id)
        # El real estate ya está en este appraisal
        return JsonResponse({'error':'La dirección especificada ya es parte de esta tasación'})
    except RealEstate.DoesNotExist:
        pd['appraisal'].real_estates.add(real_estate)
        pd['appraisal'].save()
        return render(request,'appraisal/address_list.html', pd)

def ajax_remove_address(request):

    pd = propertyData(request.POST)
    pd['appraisal'].real_estates.remove(pd['real_estate'])
    pd['appraisal'].save()
    return JsonResponse({})

def ajax_load_realestate(request):

    pd = propertyData(request.GET)
    return propertyListHTML(request,pd['real_estate'])

def ajax_add_property_modal(request):

    pd = propertyData(request.GET)
    json_dict = {}
    json_dict['form_add_property'] = FormAddProperty(label_suffix="")
    json_dict['property_types'] = Building.propertyType_dict
    return render(request,'appraisal/modals_add_property.html', {**pd,**json_dict})

def ajax_add_property(request):

    pd = propertyData(request.POST)

    prop = pd['real_estate'].createOrGetProperty(
        int(request.POST['propertyType']),
        request.POST['addressNumber2'],
        if_exists_false=True)

    if isinstance(prop,type(True)):
        if not prop:
            return JsonResponse({'error':"La propiedad ya existe"})
    else:
        return propertyListHTML(request,pd['real_estate'])

def ajax_add_apartment_modal(request):

    pd = propertyData(request.GET)
    json_dict = {}
    json_dict['form_add_apartment'] = FormAddApartment()
    return render(request,'appraisal/modals_add_apartment.html', {**pd,**json_dict})

def ajax_add_apartment(request):

    pd = propertyData(request.POST)
    json_dict = {}
    pd['real_estate'].createOrGetDepartamento(pd['apartment_building'].addressNumber2,request.POST['addressNumber2'])
    return propertyListHTML(request,pd['real_estate'])

def ajax_edit_property_modal(request):

    pd = propertyData(request.GET)
    json_dict = {}
    json_dict['form_edit_property'] = FormEditProperty(label_suffix='',initial={'addressNumber2': pd['current'].addressNumber2})
    return render(request,'appraisal/modals_edit_property.html',{**json_dict,**pd})

def ajax_edit_property(request):

    pd = propertyData(request.POST)
    pd['current'].addressNumber2 = request.POST['addressNumber2']
    pd['current'].save()
    return propertyListHTML(request,pd['real_estate'])
    
def ajax_remove_property(request):

    pd = propertyData(request.POST)
    if pd['apartment']:
        pd['apartment'].delete()
    elif pd['building']:
        pd['building'].delete()
    else:
        pd['current'].delete()
    return propertyListHTML(request,pd['real_estate'])
    
def ajax_show_property(request):

    pd = propertyData(request.GET)

    json_dict = {}
    json_dict['building'] = pd['building']

    if pd['apartment']:
        json_dict['apartment'] = pd['apartment']
        form_apartment = FormApartment(instance=pd['apartment'],label_suffix='')
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        forms = {'apartment':form_apartment,'building':form_building}
        json_dict['property_type'] = Building.TYPE_DEPARTAMENTO
        json_dict['roles'] = pd['apartment'].roles
        html = 'building/general.html'
    elif pd['apartment_building']:
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        form_apartment_building = FormApartmentBuilding(instance=pd['apartment_building'],label_suffix='')
        forms = {'building':form_building,'apartment_building':form_apartment_building}
        json_dict['property_type'] = Building.TYPE_EDIFICIO
        json_dict['roles'] = pd['apartment_building'].roles
        html = 'building/general.html'
    elif pd['house']:
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        form_house = FormHouse(instance=pd['house'],label_suffix='')
        forms = {'building':form_building,'house':form_house}
        json_dict['property_type'] = Building.TYPE_CASA
        json_dict['roles'] = pd['house'].roles
        html = 'building/general.html'
    elif pd['terrain']:
        form_terrain = FormTerrain(instance=pd['terrain'],label_suffix='')
        forms = {'terrain':form_terrain}
        json_dict['property_type'] = Building.TYPE_TERRENO
        json_dict['roles'] = pd['terrain'].roles
        html = 'terrain/general.html'

    json_dict['forms'] = forms
    json_dict['htmlBits'] = htmlBits

    return render(request,html,json_dict)

def ajax_add_rol_modal(request):

    form_add_rol = FormAddRol(label_suffix='')
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
    return render(request,'appraisal/modals_add_property_similar.html', pd)

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
        return render(request,'appraisal/realestate_value_similar_selected_terrains.html', pd)
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
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)
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
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)
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
        return render(request,'appraisal/realestate_value_similar_selected_buildings.html', pd)

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
    photo = appraisal.photos.get(id=request.GET['photo_id'])
    data['form'] = FormPhotos(initial={'category':photo.category,'description':photo.description})
    data['form'].fields['photos'].widget['initial_text'] = 'a'
    return render(request,'appraisal/modals_photo.html', data)

def ajax_photo_save(request):
    
    for photo_file in request.FILES.getlist('photos'):
        appraisal = Appraisal.objects.get(id=request.POST['appraisal_id'])
        photo = appraisal.photos.get(id=request.POST['photo_id'])
        photo.photo = photo_file
        photo.description = request.POST['description']
        photo.save()

    return render(request,'appraisal/annex_photo.html',{'photo':photo})
