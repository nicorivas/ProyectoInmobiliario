from django.contrib.gis.db import models
from region.models import Region

class Province(models.Model):
    name = models.CharField("Nombre",max_length=100)
    code = models.PositiveSmallIntegerField("Code",
        null=False,
        blank=False,
        unique=True)
    region = models.ForeignKey(Region,
        on_delete=models.CASCADE,
        verbose_name="Region",
        blank=False,
        null=False,
        to_field='code')
    mpoly = models.MultiPolygonField(null=True)