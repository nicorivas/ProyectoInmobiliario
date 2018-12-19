from django.db import models
from commune.models import Commune
from region.models import Region
from neighborhood.models import Neighborhood
from terrain.models import Terrain
from building.models import Building
from house.models import House
from apartmentbuilding.models import ApartmentBuilding
from apartment.models import Apartment
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class Asset(models.Model):
    '''
    Any other asset, simply a name with value
    '''
    name = models.CharField("Nombre",max_length=300,default="",blank=True)
    value = models.FloatField("Valor en UF",blank=True,null=False,default=0)

class RealEstate(models.Model):
    '''
    Abstracción más general de un bien raíz.
    Collección de uno o más terrenos, y todo lo que está construido (o por construirse) sobre ellos.
    Definido únicamente por su dirección o por sus coordenadas.
    '''

    name = models.CharField("Nombre",
        max_length=200,
        default="",
        blank=True,
        null=True)

    addressStreet = models.CharField("Calle",
        max_length=300,
        blank=True,
        null=True)

    addressNumber = models.CharField("Número",
        max_length=30,
        blank=True,
        null=True)
    
    addressCommune = models.ForeignKey(Commune,
        verbose_name="Comuna",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        to_field='code')

    addressRegion = models.ForeignKey(Region,
        verbose_name="Región",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        to_field='code')

    addressFromCoords = models.BooleanField("Direccion por coordenadas",
        default=False)

    lat = models.FloatField("Latitud",
        default=0.0)
    
    lng = models.FloatField("Longitud",
        default=0.0)

    neighborhood = models.ForeignKey(Neighborhood,
        verbose_name="Barrio",
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    sourceUrl = models.URLField("Source url",
        max_length=1000,
        null=True,
        blank=True)

    sourceName = models.CharField("Source name",
        max_length=20,
        null=True,
        blank=True)

    sourceId = models.CharField("Source id",
        max_length=20,
        null=True,
        blank=True)

    sourceDatePublished = models.DateTimeField("Fecha publicación",
        blank=True,
        null=True)

    sourceAddedManually = models.BooleanField("Añadido manualmente",
        blank=True,
        null=False,
        default=False)

    marketPrice = models.DecimalField("Precio mercado UF",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)

    terrains = models.ManyToManyField(Terrain)

    buildings = models.ManyToManyField(Building)

    assets = models.ManyToManyField(Asset)

    BOOLEAN_NULL_CHOICES = (
        (1, "S/A"),
        (2, "Si"),
        (3, "No")
    )

    def createCasa(self,addressNumber2):
        building = Building(real_estate=self,propertyType=Building.TYPE_CASA)
        building.save()
        casa = House(building=building,addressNumber2=addressNumber2)
        casa.save()
        self.buildings.add(building)
        self.save()
        return casa

    def createDepartamento(self, addressNumber2):
        building = Building(real_estate=self, propertyType=Building.TYPE_DEPARTAMENTO)
        building.save()
        apartmentbuilding = ApartmentBuilding(building=building, fromApartment=True)
        apartmentbuilding.save()
        departamento = Apartment(apartment_building=apartmentbuilding ,addressNumber2=addressNumber2)
        departamento.save()
        self.buildings.add(building)
        self.save()
        return departamento

    def createOrGetCasa(self,addressNumber2=None):
        try:
            building = self.buildings.get(propertyType=Building.TYPE_CASA)
            try:
                if building.casa.addressNumber2 == addressNumber2:
                    return building.casa
                else:
                    return self.createCasa(addressNumber2)
            except ObjectDoesNotExist:
                # This should never take place
                return False
        except Building.DoesNotExist:
            return self.createCasa(addressNumber2)
        except MultipleObjectsReturned:
            buildings = self.buildings.filter(propertyType=Building.TYPE_CASA)
            for building in buildings:
                if building.casa.addressNumber2 == addressNumber2:
                    return building.casa
            return self.createCasa(addressNumber2)

    def createOrGetDepartamento(self,addressNumber2=None):
        try:
            building = self.buildings.get(propertyType=Building.TYPE_DEPARTAMENTO)
            try:
                if building.departamento.addressNumber2 == addressNumber2:
                    return building.departamento
                else:
                    return self.createDepartamento(addressNumber2)
            except ObjectDoesNotExist:
                # This should never take place
                return False
        except Building.DoesNotExist:
            return self.createDepartamento(addressNumber2)
        except MultipleObjectsReturned:
            buildings = self.buildings.filter(propertyType=Building.TYPE_DEPARTAMENTO)
            for building in buildings:
                if building.departamento.addressNumber2 == addressNumber2:
                    return building.departamento
            return self.createDepartamento(addressNumber2)

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
        return 1#int(self.propertyType == self.TYPE_DEPARTAMENTO)

    @property
    def is_house(self):
        return 1#int(self.propertyType == self.TYPE_CASA)

    @property
    def is_building(self):
        return 1#int(self.propertyType == self.TYPE_EDIFICIO)

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
    
