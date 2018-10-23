from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q

from collections import OrderedDict
from realestate.models import RealEstate
from apartment.models import Apartment
from commune.models import Commune

import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np

def vis(request):

    apts = Apartment.objects.exclude(Q(marketPrice__isnull=True)|Q(builtSquareMeters__isnull=True))
    marketPrice = list(apts.values_list('marketPrice', flat=True))
    builtSquareMeters = list(apts.values_list('builtSquareMeters', flat=True))
    marketPrice = [float(x) for x in marketPrice]
    builtSquareMeters = [float(x) for x in builtSquareMeters]

    x = np.array(builtSquareMeters)
    y = np.array(marketPrice)

    #template_name = 'graph.html'

    trace1 = go.Scatter(x=x, y=y, mode="markers",  name='1st Trace')

    data=go.Data([trace1])
    layout=go.Layout(title="Providencia", xaxis={'title':'Built square meters'}, yaxis={'title':'Market price'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    context = {'graph':div}

    return render(request, 'vis/graph.html', context)

def summary_region(request,region_id):

    communes = Commune.objects.filter(region=13)

    apts = Apartment.objects.all()
    commune_apts = {}
    for commune in communes:
        commune_apts[commune] = apts.filter(addressCommune=commune)

    commune_apts = OrderedDict(sorted(commune_apts.items(), key=lambda t: t[0].name))

    context = {'apts':apts, 'commune_apts':commune_apts}

    return render(request, 'vis/summary_region.html', context)

def summary_commune(request,region_id,commune_id):

    commune = Commune.objects.get(code=commune_id)
    apts = Apartment.objects.filter(addressCommune=commune)
    apts = list(apts)
    print(apts)
    apts = sorted(apts, key=lambda t: t.addressShort)
    context = {'commune':commune,'apts':apts}

    return render(request, 'vis/summary_commune.html', context)
