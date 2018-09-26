from django.db import models
import datetime
from realestate.models import RealEstate
from neighborhood.models import Neighborhood
from commune.models import Commune
from region.models import Region

class Building(RealEstate):
    '''
    An appartment building
    '''

    sourceName = models.CharField("Source name",max_length=20,null=True,blank=True)
    sourceUrl = models.URLField("Source url",null=True,blank=True)

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
        null=True)
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
        null=True)
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
        max_length=20,
        blank=True,
        null=True)
    usoFuturo = models.CharField("Uso futuro",
        max_length=20,
        blank=True,
        null=True)
    permisoEdificacion = models.IntegerField("Permiso edificación",
        blank=True,
        null=True)
    permisoEdificacionDate = models.DateField("Permiso edificación fecha",
        blank=True,
        null=True)
    recepcionFinal = models.IntegerField("Recepcion final",
        blank=True,
        null=True)
    recepcionFinalDate = models.DateField("Recepcion final fecha",
        blank=True,
        null=True)
    expropiacion = models.BooleanField("Expropiacion",
        blank=True,
        null=True)
    viviendaSocial = models.BooleanField("Vivienda social",
        blank=True,
        null=True)
        
    class Meta:
        app_label = 'building'

    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)
