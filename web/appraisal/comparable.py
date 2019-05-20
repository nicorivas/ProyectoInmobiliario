from django.shortcuts import render
from list.html_bits import *
from .data import getPropertyFromRequest, getAppraisalFromRequest
from .forms import FormCreateProperty
from .forms import FormCreateTerrain
from .forms import FormCreateApartmentBuilding
from .forms import FormCreateApartment
from .forms import FormCreateHouse
from .forms import FormCreateAsset
from .forms import FormCreateRol
from .forms import FormCreateRealEstate
from building.models import Building
from commune.models import Commune
from realestate.models import RealEstate

def ajax_add_property_comparable_modal(request):

    appraisal = getAppraisalFromRequest(request)
    pd = getPropertyFromRequest(request)
    pd['form_real_estate'] = FormCreateRealEstate(label_suffix='')
    if pd['property'].propertyType == Building.TYPE_TERRENO:
        pd['form_property'] = FormCreateTerrain(label_suffix='')
    elif pd['property'].propertyType == Building.TYPE_CASA:
        pd['form_property'] = FormCreateHouse(label_suffix='')
    elif pd['property'].propertyType == Building.TYPE_DEPARTAMENTO:
        pd['form_property'] = FormCreateApartment(label_suffix='')
    elif pd['property'].propertyType == Building.TYPE_EDIFICIO:
        pd['form_property'] = FormCreateApartmentBuilding(label_suffix='')
    pd['htmlBits'] = htmlBits
    return render(request,'appraisal/modals_add_property_comparable.html', pd)

def ajax_add_property_comparable(request):

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

def ajax_edit_property_comparable_modal(request):
    
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

    return render(request,'appraisal/modals_add_property_comparable.html', pd)

def ajax_edit_property_comparable(request):

    pd = propertyData(request.POST)
    pd['form_real_estate'] = FormCreateRealEstate(request.POST,instance=pd['real_estate'])
    if pd['terrain']:
        pd['form_property'] = FormCreateTerrain(request.POST,instance=pd['terrain'])

    return render(request,'appraisal/modals_add_property_comparable.html', pd) 

def ajax_remove_property_comparable(request):

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