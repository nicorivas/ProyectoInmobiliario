from django.db import models
from property.models import Property
from building.models import Building

class Apartment(Property):
    ORIENTATIONS = (
        ('N', 'Norte'),
        ('NE', 'Norponiente'),
        ('E', 'Poniente'),
        ('SE', 'Surponiente'),
        ('S', 'Sur'),
        ('WS', 'Suroriente'),
        ('W', 'Oriente'),
        ('NW', 'Nororiente')
    )
    USE = (
        (0,'Usada'),
        (1,'Nueva')
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE,verbose_name="Edificio",blank=False,null=False)
    number = models.CharField("Numero",max_length=10,null=True)

    floor = models.PositiveSmallIntegerField("Piso",null=True,blank=True)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    builtSquareMeters = models.DecimalField("Superficie construida",max_digits=7,decimal_places=2,null=True,blank=True)
    usefulSquareMeters = models.DecimalField("Superficie util",max_digits=7,decimal_places=2,null=True,blank=True)
    orientation = models.CharField("Orientacion",max_length=2,choices=ORIENTATIONS,null=True,blank=True)
    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    tipoPropiedad = models.PositiveSmallIntegerField("Tipo de propiedad",choices=USE,default=0,null=True)
    antiguedad = models.PositiveSmallIntegerField("Antiguedad",default=0,null=True)
    vidaUtil = models.PositiveSmallIntegerField("Vida util",default=80,null=True)

    selloDeGases = models.PositiveSmallIntegerField("Sello de gases",default=1,null=True)

    permisoEdificacionNo = models.PositiveSmallIntegerField("Numero permiso edificacion",default=0,null=True)
    permisoEdificacionFecha = models.DateField("Fecha permiso edificacion",default='2006-10-25',null=True)
    permisoEdificacionSuperficie = models.DecimalField("Superficie permiso edificacion",max_digits=7,decimal_places=2,default=0,null=True)

    marketPrice = models.PositiveSmallIntegerField("Precio mercado UF",null=True,blank=True)

    sourceUrl = models.URLField("Source url",null=True,blank=True)
    sourceName = models.CharField("Source name",max_length=20,null=True,blank=True)
    sourceId = models.CharField("Source id",max_length=20,null=True,blank=True)

    @property
    def sourceNameNice(self):
        "Returns source to be printed in a nice way."
        if self.sourceName == 'toctoc':
            return 'TocToc'
        elif self.sourceName == 'portali':
            return 'P.I.'
        else:
            return self.sourceName

    @property
    def propertyType(self):
        "Return name of type."
        return "departamento"

    class Meta:
        app_label = 'apartment'
