from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal

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
    building,
    apartment,
    appraisal):

    def form_do_delete(form_building,form_apartment,form_appraisal):
        appraisal.delete()
        context = {}
        return render(request, 'appraisal/deleted.html',context)

    def form_do_save(form_building,form_apartment,form_appraisal):
        form_building.save()
        form_apartment.save()
        form_appraisal.save()
        print(form_appraisal)
        print('a')
        return

    def form_do_export(form_building,form_apartment,form_appraisal):

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir,'static/appraisal/test.xlsx')
        print(file_path)

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

    ret = None

    if form_building.is_valid() and \
       form_apartment.is_valid() and \
       form_appraisal.is_valid():
        if 'save' in request.POST:
            ret = form_do_save(form_building,form_apartment,form_appraisal)
        elif 'delete' in request.POST:
            ret = form_do_delete(form_building,form_apartment,form_appraisal)
        elif 'export' in request.POST:
            ret = form_do_export(form_building,form_apartment,form_appraisal)
    else:
        print(form_building.errors)
        print(form_apartment.errors)
        print(form_appraisal.errors)

    return ret

def appraisal(request,region="",commune="",street="",number="",id_b=0,
              numbera="",id_a=0,id_appraisal=0):
    '''
    '''
    print(request.POST.dict())
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
        form_building = AppraisalApartmentModelForm_Building(
            request.POST,
            instance=building)
        form_apartment = AppraisalApartmentModelForm_Apartment(
            request.POST,
            instance=apartment)
        form_appraisal = AppraisalApartmentModelForm_Appraisal(
            request.POST,
            instance=appraisal)
        ret = form_process(
            request,
            form_building,
            form_apartment,
            form_appraisal,
            building,
            apartment,
            appraisal
            )
        if isinstance(ret,HttpResponse): return ret

    form_building = AppraisalApartmentModelForm_Building(instance=building,label_suffix='')
    form_apartment = AppraisalApartmentModelForm_Apartment(instance=apartment,label_suffix='')
    form_appraisal = AppraisalApartmentModelForm_Appraisal(instance=appraisal,label_suffix='')

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

    print(building.permisoEdificacionDate)

    context = {
        'building': building,
        'apartment': apartment,
        'references': references,
        'averages': averages,
        'stds': stds,
        'form_apartment': form_apartment,
        'form_appraisal': form_appraisal,
        'form_building': form_building
        }

    return render(request, 'appraisal/apartment.html',context)

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
