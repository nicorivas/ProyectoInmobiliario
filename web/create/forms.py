from django import forms
from data.chile import comunas_regiones
from region.models import Region
from commune.models import Commune
from realestate.models import RealEstate
from django.core.exceptions import ValidationError
import datetime

class AppraisalCreateForm(forms.Form):

    propertyType_create = forms.ChoiceField(
        label="Tipo propiedad",
        choices=RealEstate.propertyType_choices,
        initial=RealEstate.TYPE_UNDEFINED)
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

    addressStreet_create = forms.CharField(
        max_length=200,
        label="Calle",
        error_messages={'required': 'Please enter your name'})
    addressStreet_create.widget.attrs.update({'class':"form-control"})

    addressNumber_create = forms.CharField(max_length=6,label="Número")
    addressNumber_create.widget.attrs.update({'class':"form-control"})

    addressNumberFlat_create = forms.CharField(max_length=6,label="Depto.",required=False)
    addressNumberFlat_create.widget.attrs.update({'class':"form-control",'disabled':''})

    appraisalTimeFrame_create = forms.DateTimeField(
        initial=datetime.datetime.now().strftime("%Y-%m-%d"),
        label="Plazo",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control datetimepicker-input",
                   'data-target':"#datetimepicker1"}))
    appraisalTimeFrame_create.input_formats = ['%d/%m/%Y %H:%M']


    appraisalPrice_create = forms.FloatField(label="Precio")
    appraisalPrice_create.widget.attrs.update({'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['addressCommune_create'].queryset = []

    def clean(self):
        if self.cleaned_data.get('addressStreet_create')=="":
            raise forms.ValidationError('No name!')
        if self.cleaned_data.get('addressNumberFlat_create').strip()=="":
            raise forms.ValidationError('No hay número de departamento (quizás puso sólo un espacio)')
        return self.cleaned_data

    def clean_appraisalTimeFrame_create(self):
        data = self.cleaned_data['appraisalTimeFrame_create']
        # Check date is not in past.
        if data.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
            raise forms.ValidationError(('Plazo se debe fijar en el futuro'), code='invalid')
        # Remember to always return the cleaned data.
        return data
