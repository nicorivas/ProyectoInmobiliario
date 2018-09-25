from django.db import models

class Property(models.Model):

    PROPERTY_TYPE_UNDEFINED = 0
    PROPERTY_TYPE_HOUSE = 1
    PROPERTY_TYPE_APARTMENT = 2
    PROPERTY_TYPE_BUILDING = 3
    propertyType_choices = [
        (PROPERTY_TYPE_UNDEFINED, "Indefinido"),
        (PROPERTY_TYPE_HOUSE, "Casa"),
        (PROPERTY_TYPE_APARTMENT, "Departamento"),
        (PROPERTY_TYPE_BUILDING, "Edificio")]

    propertyType = models.PositiveIntegerField(
        choices=propertyType_choices,
        default=PROPERTY_TYPE_UNDEFINED)

    class Meta:
        abstract = True
