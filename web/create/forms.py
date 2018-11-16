from django import forms
from region.models import Region
from commune.models import Commune
from realestate.models import RealEstate
from appraisal.models import Appraisal
from django.core.exceptions import ValidationError
import datetime


class AppraisalCreateForm(forms.Form):

    tipoTasacion_create = forms.ChoiceField(
        label="Tipo Pedido",
        choices=Appraisal.tipoTasacion_choices)
    tipoTasacion_create.widget.attrs.update({'class': "form-control"})

    objetivo_create = forms.ChoiceField(
        label="Objetivo",
        choices=Appraisal.objective_choices)
    objetivo_create.widget.attrs.update({'class': "form-control"})

    visita_create = forms.ChoiceField(
        label="Visita",
        choices=Appraisal.visit_choices)
    visita_create.widget.attrs.update({'class': "form-control", 'data-validation':"required"})

    solicitante_create = forms.ChoiceField(
        label="Solicitante",
        choices=Appraisal.petitioner_choices)
    solicitante_create.widget.attrs.update({'class': "form-control"})

    solicitanteOther_create = forms.CharField(max_length=100, label="Otro", required=False)
    solicitanteOther_create.widget.attrs.update({'class': "form-control"})

    solicitanteCodigo_create = forms.CharField(max_length=100, label="Solicitante Código", required=False)
    solicitanteCodigo_create.widget.attrs.update({'class': "form-control", 'data-validation':"required"})

    cliente_create = forms.CharField(
        max_length=100,
        label="Nombre Cliente", required=False)
    cliente_create.widget.attrs.update({'class': "form-control",'data-validation':"required"})

    clienteRut_create = forms.CharField(
        max_length=100,
        label="Rut Cliente", required=False)
    clienteRut_create.widget.attrs.update({'class': "form-control",'data-validation':"required rut"})

    propertyType_create = forms.ChoiceField(
        label="Tipo propiedad",
        choices=RealEstate.propertyType_choices,
        initial=RealEstate.TYPE_HOUSE)
    propertyType_create.widget.attrs.update({'class':"form-control"})

    addressRegion_create = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.only('name').all())
    addressRegion_create.widget.attrs.update({'class':"form-control"})

    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune_create = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.only('name').all())
    addressCommune_create.widget.attrs.update({'class':"form-control"})

    addressStreet_create = forms.CharField(
        max_length=200,
        label="Calle")
    addressStreet_create.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber_create = forms.CharField(max_length=6,label="Número")
    addressNumber_create.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber2_create = forms.CharField(max_length=6,label="Depto.",required=False)
    addressNumber2_create.widget.attrs.update({'class':"form-control"})

    appraisalTimeFrame_create = forms.DateTimeField(
        initial=datetime.datetime.now().strftime("%Y-%m-%d"),
        label="Plazo",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control datetimepicker-input",
                   'data-target':"#datetimepicker1"}))
    appraisalTimeFrame_create.input_formats = ['%d/%m/%Y %H:%M']
    
    appraisalPrice_create = forms.FloatField(label="Precio",required=False)
    appraisalPrice_create.widget.attrs.update({'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['addressCommune_create'].queryset = []

    def clean(self):
        self.cleaned_data['clienteRut_create'] = self.cleaned_data['clienteRut_create'].replace('.','')
        self.cleaned_data['clienteRut_create'] = self.cleaned_data['clienteRut_create'].replace('-','')
        self.cleaned_data['clienteRut_create'] = self.cleaned_data['clienteRut_create'].lower()
        if self.cleaned_data.get('addressStreet_create')=="":
            raise forms.ValidationError('No name!')
        if self.cleaned_data.get('addressStreet_create')=="":
            raise forms.ValidationError('No name!')
        if self.cleaned_data.get('propertyType_create') == RealEstate.TYPE_APARTMENT:
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
