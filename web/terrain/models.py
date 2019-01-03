from django.db import models

class Terrain(models.Model):
    '''
    Parts of the terrain
    '''

    name = models.CharField("Nombre",max_length=300,default="",blank=True)

    similar = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    real_estate = models.ForeignKey('realestate.RealEstate', on_delete=models.CASCADE,verbose_name="Real estate",blank=False,null=False)

    addressNumber2 = models.CharField("Dpto.",max_length=30,null=True,blank=True)

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

    uf_per_area = models.FloatField("UF per Area",blank=True,null=False,default=0)

    marketPrice = models.DecimalField("Precio mercado",max_digits=10,decimal_places=2,null=True,blank=True)

    @property
    def generic_name(self):
        return "Terreno "+self.addressNumber2

    @property
    def name_or_generic(self):
        if self.name:
            return self.name
        else:
            return self.generic_name
    