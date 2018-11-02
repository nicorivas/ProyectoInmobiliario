from django.contrib.gis.db import models
from region.models import Region, RegionFull
from province.models import Province, ProvinceFull
from dbase.globals import *

class CommuneFull(models.Model):
    name = models.CharField("Nombre",max_length=100)
    code = models.PositiveSmallIntegerField("Code",
        null=False,
        blank=False,
        unique=True)
    region = models.ForeignKey(RegionFull,
        on_delete=models.CASCADE,
        verbose_name="Region",
        blank=False,
        null=False,
        to_field='code')
    province = models.ForeignKey(ProvinceFull,
        on_delete=models.CASCADE,
        verbose_name="Provincia",
        blank=False,
        null=False,
        to_field='code')
    mpoly = models.MultiPolygonField(null=True)

    # Number of apartments that are stored in this region
    dataApartmentCount = models.PositiveIntegerField("Departamentos",null=True,blank=True,default=0)
    # Number of houses that are stored in this region
    dataHouseCount = models.PositiveIntegerField("Casas",null=True,blank=True,default=0)
    # Number of buildings that are stored in this region
    dataBuildingCount = models.PositiveIntegerField("Edificios",null=True,blank=True,default=0)

    @property
    def shortName(self):
        return self.name

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField("Nombre",max_length=100)
    code = models.PositiveSmallIntegerField("Code",
        null=False,
        blank=False,
        unique=True)
    region = models.ForeignKey(Region,
        on_delete=models.CASCADE,
        verbose_name="Region",
        blank=False,
        null=False,
        to_field='code')
    province = models.ForeignKey(Province,
        on_delete=models.CASCADE,
        verbose_name="Provincia",
        blank=False,
        null=False,
        to_field='code')

    @property
    def shortName(self):
        return self.name

    def __str__(self):
        return self.name
