from django.db import models
from commune.models import Commune
from region.models import Region
from neighborhood.models import Neighborhood

class RealEstate(models.Model):
    ''' Topmost abstraction for all kinds of properties that can be valued'''
    ''' Bien raíz '''

    # more to be added
    TYPE_UNDEFINED = 0
    TYPE_HOUSE = 1
    TYPE_APARTMENT = 2
    TYPE_BUILDING = 3
    propertyType_choices = [
        (TYPE_UNDEFINED, "Indefinido"),
        (TYPE_HOUSE, "Casa"),
        (TYPE_APARTMENT, "Departamento"),
        (TYPE_BUILDING, "Edificio")]
    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=TYPE_UNDEFINED)
    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.CharField("Numero",max_length=10,default=0)
    addressCommune = models.ForeignKey(Commune,
        on_delete=models.CASCADE,
        verbose_name="Comuna",
        blank=True,
        null=True,
        to_field='code')
    addressRegion = models.ForeignKey(Region,
        on_delete=models.CASCADE,
        verbose_name="Region",
        blank=True,
        null=True,
        to_field='code')

    name = models.CharField("Nombre",max_length=200,default="",null=True,blank=True)
    lat = models.FloatField("Latitud",default=0.0)
    lng = models.FloatField("Longitud",default=0.0)
    neighborhood = models.ForeignKey(Neighborhood,
        on_delete=models.CASCADE,
        verbose_name="Barrio",
        blank=True,
        null=True)

    @property
    def address(self):
        # Returns whole address in a nice format
        return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name+', '+self.addressRegion.name

    class Meta:
        abstract = True
