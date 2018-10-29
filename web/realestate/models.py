from django.db import models
from commune.models import Commune
from region.models import Region
from neighborhood.models import Neighborhood

class RealEstate(models.Model):
    ''' Topmost abstraction for all kinds of properties that can be valued'''
    ''' Bien raíz '''

    # more to be added
    TYPE_OTHER = 0
    TYPE_HOUSE = 1
    TYPE_APARTMENT = 2
    TYPE_BUILDING = 3
    propertyType_choices = [
        (TYPE_HOUSE, "Casa"),
        (TYPE_APARTMENT, "Departamento"),
        (TYPE_BUILDING, "Edificio"),
        (TYPE_OTHER, "Otro"),]
    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=TYPE_OTHER)
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
    addressFromCoords = models.BooleanField("Direccion por coordenadas",default=False)

    name = models.CharField("Nombre",max_length=200,default="",null=True,blank=True)
    lat = models.FloatField("Latitud",default=0.0)
    lng = models.FloatField("Longitud",default=0.0)
    neighborhood = models.ForeignKey(Neighborhood,
        on_delete=models.CASCADE,
        verbose_name="Barrio",
        blank=True,
        null=True)

    sourceUrl = models.URLField("Source url",null=True,blank=True)
    sourceName = models.CharField("Source name",max_length=20,null=True,blank=True)
    sourceId = models.CharField("Source id",max_length=20,null=True,blank=True)
    sourceDatePublished = models.DateTimeField("Fecha publicacion",blank=True,null=True)

    @property
    def address_dict(self):
        # Returns address fields as dictionary
        return {'street':self.addressStreet,'number':self.addressNumber,'commune':self.addressCommune.name,'region':self.addressRegion.shortName}

    @property
    def address(self):
        # Returns whole address in a nice format
        return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name+', '+self.addressRegion.shortName

    @property
    def addressShort(self):
        # Returns whole address in a nice format
        return self.addressStreet+' '+str(self.addressNumber)

    @property
    def latlng(self):
        # Returns whole address in a nice format
        return str(self.lat+33)[2:7]+', '+str(self.lng+70)[2:7]

    @ property
    def mapsUrl(self):
        return 'http://maps.google.com/maps?q='+str(self.lat)+','+str(self.lng)

    @property
    def get_propertyTypeName(self):
        if self.propertyType == self.TYPE_OTHER:
            return "other"
        elif self.propertyType == self.TYPE_HOUSE:
            return "house"
        elif self.propertyType == self.TYPE_APARTMENT:
            return "apartment"
        elif self.propertyType == self.TYPE_BUILDING:
            return "building"
        else:
            return None

    def get_propertyTypeIcon(self):
        if self.propertyType == self.TYPE_OTHER:
            return "far fa-times-circle"
        elif self.propertyType == self.TYPE_HOUSE:
            return "fas fa-home"
        elif self.propertyType == self.TYPE_APARTMENT:
            return "fas fa-building"
        elif self.propertyType == self.TYPE_BUILDING:
            return "fas fa-building"
        else:
            return "far fa-times-circle"
