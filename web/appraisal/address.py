from appraisal.data import propertyData

from .forms import FormEditAddress
from .forms import FormAddAddress
from .forms import FormAddProperty
from django.shortcuts import render
from building.models import Building
from commune.models import Commune
from realestate.models import RealEstate
from django.http import JsonResponse
from create import create

def ajax_add_address_modal(request):
    # Opens modal to add an address
    # Modal has a form, and needs the appraisal
    pd = propertyData(request.GET)
    real_estate = pd['appraisal'].real_estates.first()
    form_add_address = FormAddAddress(label_suffix='',
        initial={
            'addressNumber': real_estate.addressNumber,
            'addressStreet': real_estate.addressStreet,
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code })

    return render(request,'appraisal/modals/modal_add_address.html',
        {'appraisal':pd['appraisal'],'form_add_address':form_add_address})

def ajax_add_address(request):
    # Adding an address, from the add_address modal
    pd = propertyData(request.POST)
    commune = Commune.objects.get(code=request.POST['addressCommune'])
    real_estate, created = create.createOrGetRealEstate(
        addressNumber=request.POST['addressNumber'],
        addressStreet=request.POST['addressStreet'],
        addressCommune=commune,
        addressRegion=commune.region)
    print(real_estate)
    try:
        pd['appraisal'].real_estates.get(id=real_estate.id)
        # El real estate ya está en este appraisal
        return JsonResponse({'error':'La dirección especificada ya es parte de esta tasación'})
    except RealEstate.DoesNotExist:
        pd['appraisal'].real_estates.add(real_estate)
        pd['appraisal'].save()
        return render(request,'appraisal/properties/address_list.html', pd)

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

def ajax_remove_address(request):

    pd = propertyData(request.POST)
    pd['appraisal'].real_estates.remove(pd['real_estate'])
    pd['appraisal'].save()
    return JsonResponse({})

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
        return propertyListHTML(request,pd['appraisal'],pd['real_estate'])

def ajax_add_apartment_modal(request):

    pd = propertyData(request.GET)
    json_dict = {}
    json_dict['form_add_apartment'] = FormAddApartment()
    return render(request,'appraisal/modals_add_apartment.html', {**pd,**json_dict})

def ajax_add_apartment(request):

    pd = propertyData(request.POST)
    json_dict = {}
    pd['real_estate'].createOrGetDepartamento(pd['apartment_building'].addressNumber2,request.POST['addressNumber2'])
    return propertyListHTML(request,pd['appraisal'],pd['real_estate'])

def ajax_edit_property_modal(request):

    pd = propertyData(request.GET)

    app_ids = getAppraisedPropertyIds(pd['appraisal'])
    if pd['current'].propertyType in app_ids.keys():
        appraised = pd['current'].id in app_ids[pd['current'].propertyType]
    else:
        appraised = False

    json_dict = {}
    json_dict['form_edit_property'] = FormEditProperty(label_suffix='',
        initial={'addressNumber2': pd['current'].addressNumber2,'appraised':appraised})

    return render(request,'appraisal/modals_edit_property.html',{**json_dict,**pd})

def ajax_edit_property(request):

    pd = propertyData(request.POST)
    
    pd['current'].addressNumber2 = request.POST['addressNumber2']
    pd['current'].save()

    app_properties = getAppraisedProperties(pd['appraisal'])
    if pd['current'].propertyType in app_ids.keys():
        appraised = pd['current'].id in app_ids[pd['current'].propertyType]
    else:
        appraised = False
    if appraised and not 'appraised' in request.POST:
        pd['appraisal'].appproperty_set.remove()

    return propertyListHTML(request,pd['appraisal'],pd['real_estate'])
    
def ajax_remove_property(request):

    pd = propertyData(request.POST)
    if pd['apartment']:
        pd['apartment'].delete()
    elif pd['building']:
        pd['building'].delete()
    else:
        pd['current'].delete()
    return propertyListHTML(request,pd['appraisal'],pd['real_estate'])
    
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

def ajax_add_property_modal(request):
    
    pd = propertyData(request.GET)
    json_dict = {}

    real_estate = pd['appraisal'].real_estates.first()
    json_dict['form_add_property'] = FormAddProperty(label_suffix='',
        initial={
            'addressNumber': real_estate.addressNumber,
            'addressStreet': real_estate.addressStreet,
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code})

    json_dict['property_types'] = Building.propertyType_dict
    return render(request,'appraisal/modals/modal_add_property.html', {**pd,**json_dict})