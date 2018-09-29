from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from realestate.models import RealEstate
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal
from appraisal.models import Comment

import reversion
from copy import deepcopy
from reversion.models import Version

import os
import csv

from .forms import AppraisalModelForm_Building
from .forms import AppraisalModelForm_Apartment
from .forms import AppraisalModelForm_Appraisal
from .forms import AppraisalForm_Comment
from .forms import AppraisalModelForm_House

from django.db.models import Avg, StdDev

import json

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import load_workbook

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

def get_house(request,id):
    '''
        Given building id, returns the building object.
        It checks for some errors and sends to the error page.
        TODO: Change this to proper try statements
    '''
    house = House.objects.filter(id=id)
    # This must be only one building
    if len(house) == 0:
        context = {'error_message': 'House should exist by now'}
        return render(request, 'appraisal/error.html',context)
    elif len(house) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'appraisal/error.html',context)
    house = house[0]
    return house

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
    try:
        appraisal = Appraisal.objects.get(pk=id)
        appraisal = appraisal
        return appraisal
    except Appraisal.DoesNotExist:
        context = {'error_message': 'Appraisal not found?'}
        return render(request, 'appraisal/error.html', context)
    except MultipleObjectsReturned:
        context = {'error_message': 'More than one appraisal of the same property'}
        return render(request, 'appraisal/error.html', context)


def form_process(
    request,
    form_comment,
    appraisal_old,
    appraisal,
    form_tasador_user,
    form_visador_user,
    form_building=None,
    form_apartment=None,
    form_appraisal=None,
    form_house=None,
    building=None,
    apartment=None,
    house=None):

    def form_do_delete(form_building=None,form_apartment=None,form_appraisal=None, form_house=None):
        appraisal.delete()
        context = {}
        return render(request, 'appraisal/deleted.html',context)

    def form_appraisal_save(comment=""):
        with reversion.create_revision():
            form_appraisal.save()
            reversion.set_user(request.user)
            reversion.set_comment(comment)

    def form_do_save(form_appraisal,appraisal_old, form_building=None,form_apartment=None,form_house=None,):
        if not form_house:
            form_building.save()
            form_apartment.save()
            form_appraisal.save()
        else:
            form_house.save()
        return

    def form_do_finish(appraisal,form_appraisal):
        appraisal.timeFinished = datetime.datetime.now()
        print('form do finish')
        print(appraisal.status)
        appraisal.status = 'f'
        appraisal.save()
        form_appraisal.save()
        return

    def form_do_export(form_building=None,form_apartment=None,form_appraisal=None, form_house=None):

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir,'static/appraisal/test.xlsx')

        def excel_find(workbook,term):
            for sheet in workbook:
                for row in range(1,100):
                    for col in range(1,100):
                       cv = sheet.cell(row=row,column=col).value
                       if cv == term:
                           print(row,col)

        def excel_find_replace(workbook,term,rep):
            for sheet in workbook:
                for row in range(1,100):
                    for col in range(1,100):
                       cv = sheet.cell(row=row,column=col).value
                       if cv == term:
                           sheet.cell(row=row,column=col).value = rep

        wb = load_workbook(filename=file_path)

        model_instance = form_appraisal.save(commit=False)

        fields = Appraisal._meta.get_fields()
        for field in fields:
            field_name = field.deconstruct()[0]
            excel_find_replace(wb,field_name,getattr(model_instance,field_name))

        response = HttpResponse(
            content=save_virtual_workbook(wb),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="somefilename.xlsx"'

        return response

    def form_do_assign_tasador(appraisal,user):
        appraisal.tasadorUser = user
        form_appraisal_save('Changed tasador')
        return

    def form_do_assign_visador(appraisal,user):
        appraisal.visadorUser = user
        form_appraisal_save('Changed tasador')
        return

    def form_do_comment(form_comment,appraisal):
        '''
        Create comment based on the field commentText of the form.
        '''
        text = form_comment.cleaned_data['commentText']
        comment = Comment(
            user=request.user,
            text=text,
            timeCreated=datetime.datetime.now(),
            appraisal=appraisal)
        comment.save()

    print('form process')

    ret = None
    if not house:
        if form_building.is_valid() and \
           form_apartment.is_valid() and \
           form_appraisal.is_valid() and \
           form_comment.is_valid():
            if 'save' in request.POST:
                ret = form_do_save(form_building,form_apartment,form_appraisal,appraisal_old)
            elif 'delete' in request.POST:
                ret = form_do_delete(form_building,form_apartment,form_appraisal)
            elif 'export' in request.POST:
                ret = form_do_export(form_building,form_apartment,form_appraisal)
            elif 'finish' in request.POST:
                ret = form_do_finish(appraisal,form_appraisal)
            elif 'assign_tasador' in request.POST:
                ret = form_do_assign_tasador(appraisal,form_tasador_user)
            elif 'assign_visador' in request.POST:
                ret = form_do_assign_visador(appraisal,form_visador_user)
            elif 'comment' in request.POST:
                ret = form_do_comment(form_comment,appraisal)

        else:
            print(form_building.errors)
            print(form_apartment.errors)
            print(form_appraisal.errors)
            print(form_comment.errors)
    else:
        if form_house.is_valid() and \
                form_appraisal.is_valid() and \
                form_comment.is_valid():
            if 'save' in request.POST:
                ret = form_do_save(form_house, form_appraisal, appraisal_old)
            elif 'delete' in request.POST:
                ret = form_do_delete(form_house)
            elif 'export' in request.POST:
                ret = form_do_export(form_house)
            elif 'finish' in request.POST:
                ret = form_do_finish(appraisal, form_appraisal)
            elif 'assign_tasador' in request.POST:
                ret = form_do_assign_tasador(appraisal, form_tasador_user)
            elif 'assign_visador' in request.POST:
                ret = form_do_assign_visador(appraisal, form_visador_user)
            elif 'comment' in request.POST:
                ret = form_do_comment(form_comment, appraisal)

        else:
            print(form_house.errors)

    return ret

def get_similar_realestate(realestate):

    if (realestate.bedrooms != None and
        realestate.bathrooms != None and
        realestate.builtSquareMeters != None and
        realestate.usefulSquareMeters != None):

        apartments = Apartment.objects.filter(
            bedrooms=apartment.bedrooms,
            bathrooms=apartment.bathrooms,
            marketPrice__isnull=False).exclude(marketPrice=0)

        ds = []
        ni = 0
        for i, apt in enumerate(apartments):
            d1 = float(pow(apartment.builtSquareMeters - apt.builtSquareMeters,2))
            d2 = float(pow(apartment.usefulSquareMeters - apt.usefulSquareMeters,2))
            ds.append([0,0])
            ds[i][0] = apt.pk
            ds[i][1] = d1+d2

        ds = sorted(ds, key=lambda x: x[1])
        ins = [x[0] for x in ds]

        references = apartments.filter(pk__in=ins[0:5])
        return references
    else:
        return []

def appraisal(request, **kwargs):
    '''
    General view for appraisals. Gets a variable number of parameters depending
    on the type of realestate.
    '''

    region = kwargs['region']
    commune = kwargs['commune']
    street = kwargs['street']
    number = kwargs['number']
    res_type = kwargs['res_type']
    if res_type == RealEstate.TYPE_APARTMENT:
        building_id = kwargs['building_id']
        apartment_number  = kwargs['apartment_number']
        apartment_id = kwargs['apartment_id']
    elif res_type == RealEstate.TYPE_HOUSE:
        house_id = kwargs['house_id']
    appraisal_id = kwargs['appraisal_id']

    # Get current appraisal
    appraisal = get_appraisal(request,appraisal_id)
    if isinstance(appraisal,HttpResponse): return appraisal

    realestate = None
    if res_type == RealEstate.TYPE_APARTMENT:
        # Get current flat
        realestate = get_apartment(request,apartment_id)
        if isinstance(realestate,HttpResponse): return realestate
    elif res_type == RealEstate.TYPE_HOUSE:
        # Get current house
        realestate = get_house(request,house_id)
        if isinstance(realestate,HttpResponse): return realestate
    if realestate == None:
        context = {'error_message': 'Realestae was not found'}
        return render(request, 'appraisal/error.html',context)

    appraisal_old = deepcopy(appraisal)

    # DA FORM

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # Main forms
        form_appraisal = AppraisalModelForm_Appraisal(
            request.POST,
            instance=appraisal)
        form_comment = AppraisalForm_Comment(request.POST)
        if res_type == RealEstate.TYPE_APARTMENT:
            form_apartment = AppraisalModelForm_Apartment(
                request.POST,
                instance=realestate)
            form_building = AppraisalModelForm_Building(
                request.POST,
                instance=realestate.building)
        elif res_type == RealEstate.TYPE_HOUSE:
            '''
            form_house = AppraisalModelForm_House(
                request.POST,
                instance=realestate
            )
            '''

        # Other options of the form:
        # Assigning tasadores
        tasadorUser = None
        if 'tasador' in request.POST.dict().keys():
            tasadorUserId = request.POST.dict()['tasador']
            tasadorUser = User.objects.get(pk=tasadorUserId)

        visadorUser = None
        if 'visador' in request.POST.dict().keys():
            visadorUserId = request.POST.dict()['visador']
            visadorUser = User.objects.get(pk=visadorUserId)

        if not form_house:
            ret = form_process(
                request,
                form_building,
                form_apartment,
                form_appraisal,
                form_comment,
                appraisal_old,
                realestate.building,
                realestate,
                appraisal,
                tasadorUser,
                visadorUser)
        else:
            ret = form_process(
                request,
                form_house,
                form_appraisal,
                form_comment,
                appraisal_old,
                realestate.building,
                realestate,
                appraisal,
                tasadorUser,
                visadorUser)


        if isinstance(ret, HttpResponse): return ret

    # REFERENCE PROPERTIES
    references = get_similar_realestate(realestate)

    if len(references) > 0:
        averages = references.aggregate(
            Avg('marketPrice'),
            Avg('builtSquareMeters'),
            Avg('usefulSquareMeters'))
        stds = references.aggregate(
            StdDev('marketPrice'),
            StdDev('builtSquareMeters'),
            StdDev('usefulSquareMeters'))
    else:
        averages = []
        stds = []

    # Visadores and tasadores for the Bootstrap modals where you can select
    # them.
    tasadores = User.objects.filter(groups__name__in=['tasador'])
    visadores = User.objects.filter(groups__name__in=['visador'])

    # History of changes, for the logbook
    versions = list(Version.objects.get_for_object(appraisal))
    appraisal_history = []
    c = 0
    for i in range(len(versions)):
        if i == 0: continue
        version_new = versions[i]
        version_old = versions[i-1]

        appraisal_history.append({})
        appraisal_history[c]['user'] = version_new.revision.user
        appraisal_history[c]['time'] = version_new.revision.date_created
        appraisal_history[c]['diffs'] = []
        for key, value in version_new.field_dict.items():
            if value != version_old.field_dict[key]:
                appraisal_history[c]['diffs'].append([key,value,version_old.field_dict[key]])
        if len(appraisal_history[c]['diffs']) == 0:
            appraisal_history.pop(c)
        else:
            c += 1

    # Comments, for the logbook
    comments = Comment.objects.filter(appraisal=appraisal)

    # Forms
    forms = {
        'appraisal': AppraisalModelForm_Appraisal(instance=appraisal,label_suffix=''),
        'comment':AppraisalForm_Comment(label_suffix='')}
    if res_type == RealEstate.TYPE_APARTMENT:
        forms['apartment'] = AppraisalModelForm_Apartment(instance=realestate,label_suffix='')
        forms['building'] = AppraisalModelForm_Building(instance=realestate.building,label_suffix='')
    elif res_type == RealEstate.TYPE_HOUSE:
        '''
        forms['house'] = AppraisalModelForm_House(instance=realestate,label_suffix='')
        '''

    # Disable fields if appraisal is finished
    if appraisal.status == appraisal.STATE_FINISHED:
        for form in forms:
            for field in form.fields:
                form.fields[field].widget.attrs['readonly'] = True
                form.fields[field].widget.attrs['disabled'] = True

    context = {
        'appraisal':appraisal,
        'forms':forms,
        'realestate': realestate,
        'references': references,
        'averages': averages,
        'stds': stds,
        'tasadores':tasadores,
        'visadores':visadores,
        'appraisal_history': appraisal_history,
        'comments': comments,
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
