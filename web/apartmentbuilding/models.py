from django.db import models
from building.models import Building

class ApartmentBuilding(models.Model):
	'''
	An appartment building
	'''
	building = models.OneToOneField(Building,on_delete=models.CASCADE,verbose_name="Edificio",null=True,blank=False)
	
	similar = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

	floors = models.PositiveSmallIntegerField("Pisos",null=True,blank=True)

	addressNumber2 = models.CharField("Dpto.",max_length=30,null=True,blank=True)
	
	marketPrice = models.DecimalField("Precio mercado",max_digits=10,decimal_places=2,null=True,blank=True)
	
	fromApartment = models.BooleanField("Creado desde departamento",default=False,null=False)

	generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

	builtSquareMeters = models.DecimalField("Superficie construida",max_digits=7,decimal_places=2,null=True,blank=True)

	@property
	def propertyType(self):
		return Building.TYPE_EDIFICIO

	@property
	def propertyTypeIcon(self):
		return "fas fa-city"
	