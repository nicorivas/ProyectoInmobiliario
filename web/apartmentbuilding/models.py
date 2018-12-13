from django.db import models

class ApartmentBuilding(models.Model):
    '''
    An appartment building
    '''
    fromApartment = models.BooleanField("Creado desde departamento",default=False,null=False)