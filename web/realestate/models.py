from django.db import models
from commune.models import Commune
from region.models import Region
from neighborhood.models import Neighborhood


class Construction(models.Model):
    '''
    Parts of a RealEstate, such as balconies or other parts of a house.
    '''
    name = models.CharField("Nombre",max_length=300,default="",blank=True)
    
    complementary = models.BooleanField("Complementaria",blank=True,default=False)

    MATERIAL_UNKNOWN = '-'
    MATERIAL_ACERO = 'A'
    MATERIAL_HORMIGON = 'B'
    MATERIAL_ALBANILERIA = 'C'
    MATERIAL_PIEDRA_BLOQUE = 'D'
    MATERIAL_MADERA = 'E'
    MATERIAL_ADOBE = 'F'
    MATERIAL_METALCOM = 'G'
    MATERIAL_PREFAB_MADERA = 'H'
    MATERIAL_PREFAB_HORMIGON = 'I'
    MATERIAL_OTRO = 'J'
    MATERIAL_CHOICES = [
        (MATERIAL_UNKNOWN, "Desconocido"),
        (MATERIAL_ACERO, "Acero"),
        (MATERIAL_HORMIGON, "Hormigón"),
        (MATERIAL_ALBANILERIA, "Albañilería"),
        (MATERIAL_PIEDRA_BLOQUE, "Piedra/Bloque"),
        (MATERIAL_MADERA, "Madera"),
        (MATERIAL_ADOBE, "Adobe"),
        (MATERIAL_METALCOM, "Metalcom"),
        (MATERIAL_PREFAB_MADERA, "Prefab. Madera"),
        (MATERIAL_PREFAB_HORMIGON, "Prefab. Hormigón"),
        (MATERIAL_OTRO, "Otros")]
    material = models.CharField(
        max_length=2,
        choices=MATERIAL_CHOICES,
        default=MATERIAL_UNKNOWN)
    
    year = models.DateField("Año construcción",blank=True,null=False,default='1985-01-01')

    quality = models.IntegerField("Calidad",blank=True,null=True,choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])

    state = models.IntegerField("Estado",blank=True,null=True,choices=[(1,'Sin valor'),(2,'Malo'),(3,'Regular'),(4,'Bueno'),(5,'Muy bueno')])

    rol = models.CharField("Rol",max_length=20,blank=True,null=True)
    
    BOOLEAN_NULL_CHOICES = (
        (None, "S/A"),
        (True, "Si"),
        (False, "No")
    )
    prenda = models.BooleanField("Mercado objetivo",blank=True,null=True,choices=BOOLEAN_NULL_CHOICES)

    RECEPCION_CONRF = 0
    RECEPCION_SINRF = 1
    RECEPCION_SINPE = 2
    RECEPCION_SINANT = 3
    RECEPCION_NR = 4
    RECEPCION_CHOICES = [
        (RECEPCION_CONRF, "Con R/F"),
        (RECEPCION_SINRF, "Sin R/F"),
        (RECEPCION_SINPE, "Sin P/E"),
        (RECEPCION_SINANT, "Sin Ant."),
        (RECEPCION_NR, "N/R")]
    recepcion = models.IntegerField(
        choices=RECEPCION_CHOICES,
        default=RECEPCION_NR)

    area = models.FloatField("Area",
        blank=True,
        null=False,
        default=0)

    UFPerArea = models.FloatField("Area",
        blank=True,
        null=False,
        default=0)

class Terrain(models.Model):
    '''
    Parts of the terrain
    '''
    name = models.CharField("Nombre",max_length=300,default="",blank=True)

    frente = models.FloatField("Frente",blank=True,null=True)

    fondo = models.FloatField("Fondo",blank=True,null=True)

    TOPOGRAPHY_CHOICES = (
        (0, 'Plano'),
        (1, 'Semiplano'),
        (2, 'Pendiente'),
        (3, 'Pendiente abrupta')
    )
    topography = models.IntegerField("Topografía",choices=TOPOGRAPHY_CHOICES,blank=True,null=True)

    SHAPE_CHOICES = (
        (0, 'Regular'),
        (1, 'Irregular'),
    )
    shape = models.IntegerField("Forma",choices=SHAPE_CHOICES,blank=True,null=True)

    area = models.FloatField("Area",
        blank=True,
        null=False,
        default=0)

    rol = models.CharField("Rol",max_length=20,blank=True,null=True)

    UFPerArea = models.FloatField("UF per Area",
        blank=True,
        null=False,
        default=0)

class Asset(models.Model):
    '''
    Any other asset, simply a name with value
    '''
    name = models.CharField("Nombre",max_length=300,default="",blank=True)
    value = models.FloatField("Valor en UF",blank=True,null=False,default=0)

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

    addressStreet = models.CharField("Calle",max_length=300,default="",blank=True,)
    addressNumber = models.CharField("Número",max_length=10,default=0,blank=True,)
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

    constructions = models.ManyToManyField(Construction)

    terrains = models.ManyToManyField(Terrain)

    assets = models.ManyToManyField(Asset)

    BOOLEAN_NULL_CHOICES = (
        (1, "S/A"),
        (2, "Si"),
        (3, "No")
    )
    mercadoObjetivo = models.PositiveSmallIntegerField("Mercado objetivo",blank=True,null=False,default=1,choices=BOOLEAN_NULL_CHOICES)

    programa = models.CharField("Programa",max_length=10000,null=True,blank=True)

    estructuraTerminaciones = models.CharField("Estructura y terminaciones",max_length=10000,null=True,blank=True)

    anoConstruccion = models.IntegerField("Año construcción",
        blank=True,
        null=True)

    vidaUtilRemanente = models.IntegerField("Vida util remanente",
        blank=True,
        null=True)

    avaluoFiscal = models.FloatField("Avaluo fiscal",
        blank=True,
        null=True)

    dfl2 = models.PositiveSmallIntegerField("DFL 2",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    SELLO_VERDE_CHOICES = (
        ('V', 'Verde'),
        ('A', 'Amarillo'),
        ('R', 'Rojo'),
        ('NA', 'No Aplica'),
        ('VV', 'Verde vencido'),
        ('SA', 'Sin antecedentes')
    )
    selloVerde = models.CharField("Sello verde",
        max_length=2,
        choices=SELLO_VERDE_CHOICES,
        blank=True,
        null=True)

    copropiedadInmobiliaria = models.PositiveSmallIntegerField("Copropiedad Inmobiliaria",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    OCUPANTE_CHOICES = (
        ('P', 'Propietario'),
        ('A', 'Arrendatario'),
        ('O', 'Otro'),
        ('SO', 'Sin ocupante')
    )
    ocupante = models.CharField("Ocupante",
        max_length=2,
        choices=OCUPANTE_CHOICES,
        blank=True,
        null=True)

    tipoBien = models.CharField("Tipo de bien",
        max_length=20,
        blank=True,
        null=True)

    DESTINO_SII = (
        ('H', 'Habitacional'),
        ('O', 'Oficina'),
        ('C', 'Comercio'),
        ('I', 'Industria'),
        ('L', 'Bodega'),
        ('Z', 'Estacionamiento'),
        ('D', 'Deportes y Recreación'),
        ('E', 'Educación y Cultura'),
        ('G', 'Hotel, Motel'),
        ('P', 'Administración pública'),
        ('Q', 'Culto'),
        ('S', 'Salud')
    )
    destinoSII = models.CharField("Destino según SII",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    usoActual = models.CharField("Uso actual",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    usoFuturo = models.CharField("Uso futuro",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    permisoEdificacion = models.CharField("Permiso edificación",
        max_length=10,
        blank=True,
        null=True)
    permisoEdificacionDate = models.DateField("Permiso edificación fecha",
        blank=True,
        null=True)

    recepcionFinal = models.CharField("Recepcion final",
        max_length=10,
        blank=True,
        null=True)
    recepcionFinalDate = models.DateField("Recepcion final fecha",
        blank=True,
        null=True)

    expropiacion = models.PositiveSmallIntegerField("Expropiacion",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    viviendaSocial = models.PositiveSmallIntegerField("Vivienda social",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    desmontable = models.PositiveSmallIntegerField("Desmontable",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    adobe = models.PositiveSmallIntegerField("Adobe",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    acogidaLeyChoices = (
        (0, 'O.G.U. y C.'),
        (1, 'P.R.C.'),
        (2, 'Ley Pereira'),
        (3, 'Ley 19583'),
        (4, 'Ley 19667'),
        (5, 'Ley 19727'),
        (6, 'Ley 20251'),
        (7, 'Ley 6071'),
        (8, 'Ninguna'),
        (9, 'Antigüedad')
    )
    acogidaLey = models.IntegerField("Acogida a",
        choices=acogidaLeyChoices,
        blank=True,
        null=True)

    permisoEdificacionNo = models.CharField("Numero permiso edificacion",
        max_length=20,
        default=0,
        null=True)
    permisoEdificacionFecha = models.DateField("Fecha permiso edificacion",
        default='2006-10-25',
        null=True)
    permisoEdificacionSuperficie = models.DecimalField("Superficie permiso edificacion",
        max_digits=7,
        decimal_places=2,
        default=0,
        null=True)
    
    USE = (
        (0,'Usada'),
        (1,'Nueva')
    )
    tipoPropiedad = models.PositiveSmallIntegerField("Tipo de propiedad",
        choices=USE,
        default=0,
        null=True)

    antiguedad = models.PositiveSmallIntegerField("Antiguedad",
        default=0,
        null=True)

    vidaUtil = models.PositiveSmallIntegerField("Vida util",
        default=80,
        null=True)

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
        if self.propertyType == self.TYPE_HOUSE:
            if self.house.terrainSquareMeters != None and self.house.builtSquareMeters != None:
                return self.house.terrainSquareMeters + self.house.builtSquareMeters
            else:
                return 0
        elif self.propertyType == self.TYPE_APARTMENT:
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
        return int(self.propertyType == self.TYPE_APARTMENT)

    @property
    def is_house(self):
        return int(self.propertyType == self.TYPE_HOUSE)

    @property
    def is_building(self):
        return int(self.propertyType == self.TYPE_BUILDING)

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
        # Returns whole address in a nice format
        if self.addressCommune == None:
            return self.addressStreet+' '+str(self.addressNumber)
        else:
            return self.addressStreet+' '+str(self.addressNumber)+', '+self.addressCommune.name

    @property
    def addressShort(self):
        # Returns whole address in a nice format
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
    
