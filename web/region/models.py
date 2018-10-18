from django.contrib.gis.db import models

class Region(models.Model):

    # Name of the region
    name = models.CharField("Nombre",max_length=100)
    # Code, as in numbers given by chilean state
    code = models.PositiveSmallIntegerField("Code",null=False,blank=False,unique=True)
    # International code
    iso = models.CharField("Iso",max_length=6,null=False,blank=False)
    # Polygon or set of polygons that specify the shape of the region
    mpoly = models.MultiPolygonField(null=True)

    @property
    def shortName(self):
        return self.REGION_NAME__SHORT_NAME[self.name]

    def __str__(self):
        return self.name
