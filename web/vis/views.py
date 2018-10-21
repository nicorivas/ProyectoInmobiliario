from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q

from realestate.models import RealEstate
from apartment.models import Apartment

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
    print(x)
    y = np.array(marketPrice)
    print(y)

    #template_name = 'graph.html'

    trace1 = go.Scatter(x=x, y=y, mode="markers",  name='1st Trace')

    data=go.Data([trace1])
    layout=go.Layout(title="Providencia", xaxis={'title':'Built square meters'}, yaxis={'title':'Market price'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')

    context = {'graph':div}

    return render(request, 'vis/graph.html', context)
