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

    fromApartment = models.BooleanField("Creado desde departamento",
        default=False,
        null=False)
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
        null=True)
    viviendaSocial = models.BooleanField("Vivienda social",
        blank=True,
        null=True)
    desmontable = models.BooleanField("Desmontable",
        blank=True,
        null=True)
    adobe = models.BooleanField("Adobe",
        blank=True,
        null=True)
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

    class Meta:
        app_label = 'building'
