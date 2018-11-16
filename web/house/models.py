from django.db import models
from neighborhood.models import Neighborhood
from commune.models import Commune
from region.models import Region
from realestate.models import RealEstate
import datetime

class House(RealEstate):

    addressNumber2 = models.TextField("Lote",max_length=10,null=True,blank=True)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    builtSquareMeters = models.DecimalField("Superficie construida",max_digits=7,decimal_places=2,null=True,blank=True)
    terrainSquareMeters = models.DecimalField("Superficie terreno",max_digits=7,decimal_places=2,null=True,blank=True)
    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    @property 
    def builtSquareMetersVerbose(self):
        if isinstance(self.builtSquareMeters,type(None)):
            return "-"
        else:
            return "{:10.1f}".format(self.builtSquareMeters)

    @property 
    def terrainSquareMetersVerbose(self):
        if isinstance(self.terrainSquareMeters,type(None)):
            return "-"
        else:
            return "{:10.1f}".format(self.terrainSquareMeters)

    @property
    def marketPricePerBuiltSquareMeters(self):
        if isinstance(self.builtSquareMeters,type(None)) or \
           isinstance(self.marketPrice,type(None)):
            return ""
        else:
            x = self.marketPrice/self.builtSquareMeters
            return "{:10.2f}".format(x)

    @property
    def marketPricePerTotalSquareMeters(self):
        if isinstance(self.builtSquareMeters,type(None)) or \
           isinstance(self.terrainSquareMeters,type(None)) or \
           isinstance(self.marketPrice,type(None)):
            return ""
        else:
            x = self.marketPrice/(self.builtSquareMeters+self.terrainSquareMeters)
            return "{:10.2f}".format(x)

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
