from django.db import models
from building.models import Building

class ApartmentBuilding(models.Model):
    '''
    An appartment building
    '''
    building = models.OneToOneField(Building,on_delete=models.CASCADE,verbose_name="Edificio",null=True,blank=False)

    marketPrice = models.DecimalField("Precio mercado",max_digits=10,decimal_places=2,null=True,blank=True)

    fromApartment = models.BooleanField("Creado desde departamento",default=False,null=False)