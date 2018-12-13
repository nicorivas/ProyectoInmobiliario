from django.db import models

class Building(models.Model):
	'''
	Parts of a RealEstate, such as balconies or other parts of a house.
	'''
	name = models.CharField("Nombre",max_length=300,default="",blank=True)

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
