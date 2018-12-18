from django.db import models
from commune.models import Commune
from region.models import Region
from neighborhood.models import Neighborhood
from terrain.models import Terrain
from building.models import Building
from apartmentbuilding.models import ApartmentBuilding

class Asset(models.Model):
    '''
    Any other asset, simply a name with value
    '''
    name = models.CharField("Nombre",max_length=300,default="",blank=True)
    value = models.FloatField("Valor en UF",blank=True,null=False,default=0)

class RealEstate(models.Model):
    '''
    Abstracción más general de un bien raíz.
    Representa uno o más terrenos, y todo lo que está construido (o por construirse) sobre ellos.
    '''

    TYPE_NONE = ''
    TYPE_OTRO = 0
    TYPE_CASA = 1
    TYPE_DEPARTAMENTO = 2
    TYPE_OFICINA = 6
    TYPE_LOCAL_COMERCIAL = 7
    TYPE_TERRENO = 8
    TYPE_INDUSTRIA = 9
    TYPE_GALPON = 10
    TYPE_BODEGA = 11
    TYPE_ESTACIONAMIENTO = 12
    TYPE_EDIFICIO = 3
    TYPE_PARCELA = 13
    TYPE_BARCO = 14
    TYPE_VEHICULO = 15
    TYPE_MAQUINARIA = 16
    TYPE_ESTACION_DE_SERVICIO = 17
    TYPE_CONDOMINIO = 18
    propertyType_choices = [
        (TYPE_NONE,'---------'),
        (TYPE_CASA, "Casa"),
        (TYPE_DEPARTAMENTO, "Departamento"),
        (TYPE_OFICINA, "Oficina"),
        (TYPE_LOCAL_COMERCIAL, "Local Comercial"),
        (TYPE_TERRENO, "Terreno"),
        (TYPE_INDUSTRIA, "Industria"),
        (TYPE_GALPON, "Galpon"),
        (TYPE_BODEGA, "Bodega"),
        (TYPE_ESTACIONAMIENTO, "Estacionamiento"),
        (TYPE_EDIFICIO, "Edificio"),
        (TYPE_PARCELA, "Parcela"),
        (TYPE_BARCO, "Barco"),
        (TYPE_VEHICULO, "Vehiculo"),
        (TYPE_MAQUINARIA, "Maquinaria"),
        (TYPE_ESTACION_DE_SERVICIO, "Estación de Servicio"),
        (TYPE_CONDOMINIO, "Condominio"),
        (TYPE_OTRO, "Otro"),]
    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=TYPE_OTRO)

    addressStreet = models.CharField("Calle",max_length=300,default="",blank=True,)
    addressNumber = models.CharField("Número",max_length=30,default=0,blank=True,)
    addressCommune = models.ForeignKey(Commune,
        on_delete=models.CASCADE,
        verbose_name="Comuna",
        blank=True,
        null=True,
        to_field='code')
    addressRegion = models.ForeignKey(Region,
        on_delete=models.CASCADE,
        verbose_name="Región",
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

    sourceUrl = models.URLField("Source url",max_length=1000,null=True,blank=True)
    sourceName = models.CharField("Source name",max_length=20,null=True,blank=True)
    sourceId = models.CharField("Source id",max_length=20,null=True,blank=True)
    sourceDatePublished = models.DateTimeField("Fecha publicación",blank=True,null=True)
    sourceAddedManually = models.BooleanField("Añadido manualmente",blank=True,null=False,default=False)

    marketPrice = models.DecimalField("Precio mercado UF",max_digits=10,decimal_places=2,null=True,blank=True)

    terrains = models.ManyToManyField(Terrain)

    buildings = models.ManyToManyField(Building)

    assets = models.ManyToManyField(Asset)

    BOOLEAN_NULL_CHOICES = (
        (1, "S/A"),
        (2, "Si"),
        (3, "No")
    )

    def addBuilding(self, building, only_if_empty=False):
        if isinstance(building, Building):
            if only_if_empty:
                if len(self.buildings.all()) > 0:
                    return False
            self.buildings.add(building)
            self.save()
            return True
        elif isinstance(building, int):
            # Assuming its the building id.
            try:
                building = Building.objects.get(id=building)
                self.buildings.add(building)
                self.save()
                return True
            except Building.DoesNotExist:
                return False

    @property
    def sourceNameNice(self):
        "Returns source to be printed in a nice way."
        if self.sourceName == 'toctoc':
            return 'TocToc'
        elif self.sourceName == 'portali':
            return 'P.I.'
        elif self.sourceName == 'portalinmobiliario':
            return 'P.I.'
        else:
            return self.sourceName

    @property
    def total_area(self):
        if self.propertyType == self.TYPE_CASA:
            if self.house.terrainSquareMeters != None and self.house.builtSquareMeters != None:
                return self.house.terrainSquareMeters + self.house.builtSquareMeters
            else:
                return 0
        elif self.propertyType == self.TYPE_DEPARTAMENTO:
            if self.apartment.usefulSquareMeters != None and self.apartment.terraceSquareMeters != None:
                return self.apartment.usefulSquareMeters + self.apartment.terraceSquareMeters
            else:
                return 0

    @property
    def latlng(self):
        return [self.lat,self.lng]

    @property
    def latlng_verbose(self):
        return str(self.lat)+','+str(self.lng)

    @property
    def is_apartment(self):
        # Casting to int is done so that it also works when called in javascript.
        return int(self.propertyType == self.TYPE_DEPARTAMENTO)

    @property
    def is_house(self):
        return int(self.propertyType == self.TYPE_CASA)

    @property
    def is_building(self):
        return int(self.propertyType == self.TYPE_EDIFICIO)

    @property
    def address_dict(self):
        # Returns address fields as dictionary
        if self.addressCommune == None or self.addressRegion == None:
            return {}
        return {'street':self.addressStreet,'number':self.addressNumber,'commune':self.addressCommune.name,'region':self.addressRegion.shortName}

    @property
    def address(self):
        # Returns whole address in a nice format
        return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name+', '+self.addressRegion.shortName

    @property
    def addressVerboseNoRegion(self):
        if self.addressCommune == None:
            return self.addressStreet+' '+str(self.addressNumber)
        else:
            return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name

    @property
    def addressVerboseNoRegionNoCommune(self):
        return self.addressStreet+' '+str(self.addressNumber)

    @property
    def addressOrCoords(self):
        # Returns whole address in a nice format
        print('addressStreet',self.addressStreet)
        if self.addressStreet != '':
            return self.addressStreet+' '+str(self.addressNumber)
        else:
            return '('+self.latlng_verbose+')'

    @property
    def addressShort(self):
        return self.addressStreet+' '+str(self.addressNumber)

    @property
    def latlng_verbose_nice(self):
        # Returns whole address in a nice format
        return str(self.lat+33)[2:7]+', '+str(self.lng+70)[2:7]

    @ property
    def mapsUrl(self):
        return 'http://maps.google.com/maps?q='+str(self.lat)+','+str(self.lng)

    @property
    def get_propertyTypeName(self):
        if self.propertyType == self.TYPE_OTRO:
            return "other"
        elif self.propertyType == self.TYPE_CASA:
            return "house"
        elif self.propertyType == self.TYPE_DEPARTAMENTO:
            return "apartment"
        elif self.propertyType == self.TYPE_EDIFICIO:
            return "building"
        elif self.propertyType == self.TYPE_CONDOMINIO:
            return "condominium"
        else:
            return None

    def get_propertyTypeIcon(self):
        if self.propertyType == self.TYPE_OTRO:
            return "far fa-times-circle"
        elif self.propertyType == self.TYPE_CASA:
            return "fas fa-home"
        elif self.propertyType == self.TYPE_DEPARTAMENTO:
            return "fas fa-building"
        elif self.propertyType == self.TYPE_EDIFICIO:
            return "fas fa-city"
        elif self.propertyType == self.TYPE_CONDOMINIO:
            return "fas fa-torii-gate"
        else:
            return "far fa-times-circle"
    
