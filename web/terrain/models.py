from django.db import models

class Terrain(models.Model):
    '''
    Parts of the terrain
    '''

    TYPE_TERRAIN = 101

    name = models.CharField("Nombre",max_length=300,default="",blank=True)

    frente = models.FloatField("Frente",blank=True,null=True)

    fondo = models.FloatField("Fondo",blank=True,null=True)

    TOPOGRAPHY_CHOICES = (
        (0, 'Plano'),
        (1, 'Semiplano'),
        (2, 'Pendiente'),
        (3, 'Pendiente abrupta')
    )
    topography = models.IntegerField("Topografía",choices=TOPOGRAPHY_CHOICES,blank=True,null=True)

    SHAPE_CHOICES = (
        (0, 'Regular'),
        (1, 'Irregular'),
    )
    shape = models.IntegerField("Forma",choices=SHAPE_CHOICES,blank=True,null=True)

    area = models.FloatField("Area",blank=True,null=False,default=0)

    rol = models.CharField("Rol",max_length=20,blank=True,null=True)

    uf_per_area = models.FloatField("UF per Area",blank=True,null=False,default=0)