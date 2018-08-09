from django.db import models

class House(models.Model):
    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.PositiveSmallIntegerField("Numero",default=0)
    addressCommune = models.CharField("Comuna",max_length=300,default="")
    addressRegion = models.CharField("Region",max_length=300,default="")
    name = models.CharField("Nombre",max_length=100,default="")
    lat = models.FloatField("Latitud",default=0.0)
    lon = models.FloatField("Longitud",default=0.0)
    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)

class Building(models.Model):

    addressStreet = models.CharField("Calle",max_length=300,default="")
    addressNumber = models.PositiveSmallIntegerField("Numero",default=0)
    addressCommune = models.CharField("Comuna",max_length=300,default="")
    addressRegion = models.CharField("Region",max_length=300,default="")
    name = models.CharField("Nombre",max_length=100,default="")
    lat = models.FloatField("Latitud",default=0.0)
    lon = models.FloatField("Longitud",default=0.0)

    def __str__(self):
        return "{}, {} {}, {}, {}".format(
            self.name,
            self.addressStreet,
            self.addressNumber,
            self.addressCommune,
            self.addressRegion)

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
    floor = models.PositiveSmallIntegerField("Piso")
    number = models.CharField("Numero",max_length=10)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios")
    bathrooms = models.PositiveSmallIntegerField("Baños")
    totalSquareMeters = models.DecimalField("Superficie",max_digits=7,decimal_places=2)
    usefulSquareMeters = models.DecimalField("Superficie util",max_digits=7,decimal_places=2)
    orientation = models.CharField("Orientacion",max_length=2,choices=ORIENTATIONS)
    generalDescription = models.CharField("Descripcion general",max_length=10000,default="")

    tipoPropiedad = models.PositiveSmallIntegerField("Tipo de propiedad",choices=USE,default=0)
    antiguedad = models.PositiveSmallIntegerField("Antiguedad",default=0)
    vidaUtil = models.PositiveSmallIntegerField("Vida util",default=80)

    selloDeGases = models.PositiveSmallIntegerField("Sello de gases",default=1)

    permisoEdificacionNo = models.PositiveSmallIntegerField("Numero permiso edificacion",default=0)
    permisoEdificacionFecha = models.DateField("Fecha permiso edificacion",default='2006-10-25')
    permisoEdificacionSuperficie = models.DecimalField("Superficie permiso edificacion",max_digits=7,decimal_places=2,default=0)
