from django.db import models
from building.models import Building

# Agrupación general de propiedades.
# Definición popular, por un nombre.
class Condominium(models.Model):

    similar = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    
    name = models.TextField("Nombre",max_length=500,default="",null=True,blank=True)

    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    marketPrice = models.DecimalField("Precio mercado",max_digits=10,decimal_places=2,null=True,blank=True)

    TYPE_OTRO = 0
    TYPE_CONDOMINIO = 1
    TYPE_POBLACION = 2
    TYPE_SECTOR = 3
    TYPE_VILLA = 4
    TYPE_CERRO = 5
    TYPE_CONJUNTO_HABITACIONAL = 6
    TYPE_FUNDO = 7
    ctype_choices = [
        (TYPE_CONDOMINIO, "Condominio"),
        (TYPE_POBLACION, "Población"),
        (TYPE_SECTOR, "Sector"),
        (TYPE_VILLA, "Villa"),
        (TYPE_CERRO, "Cerro"),
        (TYPE_CONJUNTO_HABITACIONAL, "Conjunto Habitacional"),
        (TYPE_FUNDO, "Fundo"),
        (TYPE_OTRO, "Otro"),]
    ctype = models.PositiveIntegerField(
        choices=ctype_choices,
        default=TYPE_OTRO)
    ctype_choices_form = ctype_choices
    ctype_choices_form.insert(0,('','----'))

    @property 
    def generic_name(self):
        return "Condominio"

    @property
    def name_or_generic(self):
        return self.generic_name

    @property
    def propertyType(self):
        return Building.TYPE_CONDOMINIO

    @property
    def propertyTypeIcon(self):
        return "fas fa-home"