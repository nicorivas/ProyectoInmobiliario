from django.db import models
from django.utils.text import slugify
from apartment.models import Apartment
#from house.models import House
from realestate.models import RealEstate
from django.contrib.auth.models import User
import datetime
import reversion

#from django.contrib.contenttypes.fields import GenericForeignKey
#from django.contrib.contenttypes.models import ContentType


@reversion.register()
class Appraisal(models.Model):

    STATE_ACTIVE = 1
    STATE_FINISHED = 2
    STATES = (
        (STATE_ACTIVE,'active'),
        (STATE_FINISHED,'finished')
    )

    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    '''

    TYPE_UNDEFINED = 0
    TYPE_HOUSE = 1
    TYPE_APARTMENT = 2
    TYPE_BUILDING = 3

    propertyType_choices = [
        (TYPE_UNDEFINED, "Indefinido"),
        (TYPE_HOUSE, "Casa"),
        (TYPE_APARTMENT, "Departamento"),
        (TYPE_BUILDING, "Edificio")]
    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=TYPE_UNDEFINED)

    realEstate = models.ForeignKey(RealEstate, on_delete=models.CASCADE,
        verbose_name="Propiedad")
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
            print('goli')
            return True
        else:
            return False

    @property
    def url(self):
        if self.realestate.propertyType == RealEstate.TYPE_APARTMENT:
            return "/appraisal/{}/{}/{}/{}/{}/{}/{}/{}/{}/".format(
            slugify(self.realestate.building.addressRegion),
            slugify(self.realestate.building.addressCommune),
            slugify(self.realestate.building.addressStreet),
            self.realestate.building.addressNumber,
            self.realestate.propertyType,
            self.realestate.building.id,
            self.realestate.number,
            self.realestate.id,
            self.id
            )
        elif self.realestate.propertyType == RealEstate.TYPE_HOUSE:
            return "/appraisal/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(self.realestate.addressRegion),
                slugify(self.realstate.addressCommune),
                slugify(self.realestate.addressStreet),
                self.realestate.addressNumber,
                self.realestate.propertyType,
                self.realestate.id,
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
