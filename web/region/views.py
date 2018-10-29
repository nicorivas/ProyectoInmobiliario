from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils.text import slugify

from region.models import Region

import json

def region(request,code=0):

    if request.method == 'POST':
        '''
        Nothing to be done
        '''
    else:
        '''
        Get correct region based on url code. Then fill the context.
        '''
        mpoly = Region.objects.all().filter(code=code).values_list('mpoly')
        # We transfer to geojson because that's what json is about, transfering
        # info to javascript
        geometry_geojson = json.loads(mpoly[0][0].geojson)
        centroid_geojson = json.loads((mpoly[0][0].centroid).geojson)
        context = {
            'coordinates':geometry_geojson['coordinates'],
            'centroid':centroid_geojson['coordinates']
        }

        return render(request, 'region/index.html', context)
