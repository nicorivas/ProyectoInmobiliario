from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from realestate.models import RealEstate, Asset
#from house.models import House
from building.models import Building
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
from .forms import FormBuilding
from .forms import FormApartment
from .forms import FormHouse
from .forms import FormAppraisal
from .forms import FormComment
from .forms import FormPhotos
from .forms import FormDocuments
from .forms import FormEditAddress
from .forms import FormAddAddress
from .forms import FormAddProperty
from .forms import FormEditProperty
from .forms import FormAddApartment
from .forms import FormCreateApartment
from .forms import FormCreateHouse
#from .forms import FormCreateConstruction
from .forms import FormCreateTerrain
from .forms import FormCreateAsset
from .forms import FormCreateRol
from create import create

import viz.maps as maps
import appraisal.related as related
from appraisal.export import *
from dbase.globals import *

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

    htmlBits = {
        'unitUF':'<small>(U.F.)</small>',
        'unitPesos':'<small>($)</small>',
        'unitMeter':'<small>(m)</small>',
        'unitUFPerSquaredMeter':'<small>(U.F./m<sup>2</sup>)</small>',
        'unitPesosPerSquaredMeter':'<small>($/m<sup>2</sup>)</small>',
        'unitSquaredMeter':'<small>(m<sup>2</sup>)</small>'}

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

    a = render(request, 'appraisal/realestate_appraisal.html', context)
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

def ajax_edit_address_modal(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    form_edit_address = FormEditAddress(label_suffix='',
        initial={
            'addressNumber': real_estate.addressNumber,
            'addressStreet': real_estate.addressStreet,
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code })

    return render(request,'appraisal/modals_edit_address.html',
        {'appraisal':appraisal,'real_estate':real_estate,'form_edit_address':form_edit_address})

def ajax_add_address_modal(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate = appraisal.real_estates.first()

    form_add_address = FormAddAddress(label_suffix='',
        initial={
            'addressNumber': '',
            'addressStreet': '',
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code })

    return render(request,'appraisal/modals_add_address.html',
        {'appraisal':appraisal,'form_add_address':form_add_address})

def ajax_remove_address_modal(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    return render(request,'appraisal/modals_remove_address.html', {'appraisal':appraisal,'real_estate':real_estate})

def ajax_edit_address(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    commune = Commune.objects.get(code=request.POST['addressCommune'])

    # Check if there is already a real estate with this address
    try:
        real_estate = appraisal.real_estates.get(
            addressNumber=request.POST['addressNumber'],
            addressStreet=request.POST['addressStreet'],
            addressCommune=commune,
            addressRegion=commune.region)
        return JsonResponse({'error':'La dirección especificada ya es parte de esta tasación'})
    except RealEstate.DoesNotExist:
        real_estate.addressNumber = request.POST['addressNumber']
        real_estate.addressStreet = request.POST['addressStreet']
        real_estate.addressCommune = commune
        real_estate.addressRegion = commune.region
        real_estate.save()
        return JsonResponse({'address':real_estate.address})

def ajax_add_address(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    commune = Commune.objects.get(code=request.POST['addressCommune'])

    real_estate = create.createOrGetRealEstate(
        addressNumber=request.POST['addressNumber'],
        addressStreet=request.POST['addressStreet'],
        addressCommune=commune,
        addressRegion=commune.region)

    try:
        appraisal.real_estates.get(id=real_estate.id)
        # El real estate ya está en este appraisal
        return JsonResponse({'error':'La dirección especificada ya es parte de esta tasación'})
    except RealEstate.DoesNotExist:
        appraisal.real_estates.add(real_estate)
        appraisal.save()
        return render(request,'appraisal/address_list.html', {'appraisal':appraisal})

def ajax_remove_address(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    appraisal.real_estates.remove(real_estate)
    appraisal.save()

    return JsonResponse({})

def ajax_load_realestate(request):

    print('ajax_load_realestate')

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    print('appraisal_id',appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)
    print('real_estate_id',real_estate_id)

    buildings = real_estate.buildings.all()

    return render(request,'appraisal/property_list.html',{'buildings':buildings,'real_estate':real_estate})

def ajax_add_property_modal(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    form_add_property = FormAddProperty()

    return render(request,'appraisal/modals_add_property.html', 
        {'appraisal':appraisal,'real_estate':real_estate,'form_add_property':form_add_property})

def ajax_add_property(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    prop = real_estate.createOrGetProperty(
        int(request.POST['propertyType']),
        request.POST['addressNumber2'],
        if_exists_false=True)

    if isinstance(prop,type(True)):
        if not prop:
            return JsonResponse({'error':"La propiedad ya existe"})
    else:
        buildings = real_estate.buildings.all()
        return render(request,'appraisal/property_list.html',{'buildings':buildings,'real_estate':real_estate})

def ajax_add_apartment_modal(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.GET['building_id'])
    building = real_estate.buildings.get(id=building_id)

    form_add_apartment = FormAddApartment()

    return render(request,'appraisal/modals_add_apartment.html', 
        {'appraisal':appraisal,'real_estate':real_estate,'building':building,'form_add_apartment':form_add_apartment})

def ajax_add_apartment(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.POST['building_id'])
    building = real_estate.buildings.get(id=building_id)

    real_estate.createOrGetDepartamento(building.apartmentbuilding.addressNumber2,request.POST['addressNumber2'])
    
    buildings = real_estate.buildings.all()
    return render(request,'appraisal/property_list.html',{'buildings':buildings,'real_estate':real_estate})

def ajax_edit_property_modal(request):

    print(request)

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.GET['building_id'])
    building = real_estate.buildings.get(id=building_id)

    if building.propertyType == Building.TYPE_CASA:

        form_edit_property = FormEditProperty(label_suffix='',
            initial={'addressNumber2': building.house.addressNumber2})

        return render(request,'appraisal/modals_edit_property.html',{
                'appraisal':appraisal,
                'real_estate':real_estate,
                'building':building,
                'form_edit_property':form_edit_property})

    elif building.propertyType == Building.TYPE_EDIFICIO:

        if 'apartment_id' in request.GET:
            apartment_id = int(request.GET['apartment_id'])
            apartment = building.apartmentbuilding.apartment_set.get(id=apartment_id)
            form_edit_property = FormEditProperty(label_suffix='',
                initial={'addressNumber2': apartment.addressNumber2})
            return render(request,'appraisal/modals_edit_property.html',{
                'appraisal':appraisal,
                'real_estate':real_estate,
                'building':building,
                'apartment':apartment,
                'form_edit_property':form_edit_property})
        else:
            form_edit_property = FormEditProperty(label_suffix='',
                initial={'addressNumber2': building.apartmentbuilding.addressNumber2})
            return render(request,'appraisal/modals_edit_property.html',{
                'appraisal':appraisal,
                'real_estate':real_estate,
                'building':building,
                'form_edit_property':form_edit_property})

def ajax_edit_property(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.POST['building_id'])
    building = real_estate.buildings.get(id=building_id)

    if building.propertyType == Building.TYPE_CASA:
        building.house.addressNumber2 = request.POST['addressNumber2']
        building.house.save()
    elif building.propertyType == Building.TYPE_EDIFICIO:
        if 'apartment_id' in request.POST:
            apartment_id = int(request.POST['apartment_id'])
            apartment = building.apartmentbuilding.apartment_set.get(id=apartment_id)
            apartment.addressNumber2 = request.POST['addressNumber2']
            apartment.save()
        else:
            building.apartmentbuilding.addressNumber2 = request.POST['addressNumber2']
            building.apartmentbuilding.save()
    
    buildings = real_estate.buildings.all()
    return render(request,'appraisal/property_list.html',{'buildings':buildings,'real_estate':real_estate})

def ajax_remove_property(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.POST['building_id'])
    building = real_estate.buildings.get(id=building_id)

    if 'apartment_id' in request.POST:
        apartment_id = int(request.POST['apartment_id'])
        apartment = building.apartmentbuilding.apartment_set.get(id=apartment_id)
        apartment.delete()
    else:
        building.delete()
    
    buildings = real_estate.buildings.all()
    return render(request,'appraisal/property_list.html',{'buildings':buildings,'real_estate':real_estate})

def ajax_show_property(request):

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.GET['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.GET['building_id'])
    building = real_estate.buildings.get(id=building_id)

    if building.is_apartmentbuilding:
    
        if int(request.GET['apartment_id']) != -1:
            # DEPARTAMENTO
            apartment_id = int(request.GET['apartment_id'])
            apartment = building.apartmentbuilding.apartment_set.get(id=apartment_id)
            form_apartment = FormApartment(instance=apartment,label_suffix='')
            form_building = FormBuilding(instance=building,label_suffix='')
            forms = {
                'apartment':form_apartment,
                'building':form_building}
            return render(request,'apartment/general.html', {'forms':forms})
        else:
            form_building = FormBuilding(instance=building,label_suffix='')
            forms = {
                'building':form_building}
            return render(request,'apartmentbuilding/general.html', {'forms':forms})

    if building.is_house:

        form_house = FormHouse(instance=building.house,label_suffix='')
        forms = {'house':form_house}

        return render(request,'house/general.html', {'forms':forms})

def ajax_save_property(request):

    if request.POST['appraisal_id'] == '':
        return JsonResponse({})

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    real_estate_id = int(request.POST['real_estate_id'])
    real_estate = appraisal.real_estates.get(id=real_estate_id)

    building_id = int(request.POST['building_id'])
    building = real_estate.buildings.get(id=building_id)

    form_building = FormBuilding(request.POST,instance=building)
    form_building.save()

    apartment_id = int(request.POST['apartment_id'])
    apartment = building.apartmentbuilding.apartment_set.get(id=apartment_id)

    form_apartment = FormApartment(request.POST,instance=apartment)
    form_apartment.save()

    return JsonResponse({})