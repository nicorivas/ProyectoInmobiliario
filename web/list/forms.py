from django import forms
from region.models import Region
from commune.models import Commune
import datetime


class TasadorSearch(forms.Form):

    addressRegion = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.only('name').all(),
        empty_label="Región")
    addressRegion.widget.attrs.update({'class':"form-control"})

    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.only('name').all())
    addressCommune.widget.attrs.update({'class':"form-control"})
