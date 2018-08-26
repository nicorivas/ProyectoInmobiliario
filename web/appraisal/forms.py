from django import forms
from data.chile import comunas_regiones

class AppraisalApartmentForm(forms.Form):

    ORIENTATIONS = (
        ('N', 'Norte'),
        ('NE', 'Norponiente'),
        ('E', 'Poniente'),
        ('SE', 'Surponiente'),
        ('S', 'Sur'),
        ('WS', 'Suroriente'),
        ('W', 'Oriente'),
        ('NW', 'Nororiente')
    )

    general_floor = forms.IntegerField(label="Piso",required=False,min_value=0)
    general_bedrooms = forms.IntegerField(label="Habitaciones",required=False,min_value=0)
    general_bathrooms = forms.IntegerField(label="Baños",required=False,min_value=0)
    general_totalSquareMeters = forms.FloatField(label="Superficie",required=False,min_value=0)
    general_usefulSquareMeters = forms.FloatField(label="Superficie útil",required=False,min_value=0)
    general_orientation = forms.ChoiceField(label="Orientación",choices=ORIENTATIONS,required=False)
    general_generalDescription = forms.CharField(label="Descripción general",
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}),required=False)

    app_solicitante = forms.CharField(label="Solicitante",required=False)
    app_solicitanteSucursal = forms.CharField(label="Solicitante sucursal",required=False)
    app_solicitanteEjecutivo = forms.CharField(label="Solicitante ejecutivo",required=False)
    app_cliente = forms.CharField(label="Cliente",required=False)
    app_clienteRut = forms.IntegerField(label="Cliente Rut",required=False)
    app_propietario = forms.CharField(label="Propietario",required=False)
    app_propietarioRut = forms.IntegerField(label="Propietario Rut",required=False)
    app_rolAvaluo = forms.IntegerField(label="Rol de avaluo",required=False)
    app_tasadorNombre = forms.CharField(label="Tasador",required=False)
    app_tasadorRut = forms.IntegerField(label="Tasador Rut",required=False)
    app_visadorEmpresa = forms.CharField(label="Visador empresa",required=False)
    app_visadorEmpresaMail = forms.CharField(label="Visador empresa mail",required=False)
