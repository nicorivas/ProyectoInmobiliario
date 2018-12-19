from django.db import models
from building.models import Building

class ApartmentBuilding(models.Model):
    '''
    An appartment building
    '''
    building = models.OneToOneField(Building,on_delete=models.CASCADE,verbose_name="Edificio",null=True,blank=False)

    fromApartment = models.BooleanField("Creado desde departamento",default=False,null=False)