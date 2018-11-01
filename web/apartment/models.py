from django.db import models
from realestate.models import RealEstate
from building.models import Building

#from appraisal.models import Appraisal
#from django.contrib.contenttypes.fields import GenericRelation

class Apartment(RealEstate):

    ORIENTATIONS = (
        ('N', 'Norte'),
        ('NE', 'Norponiente'),
        ('E', 'Poniente'),
        ('SE', 'Surponiente'),
        ('S', 'Sur'),
        ('WS', 'Suroriente'),
        ('W', 'Oriente'),
        ('NW', 'Nororiente')
    )
    
    building_in = models.ForeignKey(Building, on_delete=models.CASCADE,verbose_name="Edificio",blank=False,null=False)
    
    number = models.CharField("Numero",max_length=10,null=True)
    floor = models.PositiveSmallIntegerField("Piso",null=True,blank=True)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    usefulSquareMeters = models.DecimalField("Superficie util",max_digits=7,decimal_places=2,null=True,blank=True)
    terraceSquareMeters = models.DecimalField("Superficie terraza", max_digits=7, decimal_places=2, null=True, blank=True)
    orientation = models.CharField("Orientacion",max_length=2,choices=ORIENTATIONS,null=True,blank=True)
    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    @property
    def sourceNameNice(self):
        "Returns source to be printed in a nice way."
        if self.sourceName == 'toctoc':
            return 'TocToc'
        elif self.sourceName == 'portali':
            return 'P.I.'
        else:
            return self.sourceName

    class Meta:
        app_label = 'apartment'

    def __init__(self, *args, **kwargs):
        super(Apartment, self).__init__(*args, **kwargs)
        self.propertyType=RealEstate.TYPE_APARTMENT
