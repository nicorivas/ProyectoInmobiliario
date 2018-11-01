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

    marketPrice = models.DecimalField("Precio mercado UF",max_digits=10,decimal_places=2,null=True,blank=True)


    BOOLEAN_NULL_CHOICES = (
        (None, "S/A"),
        (True, "Si"),
        (False, "No")
    )
    mercadoObjetivo = models.BooleanField("Mercado objetivo",blank=True,null=True,choices=BOOLEAN_NULL_CHOICES)


    BOOLEAN_NULL_CHOICES = (
        (None, "S/A"),
        (True, "Si"),
        (False, "No")
    )
    anoConstruccion = models.IntegerField("Año construccion",
        blank=True,
        null=True)
    vidaUtilRemanente = models.IntegerField("Vida util remanente",
        blank=True,
        null=True)
    avaluoFiscal = models.FloatField("Avaluo fiscal",
        blank=True,
        null=True)
    dfl2 = models.BooleanField("DFL 2",
        blank=True,
        null=True,
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
    copropiedadInmobiliaria = models.BooleanField("Copropiedad Inmobiliaria",
        blank=True,
        null=True,
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
    expropiacion = models.BooleanField("Expropiacion",
        blank=True,
        null=True,
        choices=BOOLEAN_NULL_CHOICES)
    viviendaSocial = models.BooleanField("Vivienda social",
        blank=True,
        null=True,
        choices=BOOLEAN_NULL_CHOICES)
    desmontable = models.BooleanField("Desmontable",
        blank=True,
        null=True,
        choices=BOOLEAN_NULL_CHOICES)
    adobe = models.BooleanField("Adobe",
        blank=True,
        null=True,
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
