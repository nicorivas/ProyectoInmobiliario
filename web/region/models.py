from django.db import models
from dbase.globals import *

class RegionFull(models.Model):

    # Name of the region
    name = models.CharField("Nombre",max_length=100)
    # Short name of the region
    name_short = models.CharField("Nombre",max_length=100)
    # Code, as in numbers given by chilean state
    code = models.PositiveSmallIntegerField("Code",null=False,blank=False,unique=True)
    # International code
    iso = models.CharField("Iso",max_length=6,null=False,blank=False)
    # Polygon or set of polygons that specify the shape of the region
    #mpoly = models.MultiPolygonField(null=True)

    # Number of apartments that are stored in this region
    dataApartmentCount = models.PositiveIntegerField("Departamentos",null=True,blank=True,default=0)
    # Number of houses that are stored in this region
    dataHouseCount = models.PositiveIntegerField("Casas",null=True,blank=True,default=0)
    # Number of buildings that are stored in this region
    dataBuildingCount = models.PositiveIntegerField("Edificios",null=True,blank=True,default=0)
    
    @property
    def shortName(self):
        return self.name_short

    def __str__(self):
        return self.name_short

class Region(models.Model):

    # Name of the region
    name = models.CharField("Nombre",max_length=100)
    # Short name of the region
    name_short = models.CharField("Nombre",max_length=100)
    # Code, as in numbers given by chilean state
    code = models.PositiveSmallIntegerField("Code",null=False,blank=False,unique=True)
    # International code
    iso = models.CharField("Iso",max_length=6,null=False,blank=False)
    
    @property
    def short_name(self):
        return self.name_short

    def __str__(self):
        return self.name_short
