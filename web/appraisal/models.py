from django.db import models
from apartment.models import Apartment

class Appraisal(models.Model):

    ESTADOS = (
        ('a','activa'),
        ('t','terminada')
    )

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE,verbose_name="Departamento",blank=False,null=False)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
    timeModified = models.DateTimeField("Time modified",blank=True,null=True)
    status = models.CharField("Estado",max_length=10,choices=ESTADOS,default='a')

    # generales
    solicitante = models.CharField("Solicitante sucursal",max_length=100,blank=True,null=True)
    solicitanteSucursal = models.CharField("Solicitante sucursal",max_length=100,blank=True,null=True)
    solicitanteEjecutivo = models.CharField("Solicitante ejecutivo",max_length=100,blank=True,null=True)
    cliente = models.CharField("Cliente",max_length=100,blank=True,null=True)
    clienteRut = models.IntegerField("Cliente RUT",blank=True,null=True)
    propietario = models.CharField("Propietario",max_length=100,blank=True,null=True)
    propietarioRut = models.IntegerField("Propietario RUT",blank=True,null=True)
    rolAvaluo = models.IntegerField("Rol avaluo",blank=True,null=True)
    tasadorNombre = models.CharField("Tasador",max_length=100,blank=True,null=True)
    tasadorRut = models.IntegerField("Tasador rut",blank=True,null=True)
    visadorEmpresa = models.CharField("Visador empresa",max_length=100,blank=True,null=True)
    visadorEmpresaMail = models.CharField("Visador empresa mail",max_length=100,blank=True,null=True)

    class Meta:
        app_label = 'appraisal'

    def __str__(self):
        return "Appraisal of {}".format(
            self.apartment)
