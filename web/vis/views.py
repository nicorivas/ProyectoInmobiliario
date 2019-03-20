from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q

from region.models import Region
from commune.models import Commune
from collections import OrderedDict
from realestate.models import RealEstate
#from apartment.models import Apartment

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

    trace = go.Scatter(x=x, y=y, mode="markers",  name='1st Trace')

    data = trace
    layout=go.Layout(title="Providencia", xaxis={'title':'Built square meters'}, yaxis={'title':'Market price'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    context = {'graph':div}

    return render(request, 'vis/graph.html', context)

def map(request):

    apts = Apartment.objects.only('lat','lng','name').all()

    x = np.array(apts.values_list('lat',flat=True))
    y = np.array(apts.values_list('lng',flat=True))
    text = list(apts.values_list('name',flat=True))

    p_scatter = go.Scatter(
        x=x,
        y=y,
        mode="markers",
        name='1st Trace',
        text=text)

    # create our callback function
    def updatePoint(trace, points, selector):
        c = list(scatter.marker.color)
        s = list(scatter.marker.size)
        for i in points.point_inds:
            c[i] = '#bae2be'
            s[i] = 20
            scatter.marker.color = c
            scatter.marker.size = s
    p_scatter.on_click(updatePoint)

    data = [p_scatter]

    layout = go.Layout(
        title="Propiedades en Santiago",
        xaxis={'title':'lat'},
        yaxis={'title':'lng'},
        hovermode='closest')

    figure = go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    context = {'graph':div}

    return render(request, 'vis/graph.html', context)


def summary_country(request):

    regions = Region.objects.all()

    total = {}
    total['apartment'] = 0
    for region in regions:
        total['apartment'] += region.dataApartmentCount

    context = {'regions':regions,'total':total}

    return render(request, 'vis/summary_country.html', context)

def summary_region(request,region_id):

    region = Region.objects.get(code=region_id)
    communes = Commune.objects.filter(region=region)

    context = {'region':region, 'communes':communes}

    return render(request, 'vis/summary_region.html', context)

def summary_commune(request,region_id,commune_id):

    commune = Commune.objects.get(code=commune_id)
    apts = Apartment.objects.filter(addressCommune=commune)
    apts = list(apts)
    apts = sorted(apts, key=lambda t: t.addressShort)
    context = {'commune':commune,'apts':apts}

    return render(request, 'vis/summary_commune.html', context)
