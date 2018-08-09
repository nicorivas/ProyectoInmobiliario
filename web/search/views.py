from django.views.generic import FormView
from django.shortcuts import render
from .models import Building
from .forms import LocationSearchForm
from .forms import CreateProperty
from django.core import serializers

def search(request):
    form_search = LocationSearchForm
    form_create = CreateProperty

    # Get buildings to be displayed on map
    buildings = Building.objects.all()
    buildings_json = serializers.serialize("json", Building.objects.all())
    context = {
        'buildings':buildings,
        'buildings_json': buildings_json,
        'form_search':form_search,
        'form_create':form_create}
    return render(request, 'search/index.html', context)
