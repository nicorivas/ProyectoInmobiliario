from django.db import models

class Building(models.Model):

    real_estate = models.ForeignKey('realestate.RealEstate', on_delete=models.CASCADE,verbose_name="Real estate",blank=False,null=False)

    TYPE_NONE = ''
    TYPE_OTRO = 0
    TYPE_CASA = 1
    TYPE_DEPARTAMENTO = 2
    TYPE_OFICINA = 6
    TYPE_LOCAL_COMERCIAL = 7
    TYPE_TERRENO = 8
    TYPE_INDUSTRIA = 9
    TYPE_GALPON = 10
    TYPE_BODEGA = 11
    TYPE_ESTACIONAMIENTO = 12
    TYPE_EDIFICIO = 3
    TYPE_PARCELA = 13
    TYPE_BARCO = 14
    TYPE_VEHICULO = 15
    TYPE_MAQUINARIA = 16
    TYPE_ESTACION_DE_SERVICIO = 17
    TYPE_CONDOMINIO = 18
    propertyType_choices = [
        (TYPE_NONE,'---------'),
        (TYPE_TERRENO, "Terreno"),
        (TYPE_CASA, "Casa"),
        (TYPE_EDIFICIO, "Edificio"),
        (TYPE_DEPARTAMENTO, "Departamento"),
        (TYPE_OFICINA, "Oficina"),
        (TYPE_LOCAL_COMERCIAL, "Local Comercial"),
        (TYPE_INDUSTRIA, "Industria"),
        (TYPE_GALPON, "Galpon"),
        (TYPE_BODEGA, "Bodega"),
        (TYPE_ESTACIONAMIENTO, "Estacionamiento"),
        (TYPE_PARCELA, "Parcela"),
        (TYPE_BARCO, "Barco"),
        (TYPE_VEHICULO, "Vehiculo"),
        (TYPE_MAQUINARIA, "Maquinaria"),
        (TYPE_ESTACION_DE_SERVICIO, "Estación de Servicio"),
        (TYPE_CONDOMINIO, "Condominio"),
        (TYPE_OTRO, "Otro"),]
    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=TYPE_OTRO)

    name = models.CharField("Nombre",max_length=300,default="",blank=True)

    marketPrice = models.DecimalField("Precio mercado UF",max_digits=10,decimal_places=2,null=True,blank=True)

    BOOLEAN_NULL_CHOICES = (
        (1, "S/A"),
        (2, "Si"),
        (3, "No")
    )
    mercadoObjetivo = models.PositiveSmallIntegerField("Mercado objetivo",blank=True,null=False,default=1,choices=BOOLEAN_NULL_CHOICES)

    anoConstruccion = models.IntegerField("Año construcción",
        blank=True,
        null=True)

    vidaUtilRemanente = models.IntegerField("Vida util remanente",
        blank=True,
        null=True)

    avaluoFiscal = models.FloatField("Avaluo fiscal",
        blank=True,
        null=True)

    dfl2 = models.PositiveSmallIntegerField("DFL 2",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    SELLO_VERDE_CHOICES = (
        ('V', 'Verde'),
        ('A', 'Amarillo'),
        ('AV', 'Amarillo Vencido'),
        ('R', 'Rojo'),
        ('NA', 'No Aplica'),
        ('VV', 'Verde vencido'),
        ('SA', 'Sin antecedentes')
    )
    selloVerde = models.CharField("Sello verde",
        max_length=2,
        choices=SELLO_VERDE_CHOICES,
        blank=True,
        null=True)

    copropiedadInmobiliaria = models.PositiveSmallIntegerField("Copropiedad Inmobiliaria",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    OCUPANTE_CHOICES = (
        ('P', 'Propietario'),
        ('A', 'Arrendatario'),
        ('O', 'Otro'),
        ('SO', 'Sin ocupante')
    )
    ocupante = models.CharField("Ocupante",
        max_length=2,
        choices=OCUPANTE_CHOICES,
        blank=True,
        null=True)

    tipoBien = models.CharField("Tipo de bien",
        max_length=20,
        blank=True,
        null=True)

    DESTINO_SII = (
        ('H', 'Habitacional'),
        ('O', 'Oficina'),
        ('C', 'Comercio'),
        ('I', 'Industria'),
        ('L', 'Bodega'),
        ('Z', 'Estacionamiento'),
        ('D', 'Deportes y Recreación'),
        ('E', 'Educación y Cultura'),
        ('G', 'Hotel, Motel'),
        ('P', 'Administración pública'),
        ('Q', 'Culto'),
        ('S', 'Salud'),
        ('SE', 'Sitio Eriazo')
    )
    destinoSII = models.CharField("Destino según SII",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    usoActual = models.CharField("Uso actual",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    usoFuturo = models.CharField("Uso futuro",
        max_length=1,
        choices=DESTINO_SII,
        blank=True,
        null=True)

    permisoEdificacionNo = models.CharField("Permiso edificación",
        max_length=20,
        blank=True,
        null=True)
    permisoEdificacionFecha = models.DateField("Fecha permiso edificación",
        blank=True,
        null=True)
    permisoEdificacionSuperficie = models.DecimalField("Superficie permiso edificación",
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True)

    recepcionFinalNo = models.CharField("Recepcion final",
        max_length=20,
        blank=True,
        null=True)
    recepcionFinalFecha = models.DateField("Recepcion final fecha",
        blank=True,
        null=True)

    expropiacion = models.PositiveSmallIntegerField("Expropiacion",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    viviendaSocial = models.PositiveSmallIntegerField("Vivienda social",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    desmontable = models.PositiveSmallIntegerField("Desmontable",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    adobe = models.PositiveSmallIntegerField("Adobe",
        blank=True,
        null=False,
        default=1,
        choices=BOOLEAN_NULL_CHOICES)

    acogidaLeyChoices = (
        (0, 'O.G.U. y C.'),
        (1, 'P.R.C.'),
        (2, 'Ley Pereira'),
        (3, 'Ley 19583'),
        (4, 'Ley 19667'),
        (5, 'Ley 19727'),
        (6, 'Ley 20251'),
        (7, 'Ley 6071'),
        (8, 'Ninguna'),
        (9, 'Antigüedad')
    )
    acogidaLey = models.IntegerField("Acogida a",
        choices=acogidaLeyChoices,
        blank=True,
        null=True)

    USE = (
        (0,'Usada'),
        (1,'Nueva'),
        (3, 'No Aplica')
    )
    tipoPropiedad = models.PositiveSmallIntegerField("Tipo de propiedad",
        choices=USE,
        default=0,
        null=True)

    antiguedad = models.PositiveSmallIntegerField("Antiguedad",
        default=0,
        null=True)

    vidaUtil = models.PositiveSmallIntegerField("Vida util",
        default=80,
        null=True)

    complementary = models.BooleanField("Complementaria",blank=True,default=False)

    MATERIAL_UNKNOWN = '-'
    MATERIAL_ACERO = 'A'
    MATERIAL_HORMIGON = 'B'
    MATERIAL_ALBANILERIA = 'C'
    MATERIAL_PIEDRA_BLOQUE = 'D'
    MATERIAL_MADERA = 'E'
    MATERIAL_ADOBE = 'F'
    MATERIAL_METALCOM = 'G'
    MATERIAL_PREFAB_MADERA = 'H'
    MATERIAL_PREFAB_HORMIGON = 'I'
    MATERIAL_OTRO = 'J'
    MATERIAL_CHOICES = [
        (MATERIAL_UNKNOWN, "Desconocido"),
        (MATERIAL_ACERO, "Acero"),
        (MATERIAL_HORMIGON, "Hormigón"),
        (MATERIAL_ALBANILERIA, "Albañilería"),
        (MATERIAL_PIEDRA_BLOQUE, "Piedra/Bloque"),
        (MATERIAL_MADERA, "Madera"),
        (MATERIAL_ADOBE, "Adobe"),
        (MATERIAL_METALCOM, "Metalcom"),
        (MATERIAL_PREFAB_MADERA, "Prefab. Madera"),
        (MATERIAL_PREFAB_HORMIGON, "Prefab. Hormigón"),
        (MATERIAL_OTRO, "Otros")]
    material = models.CharField(
        max_length=2,
        blank=True,
        choices=MATERIAL_CHOICES,
        default=MATERIAL_UNKNOWN)

    year = models.DateField("Año construcción",blank=True,null=False,default='1985-01-01')

    quality = models.IntegerField("Calidad",blank=True,null=True,choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])

    state = models.IntegerField("Estado",blank=True,null=True,choices=[(1,'Sin valor'),(2,'Malo'),(3,'Regular'),(4,'Bueno'),(5,'Muy bueno')])

    rol = models.CharField("Rol",max_length=20,blank=True,null=True)

    BOOLEAN_NULL_CHOICES = (
        (None, "S/A"),
        (True, "Si"),
        (False, "No")   
    )
    prenda = models.BooleanField("Mercado objetivo",blank=True,null=True,choices=BOOLEAN_NULL_CHOICES)

    RECEPCION_CONRF = 0
    RECEPCION_SINRF = 1
    RECEPCION_SINPE = 2
    RECEPCION_SINANT = 3
    RECEPCION_NR = 4
    RECEPCION_CHOICES = [
        (RECEPCION_CONRF, "Con R/F"),
        (RECEPCION_SINRF, "Sin R/F"),
        (RECEPCION_SINPE, "Sin P/E"),
        (RECEPCION_SINANT, "Sin Ant."),
        (RECEPCION_NR, "N/R")]
    recepcion = models.IntegerField(
        choices=RECEPCION_CHOICES,
        default=RECEPCION_NR,
        blank=True)

    area = models.FloatField("Area",
        blank=True,
        null=False,
        default=0)
    
    UFPerArea = models.FloatField("Area",
        blank=True,
        null=False,
        default=0)

    @property
    def is_apartment(self):
        # Casting to int is done so that it also works when called in javascript.
        return int(self.propertyType == Building.TYPE_DEPARTAMENTO)

    @property
    def is_house(self):
        return int(self.propertyType == Building.TYPE_CASA)

    @property
    def is_apartmentbuilding(self):
        return int(self.propertyType == Building.TYPE_EDIFICIO)

    @property
    def generic_name(self):
        if self.is_apartmentbuilding:
            return "Edificio "+self.apartmentbuilding.addressNumber2
        elif self.is_house:
            return "Casa "+self.house.addressNumber2

    @property
    def name_or_generic(self):
        if self.name:
            return self.name
        else:
            return self.generic_name

