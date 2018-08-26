from django.contrib.gis.db import models

class Neighborhood(models.Model):
    mpoly = models.MultiPolygonField()
    
