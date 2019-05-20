
from .forms import FormEditAddress
from .forms import FormAddAddress
from .forms import FormAddProperty
from django.shortcuts import render
from building.models import Building
from commune.models import Commune
from realestate.models import RealEstate
from django.http import JsonResponse
from create import create
from .forms import FormTerrain
from .forms import FormHouse
from .forms import FormBuilding
from .forms import FormApartment
from .views import getAppraisedProperties
from list.html_bits import *
from .data import getPropertyFromRequest, getAppraisalFromRequest

def ajax_load_sidebar(request):
    """
    Called when opening the tab.
    Returns the sidebar DOM.
    Via AJAX to be able to refresh when any property changes.
    """
    appraisal = getAppraisalFromRequest(request)
    app_properties = getAppraisedProperties(appraisal)
    json_dict = {}
    json_dict['app_properties'] = app_properties
    return render(request,'appraisal/properties/sidebar/properties_list.html',{**json_dict})

def ajax_add_property_modal(request):
    """
    Opens modal to add a property.
    It prefills the form for adding an address with the current address.
    """
    
    appraisal = getAppraisalFromRequest(request)
    json_dict = {}

    real_estate = appraisal.real_estates.first()
    json_dict['appraisal'] = appraisal
    json_dict['real_estate'] = real_estate
    json_dict['addressNumber'] = real_estate.addressNumber
    json_dict['addressStreet'] = real_estate.addressStreet
    json_dict['addressCommune'] = real_estate.addressCommune.name
    json_dict['addressRegion'] = real_estate.addressRegion.name
    json_dict['form_add_property'] = FormAddProperty(label_suffix='',
        initial={
            'addressNumber': real_estate.addressNumber,
            'addressStreet': real_estate.addressStreet,
            'addressCommune': real_estate.addressCommune.code,
            'addressRegion': real_estate.addressRegion.code})

    json_dict['property_types'] = Building.propertyType_dict
    return render(request,'appraisal/modals/modal_add_property.html', {**json_dict})

def ajax_add_property(request):
    """
    Submit the form of the add property modal.
    """

    print(request.POST)

    appraisal = getAppraisalFromRequest(request)
    pd = getPropertyFromRequest(request)

    prop, existed = pd['real_estate'].createOrGetProperty(
        int(request.POST['propertyType']),
        request.POST['addressNumber2'])

    print("ajax_add_property",prop.id)
    print("ajax_add_property",prop.propertyType)
    print(existed)

    if existed:
        return JsonResponse({'error':"La propiedad ya existe"})
    else:
        appprop = appraisal.addAppProperty(int(request.POST['propertyType']),prop.id)
        appraisal.save()
        return JsonResponse({'error':"Holi"})

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

    print(request.GET)

    appraisal = getAppraisalFromRequest(request)
    pd = getPropertyFromRequest(request)

    appraisal.removeAppProperty(pd["property"].propertyType,pd["property"].id)
    appraisal.save()

    return JsonResponse({})
    
def ajax_show_property(request):

    pd = getPropertyFromRequest(request)

    json_dict = {}

    if pd['property'].propertyType == Building.TYPE_DEPARTAMENTO:
        json_dict['apartment'] = pd['apartment']
        form_apartment = FormApartment(instance=pd['apartment'],label_suffix='')
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        forms = {'apartment':form_apartment,'building':form_building}
        json_dict['property_type'] = Building.TYPE_DEPARTAMENTO
        json_dict['roles'] = pd['property'].roles
        html = 'building/general.html'
    elif pd['property'].propertyType == Building.TYPE_EDIFICIO:
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        form_apartment_building = FormApartmentBuilding(instance=pd['apartment_building'],label_suffix='')
        forms = {'building':form_building,'apartment_building':form_apartment_building}
        json_dict['property_type'] = Building.TYPE_EDIFICIO
        json_dict['roles'] = pd['property'].roles
        html = 'building/general.html'
    elif pd['property'].propertyType == Building.TYPE_CASA:
        form_building = FormBuilding(instance=pd['building'],label_suffix='')
        form_house = FormHouse(instance=pd['property'],label_suffix='')
        forms = {'building':form_building,'house':form_house}
        json_dict['building'] = pd['building']
        json_dict['property_type'] = Building.TYPE_CASA
        json_dict['roles'] = pd['property'].roles
        html = 'building/general.html'
    elif pd['property'].propertyType == Building.TYPE_TERRENO:
        form_terrain = FormTerrain(instance=pd['property'],label_suffix='')
        forms = {'terrain':form_terrain}
        json_dict['property_type'] = Building.TYPE_TERRENO
        json_dict['roles'] = pd['property'].roles
        html = 'terrain/general.html'

    json_dict['forms'] = forms
    json_dict['htmlBits'] = htmlBits
    return render(request,html,json_dict)

def ajax_save_property(request):

    if request.POST['appraisal_id'] == '':
        return JsonResponse({})

    pd = getPropertyFromRequest(request)

    if pd['property'].propertyType == Building.TYPE_TERRENO:
        form_terrain = FormTerrain(request.POST,instance=pd['property'])
        form_terrain.save()

    if pd['property'].propertyType == Building.TYPE_CASA:
        form_house = FormHouse(request.POST,instance=pd['property'])
        form_house.save()

    if pd['property'].propertyType == Building.TYPE_EDIFICIO:
        form_building = FormBuilding(request.POST,instance=pd['property'])
        form_building.save()

    if pd['property'].propertyType == Building.TYPE_DEPARTAMENTO:
        form_apartment = FormApartment(request.POST,instance=pd['property'])
        form_apartment.save()

    return JsonResponse({})