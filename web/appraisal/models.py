from django.db import models
from django.utils.text import slugify
from realestate.models import RealEstate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import datetime
import reversion

class Photo(models.Model):
    photo = models.ImageField(upload_to='test/',default='no-img.jpg')
    description = models.CharField("Descripción",
        max_length=200,
        blank=True,
        null=True)
    thumbnail = ImageSpecField(source='photo',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 60})

@reversion.register()
class Appraisal(models.Model):

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
    timePaused = models.DateTimeField("Time paused",blank=True,null=True)
    STATE_IMPORTED = 0
    STATE_ACTIVE = 1
    STATE_PAUSED = 2
    STATE_FINISHED = 3
    STATES = (
        (STATE_ACTIVE,'active'),
        (STATE_FINISHED,'finished'),
        (STATE_PAUSED,'paused'),
        (STATE_IMPORTED, 'imported')
    )
    state = models.IntegerField("Estado",choices=STATES,default=STATE_ACTIVE)

    APPRAISAL = 1
    PORTAL = 2
    TOCTOC = 3
    source_choices = [
        (APPRAISAL, "Tasación"),
        (PORTAL, "Portal Inmbiliario"),
        (TOCTOC, "TocToc")
    ]
    source = models.IntegerField("Fuente de tasación",choices=source_choices,
        default=APPRAISAL,blank=True,null=True)
    price = models.FloatField("Precio tasación",blank=True,null=True)

    # generales
    OTHER = 0
    BCI = 1
    SANTANDER = 2
    ITAU = 3
    INTERNACIONAL = 4
    CHILE = 5
    CORPBANCA = 6
    SCOTIABANK = 7
    BICE = 8
    petitioner_choices = [
        (BCI, "BCI"),
        (SANTANDER, "Santander"),
        (ITAU, "Itaú"),
        (INTERNACIONAL, "Banco Internacional"),
        (CHILE, "Banco de Chile"),
        (CORPBANCA, "Corpbanca"),
        (SCOTIABANK, "Scotiabank"),
        (BICE, "BICE"),
        (OTHER, "Otro")
    ]
    solicitante = models.IntegerField("Solicitante", choices=petitioner_choices,blank=True,null=True)

    OTRA = 0
    INMOBILIARIA = 1
    REVISION = 2
    ESCRITORIO = 3
    PILOTO = 4
    TERRENO = 5
    request_choices = [
        (INMOBILIARIA, 'Hipotecaria'),
        (REVISION, 'Revisión'),
        (ESCRITORIO, 'Escritorio'),
        (PILOTO, 'Piloto'),
        (TERRENO, 'Terreno'),
        (OTRA, 'Otra')
    ]
    tipoTasacion = models.IntegerField("Tipo Pedido", choices=request_choices,blank=True,null=True)

    OTRO = 0
    GARANTIA = 1
    CREDITO = 2
    REMATE = 3
    VENTA = 4
    LIQUIDACION = 5
    objective_choices = [
        (OTRO, 'Otro'),
        (GARANTIA, 'Garantía'),
        (CREDITO, 'Crédito'),
        (REMATE, 'Remate'),
        (VENTA, 'Venta'),
        (LIQUIDACION, 'Liquidación' ),
    ]
    objetivo = models.IntegerField("Objetivo", choices=objective_choices,blank=True,null=True)

    solicitanteSucursal = models.CharField("Solicitante sucursal",max_length=100,blank=True,null=True)
    solicitanteEjecutivo = models.CharField("Solicitante ejecutivo",max_length=100,blank=True,null=True)
    solicitanteCodigo = models.CharField("Solicitante código",max_length=100,blank=True,null=True)
    cliente = models.CharField("Cliente",max_length=100,blank=True,null=True)
    clienteRut = models.CharField("Cliente RUT",max_length=10,blank=True,null=True)
    propietario = models.CharField("Propietario",max_length=100,blank=True,null=True)
    propietarioRut = models.CharField("Propietario RUT",max_length=10,blank=True,null=True)
    rolAvaluo = models.CharField("Rol principal",max_length=20,blank=True,null=True)
    tasadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_tasador')
    visadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_visador')
    visadorEmpresa = models.CharField("Visador empresa",max_length=100,blank=True,null=True)
    visadorEmpresaMail = models.EmailField("Visador empresa mail",max_length=100,blank=True,null=True)

    photos = models.ManyToManyField(Photo)

    # valor
    valorUF = models.IntegerField("Valor UF",blank=True,null=True)

    @property
    def status_verbose(self):
        return str([state[1] for state in self.STATES if state[0] == self.state][0])

    @property
    def hasTasador(self):
        print(self.tasadorUser)

    @property
    def finished(self):
        if self.state == self.STATE_FINISHED:
            return True
        else:
            return False

    @property
    def active(self):
        if self.state == self.STATE_ACTIVE:
            return True
        else:
            return False

    @property
    def paused(self):
        if self.state == self.STATE_PAUSED:
            return True
        else:
            return False

    @property
    def timeDueReal(self):
        if self.state == self.STATE_PAUSED:
            if self.timePaused != None:
                return self.timeDue+(datetime.datetime.now(datetime.timezone.utc)-self.timePaused)
            else:
                return self.timeDue
        else:
            return self.timeDue

    @property
    def url(self):
        address = self.realEstate.address_dict
        if self.realEstate.propertyType == RealEstate.TYPE_APARTMENT:
            return  "/appraisal/{}/{}/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.apartment.building_in.id,
                self.realEstate.apartment.number,
                self.realEstate.apartment.id,
                self.id)
        elif self.realEstate.propertyType == RealEstate.TYPE_HOUSE:
            return "/appraisal/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.house.id,
                self.id)
        else:
            return "error"

    @property
    def daySinceCreated(self):
        today = datetime.date.today()
        diff  = today - self.timeCreated.date()
        return diff.days

    @property
    def daysLeft(self):
        today = datetime.date.today()
        diff  = self.timeDue.date()-today
        return diff.days

    @property
    def is_appraisalOverdue(self):
        if self.timeDue < datetime.date.today():
            return True
        return False

    @property
    def timeLeft(self):
        return self.timeDue - self.timeCreated

    class Meta:
        app_label = 'appraisal'
        permissions = (
            ("assign_tasador", "Can assign tasadores"),
            ("assign_visador", "Can assign visadores"),)

    def __str__(self):
        return "{} {}".format(
            self.realEstate,
            self.solicitante)

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name.name)
            yield (field_name.name, value)

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.CharField("Comment",max_length=500)
    appraisal = models.ForeignKey(Appraisal, null=True, on_delete=models.CASCADE)
    conflict = models.BooleanField("Incidencia",default=False)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
