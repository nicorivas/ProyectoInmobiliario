from django.db import models
from neighborhood.models import Neighborhood
from commune.models import Commune
from region.models import Region
from realestate.models import RealEstate
import datetime

class House(RealEstate):

    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    terrainSquareMeters = models.DecimalField("Superficie terreno",max_digits=7,decimal_places=2,null=True,blank=True)
    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)

    def __init__(self, *args, **kwargs):
        super(House, self).__init__(*args,**kwargs)
        self.propertyType=RealEstate.TYPE_HOUSE
