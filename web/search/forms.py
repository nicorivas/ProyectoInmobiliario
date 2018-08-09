from django import forms

class LocationSearchForm(forms.Form):

    address = forms.CharField(max_length=200,label="")
    address.widget.attrs.update({'placeholder':'Buscar'})

class CreateProperty(forms.Form):

    address_create = forms.CharField(max_length=200,label="")
    address_create.widget.attrs.update({'placeholder':''})
