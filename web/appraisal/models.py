from django.db import models
from django.utils.text import slugify
from realestate.models import RealEstate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import datetime
import reversion

class Comment(models.Model):
    EVENT_CONTACTO_VALIDADO = 1
    EVENT_ASIGNACION_ACEPTADA = 2
    EVENT_ASIGNACION_RECHAZADA = 6
    EVENT_VISITA_ACORDADA = 3
    EVENT_PROPIEDAD_VISITADA = 4
    EVENT_ENVIADA_A_VISADOR = 5
    EVENT_ENTREGADO_AL_CLIENTE = 8
    EVENT_CLIENTE_VALIDADO = 9
    EVENT_CONTABILIZACION = 10
    EVENT_ABORTADO = 18
    EVENT_INCIDENCIA = 19
    EVENT_CORRECCION_INFORME = 20
    EVENT_OBSERVACION_VISADOR = 21
    EVENT_OBJECION = 22
    EVENT_TASADOR_ASIGNADO = 23
    EVENT_TASADOR_DESASIGNADO = 25
    EVENT_VISADOR_ASIGNADO = 26
    EVENT_VISADOR_DESASIGNADO = 27
    EVENT_TASACION_INGRESADA = 24
    EVENT_OTRO = 0
    event_choices = (
        (EVENT_CONTACTO_VALIDADO, "Contacto validado"),
        (EVENT_ASIGNACION_ACEPTADA, "Asignación aceptada"),
        (EVENT_ASIGNACION_RECHAZADA, "Asignación rechazada"),
        (EVENT_CLIENTE_VALIDADO, "Cliente validado"),
        (EVENT_TASADOR_ASIGNADO, "Tasador asignado"),
        (EVENT_VISADOR_ASIGNADO, "Visador asignado"),
        (EVENT_TASADOR_DESASIGNADO, "Tasador desasignado"),
        (EVENT_VISADOR_DESASIGNADO, "Visador desasignado"),
        (EVENT_TASACION_INGRESADA, "Tasación ingresada"),
        (EVENT_VISITA_ACORDADA, "Visita acordada"),
        (EVENT_PROPIEDAD_VISITADA, "Propiedad visitada"),
        (EVENT_ENVIADA_A_VISADOR, "Enviado a visador"),
        (EVENT_ENTREGADO_AL_CLIENTE, "Entregado al cliente"),
        (EVENT_CONTABILIZACION, "Contabilización"),
        (EVENT_ABORTADO, "Abortado"),
        (EVENT_INCIDENCIA, "Incidencia"),
        (EVENT_CORRECCION_INFORME, "Corrección informe"),
        (EVENT_OBSERVACION_VISADOR, "Observación visador"),
        (EVENT_OBJECION, "Objeción"),
        (EVENT_OTRO, "Otro")
    )
    event_choices_form = (
        (EVENT_CONTACTO_VALIDADO, "Contacto validado"),
        (EVENT_CLIENTE_VALIDADO, "Cliente validado"),
        (EVENT_VISITA_ACORDADA, "Visita acordada"),
        (EVENT_PROPIEDAD_VISITADA, "Propiedad visitada"),
        (EVENT_ENVIADA_A_VISADOR, "Enviado a visador"),
        (EVENT_ENTREGADO_AL_CLIENTE, "Entregado al cliente"),
        (EVENT_ABORTADO, "Abortado"),
        (EVENT_INCIDENCIA, "Incidencia"),
        (EVENT_CORRECCION_INFORME, "Corrección informe"),
        (EVENT_OBSERVACION_VISADOR, "Observación visador"),
        (EVENT_OBJECION, "Objeción"),
        (EVENT_OTRO, "Otro")
    )
    event = models.IntegerField(choices=event_choices,default=0,blank=False,null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.CharField("Comment",max_length=500)
    conflict = models.BooleanField("Incidencia",default=False)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)

    @property
    def hasText(self):
        if self.text == "" or self.text == None:
            return False
        else:
            return True

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

class Document(models.Model):
    document = models.ImageField(upload_to='test/',default='no-img.jpg')
    description = models.CharField("Descripción",
        max_length=200,
        blank=True,
        null=True)
    thumbnail = ImageSpecField(source='document',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 60})

class Rol(models.Model):
    code = models.CharField("Rol",max_length=20,blank=True,null=True)
    SIN_DATOS = 0
    DEFINITIVO = 1
    MATRIZ = 2
    EN_TRAMITE = 3
    PREASIGNADO = 4
    BIEN_COMUN = 5
    USO_Y_GOCE = 6
    NO_ENROLADO = 7
    rolTypeChoices = [
        (SIN_DATOS, "Sin datos"),
        (DEFINITIVO, "Definitivo"),
        (MATRIZ, "Matriz"),
        (EN_TRAMITE, "En trámite"),
        (PREASIGNADO, "Preasignado"),
        (BIEN_COMUN, "Bien común"),
        (USO_Y_GOCE, "Uso y Goce"),
        (NO_ENROLADO, "No enrolado")
    ]
    state = models.IntegerField("Estado", choices=rolTypeChoices, blank=True,null=False,default=0)

@reversion.register()
class Appraisal(models.Model):
    '''
    Hola
    '''

    realEstate = models.ForeignKey(RealEstate, on_delete=models.CASCADE,
        verbose_name="Propiedad",null=True)

    timeRequest = models.DateTimeField("Time created",blank=True,null=True)
    timeDue = models.DateTimeField("Time due",blank=True,null=True)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
    timeModified = models.DateTimeField("Time modified",blank=True,null=True)
    timeFinished = models.DateTimeField("Time finished",blank=True,null=True)
    timePaused = models.DateTimeField("Time paused",blank=True,null=True)

    STATE_IMPORTED = 0
    STATE_NOTASSIGNED = 4
    STATE_ACTIVE = 1
    STATE_PAUSED = 2
    STATE_FINISHED = 3
    STATES = (
        (STATE_NOTASSIGNED,'not assigned'),
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

    NONE = ''
    SIN_VISITA = 0
    COMPLETA = 1
    EXTERIOR = 2
    visit_choices = [
        (NONE,'---------'),
        (SIN_VISITA, 'Sin Visita'),
        (COMPLETA, 'Completa'),
        (EXTERIOR, 'Solo Exterior')
    ]
    visita = models.IntegerField("Visita", choices=visit_choices, blank=True,null=True)

    # generales
    NONE = ''
    OTRA = 0
    HIPOTECARIA = 1
    COMERCIAL = 7
    REVISION = 2
    ESCRITORIO = 3
    PILOTO = 4
    TERRENO = 5
    AVANCE_DE_OBRA = 6
    tipoTasacion_choices = [
        (NONE,'---------'),
        (HIPOTECARIA, 'Hipotecaria'),
        (COMERCIAL, 'Comercial'),
        (TERRENO, 'Terreno'),
        (AVANCE_DE_OBRA,'Avance de obra'),
        (REVISION, 'Revisión'),
        (ESCRITORIO, 'Escritorio'),
        (PILOTO, 'Piloto'),
        (OTRA, 'Otra')
    ]
    tipoTasacion = models.IntegerField("Tipo Pedido", choices=tipoTasacion_choices, blank=True, null=True)

    NONE = ''
    OTRO = 0
    GARANTIA = 1
    CREDITO = 2
    REMATE = 3
    VENTA = 4
    LIQUIDACION = 5
    DACION_EN_PAGO = 6
    TOMA_DE_SEGURO = 7
    objective_choices = [
        (NONE,'---------'),
        (CREDITO, 'Crédito'),
        (GARANTIA, 'Garantía General'),
        (VENTA, 'Venta Activos'),
        (DACION_EN_PAGO, 'Dación en Pago'),
        (REMATE, 'Remate'),
        (LIQUIDACION, 'Liquidación'),
        (TOMA_DE_SEGURO, 'Toma de Seguro'),
        (OTRO, 'Otra'),
    ]
    finalidad = models.IntegerField("Finalidad", choices=objective_choices,blank=True,null=True)

    NONE = ''
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
        (NONE,'---------'),
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
    solicitante = models.IntegerField("Solicitante", choices=petitioner_choices, blank=True, null=True)
    solicitanteOtro = models.CharField("Solicitante", max_length=100, blank=True, null=True)
    solicitanteSucursal = models.CharField("Solicitante sucursal",max_length=100,blank=True,null=True)
    solicitanteCodigo = models.CharField("Solicitante código",max_length=100,blank=True,null=True)
    solicitanteEjecutivo = models.CharField("Solicitante ejecutivo",max_length=100,blank=True,null=True)
    solicitanteEjecutivoEmail = models.CharField("Solicitante email",max_length=100,blank=True,null=True)
    solicitanteEjecutivoTelefono = models.CharField("Solicitante teléfono",max_length=20,blank=True,null=True)

    cliente = models.CharField("Cliente",max_length=100,blank=True,null=True)
    clienteRut = models.CharField("Cliente RUT",max_length=13,blank=True,null=True)
    clienteEmail = models.CharField("Cliente Email",max_length=100,blank=True,null=True)
    clienteTelefono = models.CharField("Cliente Teléfono",max_length=20,blank=True,null=True)

    contacto = models.CharField("Contacto",max_length=100,blank=True,null=True)
    contactoRut = models.CharField("Contacto RUT",max_length=13,blank=True,null=True)
    contactoEmail = models.CharField("Contacto Email",max_length=100,blank=True,null=True)
    contactoTelefono = models.CharField("Contacto Teléfono",max_length=20,blank=True,null=True)

    propietario = models.CharField("Propietario",max_length=100,blank=True,null=True)
    propietarioRut = models.CharField("Propietario RUT",max_length=13,blank=True,null=True)
    propietarioEmail = models.CharField("Contacto Email",max_length=100,blank=True,null=True)
    propietarioTelefono = models.CharField("Contacto Teléfono",max_length=20,blank=True,null=True)
    propietarioReferenceSII = models.BooleanField("Propietario Referencia SII",blank=True,default=False)
    
    tasadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_tasador')

    visadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_visador')
    visadorEmpresa = models.CharField("Visador empresa",max_length=100,blank=True,null=True)
    visadorEmpresaMail = models.EmailField("Visador empresa mail",max_length=100,blank=True,null=True)

    roles = models.ManyToManyField(Rol)

    orderFile = models.FileField("Documento pedido",upload_to='orders/',null=True,blank=True)

    photos = models.ManyToManyField(Photo)

    documents = models.ManyToManyField(Document)

    comments = models.ManyToManyField(Comment)

    commentsOrder = models.CharField("Comentarios pedido",max_length=1000,null=True,blank=True)

    valuationRealEstate = models.ManyToManyField(RealEstate,related_name="valuationRealEstate")

    descripcionSector = models.TextField("Descripción sector",max_length=10000,default="",null=True,blank=True)
    descripcionPlanoRegulador = models.TextField("Descripción plano regulador",max_length=10000,default="",null=True,blank=True)
    descripcionExpropiacion = models.TextField("Descripción expropiación",max_length=10000,default="",null=True,blank=True)

    # valor
    valorUF = models.FloatField("Valor UF", blank=True,null=True)




    def addComment(self,event_id,user,timeCreated,text=None):
        comment = Comment(event=event_id,user=user,timeCreated=timeCreated)
        if text and len(text) > 0:
            comment.text = text
        comment.save()
        self.comments.add(comment)
        self.save()
        return comment

    def getCommentChoices(self,comments=None):
        # List of comment types that can only happen once:
        once_ids = [
            Comment.EVENT_CONTACTO_VALIDADO,
            Comment.EVENT_CLIENTE_VALIDADO,
            Comment.EVENT_VISITA_ACORDADA,
            Comment.EVENT_PROPIEDAD_VISITADA,
            Comment.EVENT_ENVIADA_A_VISADOR,
            Comment.EVENT_ENTREGADO_AL_CLIENTE,
            Comment.EVENT_ABORTADO]
        if comments == None:
            comments = self.comments.all()
        event_choices = Comment.event_choices_form
        comment_ids = comments.values_list('event',flat=True)
        for once_id in once_ids:
            if once_id in comment_ids:
                event_choices = [x for x in event_choices if x[0] != once_id]
        return event_choices

    @property
    def status_verbose(self):
        return str([state[1] for state in self.STATES if state[0] == self.state][0])

    @property
    def hasTasador(self):
        print(self.tasadorUser)

    @property
    def not_assigned(self):
        if self.state == self.STATE_NOTASSIGNED:
            return True
        else:
            return False

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
        return ''
        if self.realEstate == None:
            return "/appraisal/{}/".format(self.id)
        address = self.realEstate.address_dict
        if self.realEstate.propertyType == RealEstate.TYPE_EDIFICIO:
            return  "/appraisal/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.apartmentbuilding.id,
                self.id)
        elif self.realEstate.propertyType == RealEstate.TYPE_CASA:
            return "/appraisal/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.house.id,
                self.id)
        if self.realEstate.propertyType == RealEstate.TYPE_DEPARTAMENTO:
            return  "/appraisal/{}/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.apartment.building_in.id,
                self.realEstate.apartment.id,
                self.id)
        elif self.realEstate.propertyType == RealEstate.TYPE_CONDOMINIO:
            return  "/appraisal/{}/{}/{}/{}/{}/{}/{}/".format(
                slugify(address['region']),
                slugify(address['commune']),
                slugify(address['street']),
                slugify(address['number']),
                self.realEstate.propertyType,
                self.realEstate.id,
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
    def solicitanteVerbose(self):
        if isinstance(self.solicitante,type(None)):
            return '-'
        else:
            for choice in self.petitioner_choices:
                if self.solicitante == choice[0]:
                    if choice[1] == "Banco Internacional":
                        return "Banco Internacional"
                    if choice[1] == "Banco de Chile":
                        return "Banco de Chile"
                    else:
                        return choice[1]
            return '-'

    @property
    def solicitanteVerboseShort(self):
        if isinstance(self.solicitante,type(None)):
            return '-'
        else:
            for choice in self.petitioner_choices:
                if self.solicitante == choice[0]:
                    if choice[1] == "Banco Internacional":
                        return "Internacional"
                    if choice[1] == "Banco de Chile":
                        return "B. de Chile"
                    else:
                        return choice[1]
            return '-'

    @property
    def timeLeft(self):
        return self.timeDue - self.timeCreated

    class Meta:
        app_label = 'appraisal'
        permissions = (
            ("assign_tasador", "Can assign tasadores"),
            ("assign_visador", "Can assign visadores"),)

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name.name)
            yield (field_name.name, value)

class AppraisalEvaluation(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    appraisal = models.OneToOneField(Appraisal, on_delete=models.CASCADE, primary_key=True)
    completeness = models.BooleanField("Aceptación del informe completo (50%)", blank=True, null=False, default=True)
    onTime = models.BooleanField("Entrega a tiempo (25%)", blank=True, null=False, default=True)
    correctSurface = models.BooleanField("Superficies correctas -hasta un 5% de error- (15%)", blank=True,
                                         null=False, default=True)
    completeNormative = models.BooleanField("Normativa Completa y correcta (5%)", blank=True, null=False, default=True)
    homologatedReferences = models.BooleanField("Referencias Homologables si las hubieran (2,5%)", blank=True,
                                                null=False, default=True)
    generalQuality = models.BooleanField("Calidad General -peso, imagenes claras configuración- (2,5%)",
                                         blank=True,null=False, default=True)
    commentText = models.CharField("Comentarios de la tasación", null=False, blank=True, max_length=500)
    commentFeedback = models.CharField("Feedback de la tasación", null=False, blank=True, max_length=500)

    @property
    def evaluationResult(self):
        grade = 0.0
        if self.completeness:
            grade += 0.5
        if self.onTime:
            grade += 0.25
        if self.correctSurface:
            grade += 0.15
        if self.completeNormative:
            grade += 0.05
        if self.homologatedReferences:
            grade += 0.025
        if self.generalQuality:
            grade += 0.025
        return grade