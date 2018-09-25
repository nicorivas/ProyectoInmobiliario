from django import forms
from data.chile import comunas_regiones
from region.models import Region
from commune.models import Commune
from property.models import Property

class LocationSearchForm(forms.Form):

    address = forms.CharField(max_length=200,label="")
    address.widget.attrs.update({'placeholder':'Buscar'})
    address.widget.attrs.update({'class':"form-control"})

class AppraisalCreateForm(forms.Form):

    propertyType_create = forms.ChoiceField(
        label="Tipo propiedad",
        choices=Property.propertyType_choices,
        initial=Property.PROPERTY_TYPE_APARTMENT)
    propertyType_create.widget.attrs.update({'class':"form-control"})

    addressRegion_create = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.all())
    addressRegion_create.widget.attrs.update({'class':"form-control"})
    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune_create = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.all())
    addressCommune_create.widget.attrs.update({'class':"form-control"})
    addressStreet_create = forms.CharField(max_length=200,label="Calle")
    addressStreet_create.widget.attrs.update({'class':"form-control"})
    addressNumber_create = forms.CharField(max_length=6,label="Número")
    addressNumber_create.widget.attrs.update({'class':"form-control"})
    addressNumberFlat_create = forms.CharField(max_length=6,label="Depto.",required=False)
    addressNumberFlat_create.widget.attrs.update({'class':"form-control"})
    appraisalTimeFrame_create = forms.IntegerField(max_value=900, label="Plazo")
    appraisalTimeFrame_create.widget.attrs.update({'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['addressCommune_create'].queryset = []
