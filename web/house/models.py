from django.db import models
from neighborhood.models import Neighborhood
from commune.models import Commune
from region.models import Region
import datetime

class House(models.Model):
    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.PositiveSmallIntegerField("Numero",default=0)
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
    name = models.CharField("Nombre",max_length=100,default="")
    lat = models.FloatField("Latitud",default=0.0)
    lon = models.FloatField("Longitud",default=0.0)
    neighborhood = models.ForeignKey(Neighborhood,
        on_delete=models.CASCADE,
        verbose_name="Barrio",
        blank=True,
        null=True)

    # Areas
    areaUtilTerreno = models.IntegerField("Metros cuadrados útiles terreno",
        default=0,
        blank=True,
        null=True)
    areaUtilEdificacion = models.IntegerField("Metros cuadrados útiles construccion",
        default=0,
        blank=True,
        null=True)

    # Cosas de precio
    valorComercialUF = models.IntegerField("Valor comercial UF",
        default=0,
        blank=True,
        null=True)

    # Detalles tecnicos
    anoConstruccion = models.IntegerField("Año construccion",
        default=0,
        blank=True,
        null=True)
    vidaUtilRemanente = models.IntegerField("Vida util remanente",
        default=0,
        blank=True,
        null=True)
    avaluoFiscal = models.FloatField("Avaluo fiscal",
        default=0.0,
        blank=True,
        null=True)
    dfl2 = models.BooleanField("DFL 2",
        default=False,
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
        default='SA',
        blank=True,
        null=True)
    copropiedadInmobiliaria = models.BooleanField("Copropiedad Inmobiliaria",
        default=False,
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
        default='P',
        blank=True,
        null=True)
    tipoBien = models.CharField("Tipo de bien",
        max_length=20,
        default='',
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
        default='',
        blank=True,
        null=True)
    usoActual = models.CharField("Uso actual",
        max_length=20,
        default='',
        blank=True,
        null=True)
    usoFuturo = models.CharField("Uso futuro",
        max_length=20,
        default='',
        blank=True,
        null=True)
    permisoEdificacion = models.IntegerField("Permiso edificación",
        default=0,
        blank=True,
        null=True)
    permisoEdificacionDate = models.DateField("Permiso edificación fecha",
        default=datetime.date.today,
        blank=True,
        null=True)
    recepcionFinal = models.IntegerField("Recepcion final",
        default=0,
        blank=True,
        null=True)
    recepcionFinalDate = models.DateField("Recepcion final fecha",
        default=datetime.date.today,
        blank=True,
        null=True)
    expropiacion = models.BooleanField("Expropiacion",
        default=False,
        blank=True,
        null=True)
    viviendaSocial = models.BooleanField("Vivienda social",
        default=False,
        blank=True,
        null=True)
    adobe = models.BooleanField("Construccion de adobe",
        default=False,
        blank=True,
        null=True)
    desmontable = models.BooleanField("Construccion desmotanble",
        default=False,
        blank=True,
        null=True)

    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)
