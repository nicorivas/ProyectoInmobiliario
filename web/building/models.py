from django.db import models
import datetime
from realestate.models import RealEstate
from neighborhood.models import Neighborhood
from commune.models import Commune
from region.models import Region

class Building(RealEstate):
    '''
    An appartment building
    '''
    fromApartment = models.BooleanField("Creado desde departamento",
        default=False,
        null=False)

    class Meta:
        app_label = 'building'
