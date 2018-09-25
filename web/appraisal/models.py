from django.db import models
from django.utils.text import slugify
from apartment.models import Apartment
from django.contrib.auth.models import User
import datetime
import reversion

@reversion.register()
class Appraisal(models.Model):

    STATE_ACTIVE = 1
    STATE_FINISHED = 2
    STATES = (
        (STATE_ACTIVE,'active'),
        (STATE_FINISHED,'finished')
    )

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE,verbose_name="Departamento",blank=False,null=False)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
    timeModified = models.DateTimeField("Time modified",blank=True,null=True)
    timeFinished = models.DateTimeField("Time finished",blank=True,null=True)
    timeDue = models.DateTimeField("Time due",blank=True,null=True)
    status = models.IntegerField("Estado",choices=STATES,default=STATE_ACTIVE)

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
    def status_verbose(self):
        return str(self.status)

    @property
    def finished(self):
        if self.status == self.STATE_FINISHED:
            return True
        else:
            return False

    @property
    def active(self):
        if self.status == self.STATE_ACTIVE:
            return True
        else:
            return False

    @property
    def url(self):
        return "/appraisal/{}/{}/{}/{}/{}/departamento/{}/{}/{}/".format(
            slugify(self.apartment.building.addressRegion),
            slugify(self.apartment.building.addressCommune),
            slugify(self.apartment.building.addressStreet),
            self.apartment.building.addressNumber,
            self.apartment.building.id,
            self.apartment.number,
            self.apartment.id,
            self.id
        )

    @property
    def daySinceCreated(self):
        today = datetime.date.today()
        diff  = today - self.timeCreated.date()
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

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.CharField("Comment",max_length=500)
    appraisal = models.ForeignKey(Appraisal, null=True, on_delete=models.CASCADE)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
