#!/usr/bin/env python
import sys
import os
import django
sys.path.append('/Users/nico/Code/tasador/web/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

from realestate.models import RealEstate
from building.models import Building
from apartmentbuilding.models import ApartmentBuilding

buildings = Building.objects.all()
realestate = RealEstate.objects.all()
n = len(buildings)
for i, building in enumerate(buildings):
	print(i,n)
	if i < 49800: continue
	real_estate = realestate.get(id=building.real_estate.id)
	if not real_estate.addBuilding(building,only_if_empty=True):
		print('Full')

'''
real_estates = RealEstate.objects.all()
for i, real_estate in enumerate(real_estates):
	print(i)
	if not real_estate.addApartmentBuilding(real_estate.id):
		print('failed',real_estate)
'''
'''
apartment_building = ApartmentBuilding.objects.all()
n = len(apartment_building)
for i, apartment_building in enumerate(apartment_building):
	print(i,n)
	building = Building.objects.get(id=apartment_building.id)
	apartment_building.building = building
'''
'''
real_estates = RealEstate.objects.all()
n = len(real_estates)
for i, real_estate in enumerate(real_estates):
	print(i,n)
	building = Building(
		propertyType=real_estate.propertyType,
		name=real_estate.name,
		marketPrice=real_estate.marketPrice,
		mercadoObjetivo=real_estate.mercadoObjetivo,
		programa=real_estate.programa,
		estructuraTerminaciones=real_estate.estructuraTerminaciones,
		anoConstruccion=real_estate.anoConstruccion,
		vidaUtilRemanente=real_estate.vidaUtilRemanente,
		avaluoFiscal=real_estate.avaluoFiscal,
		dfl2=real_estate.dfl2,
		selloVerde=real_estate.selloVerde,
		copropiedadInmobiliaria=real_estate.copropiedadInmobiliaria,
		ocupante=real_estate.ocupante,
		tipoBien=real_estate.tipoBien,
		destinoSII=real_estate.destinoSII,
		usoActual=real_estate.usoActual,
		usoFuturo=real_estate.usoFuturo,
		permisoEdificacionNo=real_estate.permisoEdificacionNo,
		permisoEdificacionFecha=real_estate.permisoEdificacionFecha,
		permisoEdificacionSuperficie=real_estate.permisoEdificacionSuperficie,
		recepcionFinalNo=real_estate.recepcionFinalNo,
		recepcionFinalFecha=real_estate.recepcionFinalFecha,
		expropiacion=real_estate.expropiacion,
		viviendaSocial=real_estate.viviendaSocial,
		desmontable=real_estate.desmontable,
		adobe=real_estate.adobe,
		acogidaLey=real_estate.acogidaLey,
		tipoPropiedad=real_estate.tipoPropiedad,
		antiguedad=real_estate.antiguedad,
		vidaUtil=real_estate.vidaUtil)
	building.real_estate = real_estate
	bid = building.save()
	real_estate.addBuilding(building)
	real_estate.save()
'''