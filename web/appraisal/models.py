from django.db import models
from django.utils.text import slugify
from realestate.models import RealEstate, Price
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from building.models import Building
from terrain.models import Terrain
from house.models import House
from apartmentbuilding.models import ApartmentBuilding
from apartment.models import Apartment

import datetime
import reversion

class Photo(models.Model):
    
    photo = models.ImageField(upload_to='test/',default='no-img.jpg',null=True)
    
    NULL = ''
    PHOTO_CATEGORY_ENTORNO = 0
    PHOTO_CATEGORY_EMPLAZAMIENTO = 1
    PHOTO_CATEGORY_FACHADA = 2
    PHOTO_CATEGORY_ESPACIOS_COMUNES = 3
    PHOTO_CATEGORY_OTHER = 4
    PHOTO_CATEGORIES = (
        (NULL,'---------'),
        (PHOTO_CATEGORY_ENTORNO,'Entorno'),
        (PHOTO_CATEGORY_EMPLAZAMIENTO,'Emplazamiento'),
        (PHOTO_CATEGORY_FACHADA,'Fachada'),
        (PHOTO_CATEGORY_ESPACIOS_COMUNES,'Espacios comunes'),
        (PHOTO_CATEGORY_OTHER,'Otra')
        )
    category = models.IntegerField("Categoría",
        choices=PHOTO_CATEGORIES,
        blank=True,
        null=True)

    description = models.CharField("Descripción",
        max_length=200,
        blank=True,
        null=True)

    # Photos with fixed cannot be deleted (the image of course yes).
    fixed = models.BooleanField("Fixed",blank=False,default=False)

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

    apartment = models.ForeignKey(Apartment,null=True,blank=True,related_name='roles',on_delete=models.CASCADE)
    house = models.ForeignKey(House,null=True,blank=True,related_name='roles',on_delete=models.CASCADE)
    apartment_building = models.ForeignKey(ApartmentBuilding,null=True,blank=True,related_name='roles',on_delete=models.CASCADE)
    terrain = models.ForeignKey(Terrain,null=True,blank=True,related_name='roles',on_delete=models.CASCADE)

@reversion.register()
class Appraisal(models.Model):
    '''
    Hola
    '''

    real_estates = models.ManyToManyField(RealEstate)
    real_estate_main = models.ForeignKey(RealEstate,null=True,on_delete=models.CASCADE, related_name='appraisals_main') # To speed up lookups
    property_main = models.ForeignKey(AppProperty,null=True,on_delete=models.CASCADE, related_name='appraisals_main') # To speed up lookups

    timeRequest = models.DateTimeField("Time created",blank=True,null=True)
    timeDue = models.DateTimeField("Time due",blank=True,null=True)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
    timeModified = models.DateTimeField("Time modified",blank=True,null=True)
    timeFinished = models.DateTimeField("Time finished",blank=True,null=True)
    timePaused = models.DateTimeField("Time paused",blank=True,null=True)

    STATE_IMPORTED = 0
    STATE_PAUSED = 2
    STATE_FINISHED = 3
    STATE_NOT_ASSIGNED = 4
    STATE_NOT_ACCEPTED = 5
    STATE_IN_APPRAISAL = 1
    STATE_IN_REVISION = 6
    STATE_SENT = 7
    STATE_ARCHIVED = 8
    STATE_ABORTED = 9
    STATES = (
        (STATE_IMPORTED,'imported'),
        (STATE_NOT_ASSIGNED,'not assigned'),
        (STATE_NOT_ACCEPTED,'not accepted'),
        (STATE_IN_APPRAISAL,'in appraisal'),
        (STATE_IN_REVISION,'in revision'),
        (STATE_SENT,'sent'),
        (STATE_ARCHIVED,'archivada'),
        (STATE_ABORTED,'abortada'),
        (STATE_PAUSED,'paused'),
        (STATE_FINISHED,'finished')
    )
    state = models.IntegerField("Estado",choices=STATES,null=True)

    in_conflict = models.BooleanField("En conflicto",default=False,null=False)

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
    solicitanteEjecutivoTelefono = models.CharField("Solicitante teléfono",max_length=30,blank=True,null=True)

    cliente = models.CharField("Cliente",max_length=100,blank=True,null=True)
    clienteRut = models.CharField("Cliente RUT",max_length=13,blank=True,null=True)
    clienteEmail = models.CharField("Cliente Email",max_length=100,blank=True,null=True)
    clienteTelefono = models.CharField("Cliente Teléfono",max_length=30,blank=True,null=True)
    clienteValidado = models.BooleanField("Cliente validado",blank=True,null=False,default=False)

    contacto = models.CharField("Contacto",max_length=100,blank=True,null=True)
    contactoRut = models.CharField("Contacto RUT",max_length=13,blank=True,null=True)
    contactoEmail = models.CharField("Contacto Email",max_length=100,blank=True,null=True)
    contactoTelefono = models.CharField("Contacto Teléfono",max_length=30,blank=True,null=True)
    contactoValidado = models.BooleanField("Cliente validado",blank=True,null=False,default=False)

    propietario = models.CharField("Propietario",max_length=100,blank=True,null=True)
    propietarioRut = models.CharField("Propietario RUT",max_length=13,blank=True,null=True)
    propietarioEmail = models.CharField("Contacto Email",max_length=100,blank=True,null=True)
    propietarioTelefono = models.CharField("Contacto Teléfono",max_length=30,blank=True,null=True)
    propietarioReferenceSII = models.BooleanField("Propietario Referencia SII",blank=True,default=False)
    
    tasadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_tasador')

    visadorUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='appraisals_visador')
    visadorEmpresa = models.CharField("Visador empresa",max_length=100,blank=True,null=True)
    visadorEmpresaMail = models.EmailField("Visador empresa mail",max_length=100,blank=True,null=True)

    roles = models.ManyToManyField(Rol)

    orderFile = models.FileField("Documento pedido",upload_to='orders/',null=True,blank=True)

    photos = models.ManyToManyField(Photo)

    documents = models.ManyToManyField(Document)

    commentsOrder = models.CharField("Comentarios pedido",max_length=1000,null=True,blank=True)

    descripcionSector = models.TextField("Descripción sector",max_length=10000,default="",null=True,blank=True)
    descripcionPlanoRegulador = models.TextField("Descripción plano regulador",max_length=10000,default="",null=True,blank=True)
    descripcionExpropiacion = models.TextField("Descripción expropiación",max_length=10000,default="",null=True,blank=True)

    # valor
    valorUF = models.FloatField("Valor UF", blank=True,null=True)

    @cached_property
    def address(self):
        address = self.real_estates.first().address
        rss = self.real_estates.count()
        if rss > 1:
            address += " (+"+str(rss-1)+")"
        return address

    @cached_property
    def address_no_region(self):
        address = self.real_estate_main.address_no_region
        #rss = self.real_estates.count()
        #if rss > 1:
        #    address += " (+"+str(rss-1)+")"
        return address

    @cached_property
    def status_verbose(self):
        return str([state[1] for state in self.STATES if state[0] == self.state][0])

    @cached_property
    def hasTasador(self):
        print(self.tasadorUser)

    @cached_property
    def not_assigned(self):
        if self.state == self.STATE_NOT_ASSIGNED:
            return True
        else:
            return False

    @cached_property
    def finished(self):
        if self.state == self.STATE_FINISHED:
            return True
        else:
            return False

    @cached_property
    def in_appraisal(self):
        if self.state == self.STATE_IN_APPRAISAL:
            return True
        else:
            return False

    @cached_property
    def paused(self):
        if self.state == self.STATE_PAUSED:
            return True
        else:
            return False

    @cached_property
    def timeDueReal(self):
        if self.state == self.STATE_PAUSED:
            if self.timePaused != None:
                return self.timeDue+(datetime.datetime.now(datetime.timezone.utc)-self.timePaused)
            else:
                return self.timeDue
        else:
            return self.timeDue

    @cached_property
    def url(self):
        return "/appraisal/{}/".format(self.id)

    @cached_property
    def daySinceCreated(self):
        today = datetime.date.today()
        diff  = today - self.timeCreated.date()
        return diff.days

    @cached_property
    def is_appraisalOverdue(self):
        if self.timeDue < datetime.date.today():
            return True
        return False

    @cached_property
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

    @cached_property
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

    @cached_property
    def timeLeft(self):
        return self.timeDue - self.timeCreated

    @cached_property
    def daysLeft(self):
        today = datetime.date.today()
        if self.timeDue:
            diff  = self.timeDue.date()-today
            return diff.days
        else:
            return None

    def addComment(self,event_id,user,timeCreated,text=None):
        comment = Comment(event=event_id,user=user,timeCreated=timeCreated)
        if text and len(text) > 0:
            comment.text = text
        comment.save()
        self.comments.add(comment)
        self.save()
        return comment

    def addAppProperty(self,property_type,property_id):
        app_property = AppProperty(property_type=property_type,property_id=property_id,appraisal=self)
        app_property.save()
        return app_property

    def getCommentChoices(self,comments=None,state=None):
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

        event_choices = Comment.event_choices_state[state]
        print(event_choices)

        # already commented
        comment_ids = comments.values_list('event',flat=True)

        event_choices = [x for x in event_choices if x not in comment_ids or (x in comment_ids and x not in once_ids)]
        event_choices = [x for x in Comment.event_choices if x[0] in event_choices]
        print(event_choices)
        return event_choices

    def buildings(self):
        buildings = []
        for prop in self.appproperty_set.all():
            bld = prop.get_building()
            if bld != None:
                buildings.append(bld)
        return buildings

    def getAppraisalPrice(self):
        precios = Price.objects.get_related
        return

    class Meta:
        app_label = 'appraisal'
        permissions = (
            ("assign_tasador", "Can assign tasadores"),
            ("assign_visador", "Can assign visadores"),
            ("validate_contact", "Can validate contacts"))

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name.name)
            yield (field_name.name, value)

class AppProperty(models.Model):
    
    property_type = models.PositiveIntegerField(choices=Building.propertyType_choices,default=Building.TYPE_OTRO)
    property_id = models.PositiveIntegerField()
    appraisal = models.ForeignKey(Appraisal,on_delete=models.CASCADE)

    def is_apartment(self):
        if self.property_type == Building.TYPE_DEPARTAMENTO:
            return True
        else:
            return False

    def get_property(self):
        if self.property_type == Building.TYPE_DEPARTAMENTO:
            return Apartment.objects.get(id=self.property_id)
        elif self.property_type == Building.TYPE_CASA:
            return House.objects.get(id=self.property_id)
        elif self.property_type == Building.TYPE_EDIFICIO:
            return ApartmentBuilding.objects.get(id=self.property_id)
        elif self.property_type == Building.TYPE_TERRENO:
            return Terrain.objects.get(id=self.property_id)

    def get_building(self):
        if self.property_type == Building.TYPE_DEPARTAMENTO:
            return Apartment.objects.get(id=self.property_id).apartment_building.building
        elif self.property_type == Building.TYPE_CASA:
            return House.objects.get(id=self.property_id).building
        elif self.property_type == Building.TYPE_EDIFICIO:
            return ApartmentBuilding.objects.get(id=self.property_id).building
        else:
            return None

    def propertyTypeIcon(self):
        return Building.property_type_icon[self.property_type]

class Comment(models.Model):
    EVENT_CONTACTO_VALIDADO = 1
    EVENT_CONTACTO_INVALIDADO = 30
    EVENT_SOLICITUD_ACEPTADA = 2
    EVENT_SOLICITUD_RECHAZADA = 6
    EVENT_VISITA_ACORDADA = 3
    EVENT_PROPIEDAD_VISITADA = 4
    EVENT_ENVIADA_A_VISADOR = 5
    EVENT_ENTREGADO_AL_CLIENTE = 8
    EVENT_CLIENTE_VALIDADO = 9
    EVENT_CLIENTE_INVALIDADO = 29
    EVENT_CONTABILIZACION = 10
    EVENT_ABORTADO = 18
    EVENT_INCIDENCIA = 19
    EVENT_CORRECCION_INFORME = 20
    EVENT_OBSERVACION_VISADOR = 21
    EVENT_OBJECION = 22
    EVENT_TASADOR_SOLICITADO = 23
    EVENT_TASADOR_DESASIGNADO = 25
    EVENT_VISADOR_ASIGNADO = 26
    EVENT_VISADOR_DESASIGNADO = 27
    EVENT_TASACION_INGRESADA = 24
    EVENT_COMENTARIO = 28
    EVENT_OTRO = 0
    event_choices = (
        (EVENT_CONTACTO_VALIDADO, "Contacto validado"),
        (EVENT_CONTACTO_INVALIDADO, "Contacto invalidado"),
        (EVENT_CLIENTE_VALIDADO, "Cliente validado"),
        (EVENT_CLIENTE_INVALIDADO, "Cliente invalido"),
        (EVENT_TASADOR_SOLICITADO, "Tasador solicitado"),
        (EVENT_SOLICITUD_ACEPTADA, "Solicitud de tasador aceptada"),
        (EVENT_SOLICITUD_RECHAZADA, "Solicitud de tasador rechazada"),
        (EVENT_TASADOR_DESASIGNADO, "Tasador desasignado"),
        (EVENT_VISADOR_ASIGNADO, "Visador asignado"),
        (EVENT_VISADOR_DESASIGNADO, "Visador desasignado"),
        (EVENT_TASACION_INGRESADA, "Tasación ingresada"),
        (EVENT_VISITA_ACORDADA, "Visita acordada"),
        (EVENT_PROPIEDAD_VISITADA, "Propiedad visitada"),
        (EVENT_ENVIADA_A_VISADOR, "Enviado a visador"),
        (EVENT_ENTREGADO_AL_CLIENTE, "Entregado al cliente"),
        (EVENT_CONTABILIZACION, "Contabilización"),
        (EVENT_INCIDENCIA, "Incidencia"),
        (EVENT_CORRECCION_INFORME, "Corrección informe"),
        (EVENT_OBSERVACION_VISADOR, "Observación visador"),
        (EVENT_COMENTARIO, "Comentario"),
        (EVENT_OTRO, "Otro")
    )
    event_choices_state = {
        Appraisal.STATE_NOT_ASSIGNED:[
            EVENT_VISITA_ACORDADA,
            EVENT_INCIDENCIA,
            EVENT_COMENTARIO
        ],
        Appraisal.STATE_NOT_ACCEPTED:[
            EVENT_VISITA_ACORDADA,
            EVENT_INCIDENCIA,
            EVENT_COMENTARIO
        ],
        Appraisal.STATE_IN_APPRAISAL:[
            EVENT_VISITA_ACORDADA,
            EVENT_PROPIEDAD_VISITADA,
            EVENT_ENVIADA_A_VISADOR,
            EVENT_INCIDENCIA,
            EVENT_COMENTARIO
        ],
        Appraisal.STATE_IN_REVISION:[
            EVENT_ENTREGADO_AL_CLIENTE,
            EVENT_INCIDENCIA,
            EVENT_COMENTARIO
        ],
        Appraisal.STATE_SENT:[
            EVENT_COMENTARIO
        ]
    }
    event = models.IntegerField(choices=event_choices,default=0,blank=False,null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    text = models.CharField("Comment",max_length=500)
    conflict = models.BooleanField("Incidencia",default=False)
    timeCreated = models.DateTimeField("Time created",blank=True,null=True)
    appraisal = models.ForeignKey(Appraisal,on_delete=models.CASCADE, blank=True, null=True, related_name="comments")

    @property
    def incidencia(self):
        return self.event == self.EVENT_INCIDENCIA
    @property
    def deletable(self):
        return self.event != self.EVENT_TASACION_INGRESADA
    
    def hasText(self):
        if self.text == "" or self.text == None:
            return False
        else:
            return True

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


class AppraiserExpenses(models.Model):
    description = models.CharField("Descripcion del gasto", null=False, blank=True, max_length=1000)
    totalPrice = models.IntegerField(default=0, blank=False, null=False)
    appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.totalPrice