from django import forms
#from django_google_maps.widgets import GoogleMapsAddressAutocomplete

class LocationSearchForm(forms.Form):

    address = forms.CharField(max_length=100,label="")
    address.widget.attrs.update({'placeholder':'Dirección / Comuna / Lugar'})
