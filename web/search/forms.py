from django import forms
from data.chile import comunas_regiones

class LocationSearchForm(forms.Form):

    address = forms.CharField(max_length=200,label="")
    address.widget.attrs.update({'placeholder':'Buscar'})

class AppraisalCreateForm(forms.Form):

    addressRegion_create = forms.ChoiceField(label="Región",choices=[(a,a) for a in comunas_regiones.regiones])
    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune_create = forms.ChoiceField(label="Comuna",choices=[(a,a) for a in comunas_regiones.comunas])
    addressStreet_create = forms.CharField(max_length=200,label="Calle")
    #addressStreet_create.widget.attrs.update({'placeholder':''})
    addressNumber_create = forms.CharField(max_length=6,label="Número")
    addressNumberFlat_create = forms.CharField(max_length=6,label="Depto.")
    #comunas_regiones['regiones'][''] =

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['addressCommune_create'].queryset = []
