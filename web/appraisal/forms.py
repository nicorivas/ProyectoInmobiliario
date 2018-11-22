from django import forms
from realestate.models import RealEstate, Construction, Terrain, Asset
from apartment.models import Apartment
from appraisal.models import Appraisal, Rol
from building.models import Building
from house.models import House
from region.models import Region
from commune.models import Commune
from multiupload.fields import MultiImageField

class FormRealEstate(forms.ModelForm):

    class Meta:
        model = RealEstate
        fields = [
            'addressStreet',
            'addressNumber',
            'addressCommune',
            'addressRegion',
            'anoConstruccion',
            'programa',
            'estructuraTerminaciones',
            'vidaUtilRemanente',
            'avaluoFiscal',
            'dfl2',
            'selloVerde',
            'copropiedadInmobiliaria',
            'ocupante',
            'tipoBien',
            'destinoSII',
            'usoActual',
            'usoFuturo',
            'permisoEdificacionNo',
            'permisoEdificacionFecha',
            'recepcionFinalNo',
            'recepcionFinalFecha',
            'expropiacion',
            'viviendaSocial',
            'desmontable',
            'adobe',
            'acogidaLey',
            'mercadoObjetivo'
        ]

        class_bs = {'class':"form-control"}
        class_bs_sm = {'class':"form-control form-control-sm"}
        class_dp_y_bs = {'class':"form-control"}
        class_dp_m_bs = {'class':"form-control"}
        class_se_bs = {'class':"custom-select"}

        widgets = {
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs),
            'addressCommune': forms.Select(attrs=class_bs),
            'addressRegion': forms.Select(attrs=class_bs),
            'anoConstruccion': forms.TextInput(attrs=class_dp_y_bs),
            'programa': forms.Textarea(attrs={'class':"form-control",'rows':5}),
            'estructuraTerminaciones': forms.Textarea(attrs={'class':"form-control",'rows':10}),
            'vidaUtilRemanente': forms.NumberInput(attrs=class_bs),
            'avaluoFiscal': forms.NumberInput(attrs={'class':"form-control",'lang':"es"}),
            'dfl2': forms.Select(attrs=class_se_bs),
            'selloVerde': forms.Select(attrs=class_se_bs),
            'copropiedadInmobiliaria': forms.Select(attrs=class_se_bs),
            'ocupante': forms.Select(attrs=class_se_bs),
            'tipoBien': forms.TextInput(attrs=class_bs),
            'destinoSII': forms.Select(attrs=class_se_bs),
            'usoActual': forms.Select(attrs=class_se_bs),
            'usoFuturo': forms.Select(attrs=class_se_bs),
            'permisoEdificacionNo': forms.TextInput(attrs=class_bs),
            'permisoEdificacionFecha': forms.TextInput(attrs={'class':"form-control"}),
            'recepcionFinalNo': forms.TextInput(attrs=class_bs),
            'recepcionFinalFecha': forms.DateTimeInput(attrs=class_dp_m_bs),
            'expropiacion': forms.Select(attrs=class_se_bs),
            'viviendaSocial': forms.Select(attrs=class_se_bs),
            'desmontable': forms.Select(attrs=class_se_bs),
            'adobe': forms.Select(attrs=class_se_bs),
            'acogidaLey': forms.Select(attrs=class_se_bs),
            'mercadoObjetivo': forms.Select(attrs={'class':"custom-select"})
        }
        
    def __init__(self, *args, **kwargs):
        super(FormRealEstate, self).__init__(*args, **kwargs)
        #self.fields['addressCommune'].queryset = Commune.objects.only('name').all()
        #self.fields['addressRegion'].queryset = Region.objects.only('name').all()

class FormBuilding(forms.ModelForm):

    class Meta:
        model = Building
        fields = []

        class_bs = {'class':"form-control form-control-sm"}
        class_dp_y_bs = {'class':"form-control form-control-sm datepicker_year"}
        class_dp_m_bs = {'class':"form-control form-control-sm datepicker_month"}
        class_se_bs = {'class':"custom-select custom-select-sm"}

        widgets = {}

class FormApartment(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = [
            'addressNumber2',
            'floor',
            'bedrooms',
            'bathrooms',
            'usefulSquareMeters',
            'terraceSquareMeters',
            'orientation',
            'generalDescription'
        ]
        class_bs = {'class':"form-control"}
        class_bs_sm = {'class':"form-control form-control-sm"}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'floor': forms.NumberInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'usefulSquareMeters': forms.NumberInput(attrs=class_bs),
            'terraceSquareMeters': forms.NumberInput(attrs=class_bs),
            'orientation': forms.Select(attrs={'class':"custom-select"}),
            'generalDescription': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':15})
        }

class FormHouse(forms.ModelForm):

    class Meta:
        model = House

        fields = [
            'addressNumber2',
            'bedrooms',
            'bathrooms',
            'builtSquareMeters',
            'terrainSquareMeters',
            'generalDescription'
        ]
        class_bs = {'class': "form-control form-control-sm"}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'terrainSquareMeters': forms.NumberInput(attrs=class_bs),
            'generalDescription': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':15})
        }

class FormAppraisal(forms.ModelForm):

    class Meta:
        model = Appraisal
        fields = [
            'solicitante',
            'solicitanteCodigo',
            'solicitanteSucursal',
            'solicitanteEjecutivo',
            'cliente',
            'clienteRut',
            'propietario',
            'propietarioRut',
            'propietarioReferenceSII',
            'visadorEmpresa',
            'visadorEmpresaMail',
            'valorUF',
            'tipoTasacion',
            'objetivo',
            'descripcionSector',
            'descripcionPlanoRegulador',
            'descripcionExpropiacion'
        ]
        attrs = {'class':"form-control"}
        attrs_sm = {'class':"form-control form-control-sm"}
        attrs_check = {'class':"form-check-input"}
        attrs_req = {'class':"form-control form-control-sm",'data-validation':"required"}
        attrs_rut = {'class':"form-control",'data-validation':"rut"}
        widgets = {
            'solicitante': forms.Select(choices=Appraisal.petitioner_choices, attrs=attrs),
            'solicitanteCodigo': forms.TextInput(attrs=attrs),
            'solicitanteSucursal': forms.TextInput(attrs=attrs),
            'solicitanteEjecutivo': forms.TextInput(attrs=attrs),
            'cliente': forms.TextInput(attrs=attrs),
            'clienteRut': forms.TextInput(attrs=attrs_rut),
            'propietario': forms.TextInput(attrs=attrs),
            'propietarioRut': forms.TextInput(attrs=attrs_rut),
            'propietarioReferenceSII': forms.CheckboxInput(attrs=attrs_check),
            'visadorEmpresa': forms.TextInput(attrs=attrs),
            'visadorEmpresaMail': forms.EmailInput(attrs=attrs),
            'valorUF': forms.TextInput(attrs={'class':"form-control text-right",'lang':"es-ES"}),
            'tipoTasacion':forms.Select(choices=Appraisal.tipoTasacion_choices, attrs=attrs),
            'objetivo':forms.Select(attrs=attrs,choices=Appraisal.petitioner_choices),
            'descripcionSector':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'descripcionPlanoRegulador':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'descripcionExpropiacion':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5})
        }

class FormCreateApartment(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'addressCommune',
            'addressStreet',
            'addressNumber',
            'addressNumber2',
            'floor',
            'sourceUrl',
            'sourceName',
            'sourceId',
            'bedrooms',
            'bathrooms',
            'usefulSquareMeters',
            'terraceSquareMeters',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'addressCommune': forms.Select(attrs=class_bs),
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs),
            'addressNumber2': forms.NumberInput(attrs=class_bs),
            'floor': forms.NumberInput(attrs=class_bs),
            'sourceUrl': forms.URLInput(attrs=class_bs),
            'sourceName': forms.TextInput(attrs={'class':"form-control form-control-sm sourceName"}),
            'sourceId': forms.TextInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'usefulSquareMeters': forms.NumberInput(attrs=class_bs),
            'terraceSquareMeters': forms.NumberInput(attrs=class_bs),
            'marketPrice': forms.NumberInput(attrs=class_bs)
            }

class FormCreateHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'addressCommune',
            'addressStreet',
            'addressNumber',
            'addressNumber2',
            'sourceUrl',
            'sourceName',
            'sourceId',
            'bedrooms',
            'bathrooms',
            'builtSquareMeters',
            'terrainSquareMeters',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'addressCommune': forms.Select(attrs=class_bs),
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs),
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'sourceUrl': forms.URLInput(attrs=class_bs),
            'sourceName': forms.TextInput(attrs={'class':"form-control form-control-sm sourceName"}),
            'sourceId': forms.TextInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'terrainSquareMeters': forms.NumberInput(attrs=class_bs),
            'marketPrice': forms.NumberInput(attrs=class_bs)
            }

class FormCreateTerrain(forms.ModelForm):
    class Meta:
        model = Terrain
        fields = [
            'name',
            'frente',
            'fondo',
            'topography',
            'shape',
            'rol',
            'area',
            'UFPerArea'
            ]
        class_bs = {'class':"form-control form-control-sm terrains"}
        class_bs_right = {'class':"form-control form-control-sm terrains",'style':'text-align:right;'}
        widgets = {
            'name': forms.TextInput(attrs=class_bs),
            'frente': forms.NumberInput(attrs=class_bs),
            'fondo': forms.NumberInput(attrs=class_bs),
            'topography': forms.Select(attrs=class_bs),
            'shape': forms.Select(attrs=class_bs),
            'rol': forms.TextInput(attrs=class_bs),
            'area': forms.NumberInput(attrs=class_bs_right),
            'UFPerArea': forms.NumberInput(attrs=class_bs_right)
            }

class FormCreateConstruction(forms.ModelForm):
    class Meta:
        model = Construction
        fields = [
            'name',
            'material',
            'year',
            'prenda',
            'recepcion',
            'state',
            'quality',
            'rol',
            'area',
            'UFPerArea'
            ]
        class_bs = {'class':"form-control form-control-sm constructions"}
        class_bs_right = {'class':"form-control form-control-sm terrains",'style':'text-align:right;'}
        widgets = {
            'name': forms.TextInput(attrs=class_bs),
            'material': forms.Select(attrs=class_bs),
            'year': forms.DateInput(attrs=class_bs),
            'prenda': forms.NullBooleanSelect(attrs=class_bs),
            'recepcion': forms.Select(attrs=class_bs),
            'state': forms.Select(attrs=class_bs),
            'quality': forms.Select(attrs=class_bs),
            'rol': forms.TextInput(attrs=class_bs),
            'area': forms.NumberInput(attrs=class_bs_right),
            'UFPerArea': forms.NumberInput(attrs=class_bs_right)
            }

class FormCreateAsset(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'value'
            ]
        class_bs = {'class':"form-control form-control-sm constructions"}
        class_bs_right = {'class':"form-control form-control-sm terrains",'style':'text-align:right;'}
        widgets = {
            'name': forms.TextInput(attrs=class_bs),
            'value': forms.NumberInput(attrs=class_bs_right)
            }

class FormCreateRol(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'code',
            'state'
            ]
        class_bs = {'class':"form-control"}
        widgets = {
            'code': forms.TextInput(attrs=class_bs),
            'state': forms.Select(choices=Rol.rolTypeChoices,attrs=class_bs),
            } 

class FormPhotos(forms.Form):
    class_bs = {'class':"form-control form-control-sm"}
    photos = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class':"custom-file-input",'multiple': True}))
    description = forms.CharField(
        label='Descripción',
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={'size':20,'class':"form-control",'placeholder':'Descripción'}))

class FormDocuments(forms.Form):
    class_bs = {'class':"form-control form-control-sm"}
    documents = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class':"custom-file-input",'multiple': True}))
    description = forms.CharField(
        label='Descripción',
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={'size':20,'class':"form-control",'placeholder':'Descripción'}))

class FormComment(forms.Form):
    commentText = forms.CharField(label='Comment',max_length=500,widget=forms.Textarea,required=False)
    commentConflict = forms.BooleanField(label='Conflict',required=False)
    commentText.widget.attrs.update({'class':"form-control",'rows':3})
