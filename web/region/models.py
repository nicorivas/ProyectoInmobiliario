from django.contrib.gis.db import models

class Region(models.Model):
    name = models.CharField("Nombre",max_length=100)
    code = models.PositiveSmallIntegerField("Code",null=False,blank=False,unique=True)
    iso = models.CharField("Iso",max_length=6,null=False,blank=False)
    mpoly = models.MultiPolygonField(null=True)
