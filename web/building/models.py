from django.db import models
from neighborhood.models import Neighborhood

class Building(models.Model):

    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.PositiveSmallIntegerField("Numero",default=0)
    addressCommune = models.CharField("Comuna",max_length=300,default="")
    addressRegion = models.CharField("Region",max_length=300,default="")
    name = models.CharField("Nombre",max_length=100,default="",null=True,blank=True)
    lat = models.FloatField("Latitud",default=0.0)
    lon = models.FloatField("Longitud",default=0.0)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE,verbose_name="Barrio",blank=True,null=True)

    class Meta:
        app_label = 'building'

    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)
