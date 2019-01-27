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

    def createTerreno(self,addressNumber2):
        terrain = self.terrains.create(real_estate=self, addressNumber2=addressNumber2)
        self.save()
        return terrain

    def createCasa(self,addressNumber2):
        building = Building(real_estate=self, propertyType=Building.TYPE_CASA)
        building.save()
        casa = House(building=building, addressNumber2=addressNumber2)
        casa.save()
        self.buildings.add(building)
        self.save()
        return casa

    def createDepartamento(self, addressNumber2=None, addressNumber3=None, apartment_building=None):
        if apartment_building == None:
            if addressNumber2 == None:
                # Si no nos dieron número de edificio, crearlo
                building = Building(real_estate=self,propertyType=Building.TYPE_EDIFICIO)
                building.save()
                apartment_building = ApartmentBuilding(building=building, fromApartment=True)
                apartment_building.save()
            else:
                # Si nos dieron, 
                buildings = self.buildings.filter(propertyType=Building.TYPE_EDIFICIO)
                for building in buildings:
                    if building.apartmentbuilding.addressNumber2 == addressNumber2:
                        apartment_building = building.apartmentbuilding
                        break
    
        departamento = Apartment(apartment_building=apartment_building ,addressNumber2=addressNumber3)
        departamento.save()
        
        self.buildings.add(apartment_building.building)
        self.save()

        return departamento

    def createEdificio(self, addressNumber2):
        building = Building(real_estate=self, propertyType=Building.TYPE_EDIFICIO)
        building.save()
        apartment_building = ApartmentBuilding(building=building, addressNumber2=addressNumber2, fromApartment=False)
        apartment_building.save()
        self.buildings.add(building)
        self.save()
        return apartment_building

    def createCondominio(self, addressNumber2):
        building = Building(real_estate=self, propertyType=Building.TYPE_CONDOMINIO)
        building.save()
        self.buildings.add(building)
        self.save()
        return building

    def createOrGetTerreno(self,addressNumber2=None,if_exists_false=False):
        try:
            terrains = self.terrains.all()
            for terrain in terrains:
                if terrain.addressNumber2 == addressNumber2:
                    if if_exists_false:
                        return False
                    else:
                        return terrain, True
            return self.createTerreno(addressNumber2), False
        except Building.DoesNotExist:
            return self.createTerreno(addressNumber2), False

    def createOrGetTerrain(self,**kwargs):
        return self.createOrGetTerreno(**kwargs)

    def createOrGetCasa(self,addressNumber2=None,if_exists_false=False):
        try:
            buildings = self.buildings.filter(propertyType=Building.TYPE_CASA)
            for building in buildings:
                if building.house.addressNumber2 == addressNumber2:
                    if if_exists_false:
                        return False
                    else:
                        return building.house, True
            return self.createCasa(addressNumber2), False
        except Building.DoesNotExist:
            return self.createCasa(addressNumber2), False
    
    def createOrGetHouse(self,**kwargs):
        return self.createOrGetCasa(**kwargs)

    def createOrGetDepartamento(self,addressNumber2=None,addressNumber3=None,apartment_building=None):
        if apartment_building == None:
            if addressNumber2 == None:
                # Si el edificio no fue especificado, entonces tenemos que crear
                # una torre sí o sí, y el correspondiente departamento
                return self.createDepartamento(None,addressNumber3), False
            try:
                # Si el edificio fue especificado, entonces tenemos que encontrarlo...
                buildings = self.buildings.filter(propertyType=Building.TYPE_EDIFICIO)
                for building in buildings:
                    if building.apartmentbuilding.addressNumber2 == addressNumber2:
                        # ... y encontrar el departamento.
                        for apartment in building.apartmentbuilding.apartment_set.all():
                            if apartment.addressNumber2 == addressNumber3:
                                return apartment, True
                        return self.createDepartamento(addressNumber2,addressNumber3), False
                # Si fue especificado el edificio pero no lo encontramos, crear la torre
                # con el número que nos dieron, y el departamento.
                return self.createDepartamento(addressNumber2,addressNumber3), False
            except Building.DoesNotExist:
                # Si no hay niun edificio pero nos dieron un número, crear la torre
                # con el número que nos dieron, y el departamento.
                return self.createDepartamento(addressNumber2,addressNumber3), False
        else:
            for apartment in apartment_building.apartment_set.all():
                if apartment.addressNumber2 == addressNumber3:
                    return apartment, True
            return self.createDepartamento(apartment_building=apartment_building,addressNumber3=addressNumber3), False

    def createOrGetApartment(self,**kwargs):
        return self.createOrGetDepartamento(**kwargs)

    def createOrGetEdificio(self,addressNumber2=None,if_exists_false=False):
        try:
            buildings = self.buildings.filter(propertyType=Building.TYPE_EDIFICIO)
            for building in buildings:
                if building.apartmentbuilding.addressNumber2 == addressNumber2:
                    if if_exists_false:
                        return False
                    else:
                        return building.apartmentbuilding, True
            return self.createEdificio(addressNumber2), False
        except Building.DoesNotExist:
            return self.createEdificio(addressNumber2), False

    def createOrGetApartmentBuilding(self,**kwargs):
        return self.createOrGetEdificio(**kwargs)

    def createOrGetCondominio(self,addressNumber2=None):
        try:
            building = self.buildings.get(propertyType=Building.TYPE_CONDOMINIO)
            return building
        except Building.DoesNotExist:
            return self.createCondominio(addressNumber2)
        except MultipleObjectsReturned:
            buildings = self.buildings.filter(propertyType=Building.TYPE_CONDOMINIO)
            for building in buildings:
                if building.addressNumber2 == addressNumber2:
                    return building
            return self.createCondominio(addressNumber2)

    def addBuilding(self, building, only_if_empty=False):
        if isinstance(building, Building):
            if only_if_empty:
                if self.buildings.count() > 0:
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

    def createOrGetProperty(self, propertyType, addressNumber2,if_exists_false=False):
        if propertyType == Building.TYPE_EDIFICIO:
            return self.createOrGetEdificio(addressNumber2,if_exists_false=if_exists_false)
        elif propertyType == Building.TYPE_CASA:
            return self.createOrGetCasa(addressNumber2,if_exists_false=if_exists_false)
        elif propertyType == Building.TYPE_TERRENO:
            return self.createOrGetTerreno(addressNumber2,if_exists_false=if_exists_false)
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
        if self.propertyType == Building.TYPE_CASA:
            if self.buildings.first().house.terrainSquareMeters != None and self.buildings.first().house.builtSquareMeters != None:
                return self.buildings.first().house.terrainSquareMeters + self.buildings.first().house.builtSquareMeters
            else:
                return 0
        elif self.propertyType == Building.TYPE_DEPARTAMENTO:
            return 0
            '''
            if self.buildings.first().apartmentbuilding.apartment_set.first().usefulSquareMeters != None and self.apartment.terraceSquareMeters != None:
                return self.apartment.usefulSquareMeters + self.apartment.terraceSquareMeters
            else:
                return 0
            '''

    @property
    def latlng(self):
        return [self.lat,self.lng]

    @property
    def latlng_verbose(self):
        return str(self.lat)+','+str(self.lng)

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
    def address_no_region(self):
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
    def propertyType(self):
        if self.buildings.count() == 0:
            if self.terrains.count() == 0:
                return None
            else:
                return Terrain.TYPE_TERRAIN
        else:
            return self.buildings.first().propertyType

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
