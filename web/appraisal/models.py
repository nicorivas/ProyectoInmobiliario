from django.db import models
from apartment.models import Apartment
from django.contrib.auth.models import User
import datetime
import reversion

@reversion.register()
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
    solicitante = models.CharField("Solicitante",max_length=100,blank=True,null=True)
    solicitanteSucursal = models.CharField("Solicitante sucursal",max_length=100,blank=True,null=True)
    solicitanteEjecutivo = models.CharField("Solicitante ejecutivo",max_length=100,blank=True,null=True)
    cliente = models.CharField("Cliente",max_length=100,blank=True,null=True)
    clienteRut = models.IntegerField("Cliente RUT",blank=True,null=True)
    propietario = models.CharField("Propietario",max_length=100,blank=True,null=True)
    propietarioRut = models.IntegerField("Propietario RUT",blank=True,null=True)
    rolAvaluo = models.IntegerField("Rol principal",blank=True,null=True)
    tasadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_tasador')
    visadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_visador')
    visadorEmpresa = models.CharField("Visador empresa",max_length=100,blank=True,null=True)
    visadorEmpresaMail = models.EmailField("Visador empresa mail",max_length=100,blank=True,null=True)

    # valor
    valorUF = models.IntegerField("Valor UF",blank=True,null=True)

    @property
    def daySinceCreated(self):
        today = datetime.date.today()
        diff  = today - self.timeCreated.date()
        print(diff.days)
        return diff.days

    class Meta:
        app_label = 'appraisal'
        permissions = (
            ("assign_tasador", "Can assign tasadores"),
            ("assign_visador", "Can assign visadores"),)

    def __str__(self):
        return "{} {}".format(
            self.apartment,
            self.solicitante)

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name.name)
            yield (field_name.name, value)
