from django import forms
from region.models import Region
from commune.models import Commune
from realestate.models import RealEstate
from appraisal.models import Appraisal
from django.core.exceptions import ValidationError
import datetime


class AppraisalCreateForm(forms.Form):

    archivo = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class':"custom-file-input",'multiple': False}))

    tipoTasacion = forms.ChoiceField(
        label="Tipo Pedido",
        choices=Appraisal.tipoTasacion_choices)
    tipoTasacion.widget.attrs.update({'class': "form-control"})

    finalidad = forms.ChoiceField(
        label="Finalidad",
        choices=Appraisal.objective_choices)
    finalidad.widget.attrs.update({'class': "form-control"})

    visita = forms.ChoiceField(
        label="Visita",
        choices=Appraisal.visit_choices)
    visita.widget.attrs.update({'class': "form-control", 'data-validation':"required"})

    solicitante = forms.ChoiceField(
        label="Solicitante",
        choices=Appraisal.petitioner_choices)
    solicitante.widget.attrs.update({'class': "form-control"})

    solicitanteOther = forms.CharField(max_length=100, label="Otro", required=False)
    solicitanteOther.widget.attrs.update({'class': "form-control"})

    solicitanteCodigo = forms.CharField(max_length=100, label="Código", required=False)
    solicitanteCodigo.widget.attrs.update({'class': "form-control", 'data-validation':"required"})

    solicitanteSucursal = forms.CharField(max_length=100, label="Sucursal", required=False)
    solicitanteSucursal.widget.attrs.update({'class': "form-control", 'data-validation':"required"})

    solicitanteEjecutivo = forms.CharField(
        max_length=100,
        label="Ejecutivo",
        required=False)
    solicitanteEjecutivo.widget.attrs.update({'class': "form-control"})
    solicitanteEjecutivoEmail = forms.EmailField(
        max_length=100,
        label="Email",
        required=False)
    solicitanteEjecutivoEmail.widget.attrs.update({'class': "form-control"})
    solicitanteEjecutivoTelefono = forms.CharField(
        max_length=20,
        label="Teléfono",
        required=False)
    solicitanteEjecutivoTelefono.widget.attrs.update({'class': "form-control"})

    cliente = forms.CharField(label="Nombre cliente", max_length=100, required=False)
    cliente.widget.attrs.update({'class': "form-control"})
    clienteRut = forms.CharField(label="Rut cliente", max_length=100, required=False)
    clienteRut.widget.attrs.update({'class': "form-control"})
    clienteEmail = forms.EmailField(label="Email cliente", max_length=100, required=False)
    clienteEmail.widget.attrs.update({'class': "form-control"})
    clienteTelefono = forms.CharField(label="Teléfono cliente", max_length=100, required=False)
    clienteTelefono.widget.attrs.update({'class': "form-control"})

    propietario = forms.CharField(label="Nombre propietario", max_length=100, required=False)
    propietario.widget.attrs.update({'class': "form-control"})
    propietarioRut = forms.CharField(label="Rut propietario", max_length=100, required=False)
    propietarioRut.widget.attrs.update({'class': "form-control"})
    propietarioEmail = forms.EmailField(label="Email propietario", max_length=100, required=False)
    propietarioEmail.widget.attrs.update({'class': "form-control"})
    propietarioTelefono = forms.CharField(label="Teléfono propietario", max_length=100, required=False)
    propietarioTelefono.widget.attrs.update({'class': "form-control"})

    contacto = forms.CharField(label="Nombre contacto", max_length=100, required=False)
    contacto.widget.attrs.update({'class': "form-control",'data-validation':"required"})
    contactoRut = forms.CharField(label="Rut contacto", max_length=100, required=False)
    contactoRut.widget.attrs.update({'class': "form-control"})
    contactoEmail = forms.EmailField(label="Email contacto", max_length=100, required=False)
    contactoEmail.widget.attrs.update({'class': "form-control"})
    contactoTelefono = forms.CharField(label="Teléfono contacto", max_length=100, required=False)
    contactoTelefono.widget.attrs.update({'class': "form-control"})

    propertyType = forms.ChoiceField(
        label="Tipo propiedad",
        choices=RealEstate.propertyType_choices)
    propertyType.widget.attrs.update({'class':"form-control"})

    rol = forms.CharField(label="Rol", max_length=20, required=False)
    rol.widget.attrs.update({'class': "form-control"})

    addressRegion = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.only('name').all())
    addressRegion.widget.attrs.update({'class':"form-control"})

    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.only('name').all())
    addressCommune.widget.attrs.update({'class':"form-control"})

    addressStreet = forms.CharField(
        max_length=200,
        label="Calle")
    addressStreet.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber = forms.CharField(max_length=30,label="Número")
    addressNumber.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber2 = forms.CharField(max_length=30,label="Depto.",required=False)
    addressNumber2.widget.attrs.update({'class':"form-control"})

    appraisalTimeRequest = forms.DateTimeField(label="Fecha solicitud",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control datetimepicker-input",
                   'data-target':"#datetimepicker1"}))
    appraisalTimeRequest.input_formats = ['%d/%m/%Y']
    appraisalTimeDue = forms.DateTimeField(label="Fin de plazo",
        widget=forms.DateTimeInput(
            attrs={'class': "form-control datetimepicker-input",
                   'data-target':"#datetimepicker2"}))
    appraisalTimeDue.input_formats = ['%d/%m/%Y %H:%M']
    
    appraisalPrice = forms.FloatField(label="Precio",required=False)
    appraisalPrice.widget.attrs.update({'class': "form-control"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['addressCommune'].queryset = []

    def clean(self):
        self.cleaned_data['clienteRut'] = self.cleaned_data['clienteRut'].replace('.','')
        self.cleaned_data['clienteRut'] = self.cleaned_data['clienteRut'].replace('-','')
        self.cleaned_data['clienteRut'] = self.cleaned_data['clienteRut'].lower()
        if self.cleaned_data.get('addressStreet')=="":
            raise forms.ValidationError('No name!')
        if self.cleaned_data.get('addressStreet')=="":
            raise forms.ValidationError('No name!')
        if self.cleaned_data.get('propertyType') == RealEstate.TYPE_APARTMENT:
            if self.cleaned_data.get('addressNumberFlat').strip()=="":
                raise forms.ValidationError('No hay número de departamento (quizás puso sólo un espacio)')
        return self.cleaned_data

    def clean_appraisalTimeFrame(self):
        data = self.cleaned_data['appraisalTimeFrame']
        # Check date is not in past.
        if data.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None):
            raise forms.ValidationError(('Plazo se debe fijar en el futuro'), code='invalid')
        # Remember to always return the cleaned data.
        return data
