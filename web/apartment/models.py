from django.db import models
from realestate.models import RealEstate
#from building.models import Building
from apartmentbuilding.models import ApartmentBuilding

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
    
    building_in = models.ForeignKey(ApartmentBuilding, on_delete=models.CASCADE,verbose_name="Edificio",blank=False,null=False)
    
    addressNumber2 = models.CharField("Dpto.",max_length=30,null=True,blank=True)
    floor = models.PositiveSmallIntegerField("Piso",null=True,blank=True)
    bedrooms = models.PositiveSmallIntegerField("Dormitorios",null=True,blank=True)
    bathrooms = models.PositiveSmallIntegerField("Baños",null=True,blank=True)
    usefulSquareMeters = models.DecimalField("Superficie util",max_digits=7,decimal_places=2,null=True,blank=True)
    terraceSquareMeters = models.DecimalField("Superficie terraza", max_digits=7, decimal_places=2, null=True, blank=True)
    orientation = models.CharField("Orientación",max_length=2,choices=ORIENTATIONS,null=True,blank=True)
    generalDescription = models.TextField("Descripcion general",max_length=10000,default="",null=True,blank=True)

    @property 
    def usefulSquareMetersVerbose(self):
        if isinstance(self.usefulSquareMeters,type(None)):
            return "-"
        else:
            return "{:10.1f}".format(self.usefulSquareMeters)

    @property 
    def terraceSquareMetersVerbose(self):
        if isinstance(self.terraceSquareMeters,type(None)):
            return "-"
        else:
            return "{:10.1f}".format(self.terraceSquareMeters)

    @property
    def marketPricePerUsefulSquareMeters(self):
        if isinstance(self.usefulSquareMeters,type(None)) or \
           isinstance(self.marketPrice,type(None)):
            return ""
        else:
            x = self.marketPrice/self.usefulSquareMeters
            return "{:10.2f}".format(x)

    @property
    def marketPricePerTotalSquareMeters(self):
        if isinstance(self.marketPrice,type(None)) or \
           isinstance(self.terraceSquareMeters,type(None)) or \
           isinstance(self.usefulSquareMeters,type(None)):
            return ""
        else:
            x = self.marketPrice/(self.usefulSquareMeters+self.terraceSquareMeters)
            return "{:10.2f}".format(x)
    

    class Meta:
        app_label = 'apartment'

    def __init__(self, *args, **kwargs):
        super(Apartment, self).__init__(*args, **kwargs)
        self.propertyType=RealEstate.TYPE_APARTMENT
