from django.db import models
from building.models import Building

class Apartment(models.Model):
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
    number = models.CharField("Numero",max_length=10)

    floor = models.PositiveSmallIntegerField("Piso",null=True,blank=True)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    totalSquareMeters = models.DecimalField("Superficie",max_digits=7,decimal_places=2,null=True,blank=True)
    usefulSquareMeters = models.DecimalField("Superficie util",max_digits=7,decimal_places=2,null=True,blank=True)
    orientation = models.CharField("Orientacion",max_length=2,choices=ORIENTATIONS,null=True,blank=True)
    generalDescription = models.CharField("Descripcion general",max_length=10000,default="")

    tipoPropiedad = models.PositiveSmallIntegerField("Tipo de propiedad",choices=USE,default=0)
    antiguedad = models.PositiveSmallIntegerField("Antiguedad",default=0)
    vidaUtil = models.PositiveSmallIntegerField("Vida util",default=80)

    selloDeGases = models.PositiveSmallIntegerField("Sello de gases",default=1)

    permisoEdificacionNo = models.PositiveSmallIntegerField("Numero permiso edificacion",default=0)
    permisoEdificacionFecha = models.DateField("Fecha permiso edificacion",default='2006-10-25')
    permisoEdificacionSuperficie = models.DecimalField("Superficie permiso edificacion",max_digits=7,decimal_places=2,default=0)

    class Meta:
        app_label = 'apartment'
