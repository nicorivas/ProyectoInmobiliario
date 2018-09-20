from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal

import reversion
from copy import deepcopy
from reversion.models import Version

import os
import csv

from .forms import AppraisalApartmentModelForm_Building
from .forms import AppraisalApartmentModelForm_Apartment
from .forms import AppraisalApartmentModelForm_Appraisal

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

def form_process(
    request,
    form_building,
    form_apartment,
    form_appraisal,
    appraisal_old,
    building,
    apartment,
    appraisal,
    form_tasador_user):

    def form_do_delete(form_building,form_apartment,form_appraisal):
        appraisal.delete()
        context = {}
        return render(request, 'appraisal/deleted.html',context)

    def form_do_save(form_building,form_apartment,form_appraisal,appraisal_old):
        form_building.save()
        form_apartment.save()
        with reversion.create_revision():
            form_appraisal.save()
            reversion.set_user(request.user)
            reversion.set_comment("Created revision 1")
        return

    def form_do_export(form_building,form_apartment,form_appraisal):

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
        print('form_do_assign_tasador',form_tasador_user)
        print(appraisal.tasadorUser)
        appraisal.tasadorUser = user
        print(appraisal.tasadorUser)
        appraisal.save()
        return

    ret = None

    if form_building.is_valid() and \
       form_apartment.is_valid() and \
       form_appraisal.is_valid():
        if 'save' in request.POST:
            ret = form_do_save(form_building,form_apartment,form_appraisal,appraisal_old)
        elif 'delete' in request.POST:
            ret = form_do_delete(form_building,form_apartment,form_appraisal)
        elif 'export' in request.POST:
            ret = form_do_export(form_building,form_apartment,form_appraisal)
        elif 'assign_tasador' in request.POST:
            ret = form_do_assign_tasador(appraisal,form_tasador_user)
    else:
        print(form_building.errors)
        print(form_apartment.errors)
        print(form_appraisal.errors)

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

    appraisal_old = deepcopy(appraisal)

    # DA FORM

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # Main forms
        form_building = AppraisalApartmentModelForm_Building(
            request.POST,
            instance=building)
        form_apartment = AppraisalApartmentModelForm_Apartment(
            request.POST,
            instance=apartment)
        form_appraisal = AppraisalApartmentModelForm_Appraisal(
            request.POST,
            instance=appraisal)

        # Other options of the form:
        # For assigning tasadores
        tasadorUser = None
        if 'tasador' in request.POST.dict().keys():
            tasadorUserId = request.POST.dict()['tasador']
            tasadorUser = User.objects.get(pk=tasadorUserId)

        ret = form_process(
            request,
            form_building,
            form_apartment,
            form_appraisal,
            appraisal_old,
            building,
            apartment,
            appraisal,
            tasadorUser
            )
        if isinstance(ret, HttpResponse): return ret

    form_building = AppraisalApartmentModelForm_Building(instance=building, label_suffix='')
    form_apartment = AppraisalApartmentModelForm_Apartment(instance=apartment, label_suffix='')
    form_appraisal = AppraisalApartmentModelForm_Appraisal(instance=appraisal, label_suffix='')

    # REFERENCE PROPERTIES
    # Do we have enough data to compare?
    references = []
    if (apartment.bedrooms != None and
        apartment.bathrooms != None and
        apartment.builtSquareMeters != None and
        apartment.usefulSquareMeters != None):

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

    context = {
        'building': building,
        'apartment': apartment,
        'references': references,
        'averages': averages,
        'stds': stds,
        'tasadores':tasadores,
        'visadores':visadores,
        'form_apartment': form_apartment,
        'form_appraisal': form_appraisal,
        'form_building': form_building,
        'appraisal_history': appraisal_history,
        }

    a = render(request, 'appraisal/apartment.html',context)
    return a

def ajax_computeValuations(request):
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
