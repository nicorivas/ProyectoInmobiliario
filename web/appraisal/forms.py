from django import forms
from realestate.models import RealEstate, Asset
from apartment.models import Apartment
from appraisal.models import Appraisal, Rol, Comment, Photo
from building.models import Building
from apartmentbuilding.models import ApartmentBuilding
from terrain.models import Terrain
from house.models import House
from region.models import Region
from commune.models import Commune
from condominium.models import Condominium
from multiupload.fields import MultiImageField
from dbase.globals import *

class FormAppraisal(forms.ModelForm):

    class Meta:
        model = Appraisal
        fields = [
            'solicitante',
            'solicitanteCodigo',
            'solicitanteSucursal',
            'solicitanteEjecutivo',
            'solicitanteEjecutivoEmail',
            'solicitanteEjecutivoTelefono',
            'cliente',
            'clienteRut',
            'clienteEmail',
            'clienteTelefono',
            'contacto',
            'contactoRut',
            'contactoEmail',
            'contactoTelefono',
            'propietario',
            'propietarioRut',
            'propietarioEmail',
            'propietarioTelefono',
            'propietarioReferenceSII',
            'visadorEmpresa',
            'visadorEmpresaMail',
            'valorUF',
            'tipoTasacion',
            'finalidad',
            'visita',
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
            'solicitanteEjecutivoEmail': forms.TextInput(attrs=attrs),
            'solicitanteEjecutivoTelefono': forms.TextInput(attrs=attrs),
            'contacto': forms.TextInput(attrs=attrs),
            'contactoRut': forms.TextInput(attrs=attrs_rut),
            'contactoEmail': forms.TextInput(attrs=attrs),
            'contactoTelefono': forms.TextInput(attrs=attrs),
            'cliente': forms.TextInput(attrs=attrs),
            'clienteRut': forms.TextInput(attrs=attrs_rut),
            'clienteEmail': forms.TextInput(attrs=attrs),
            'clienteTelefono': forms.TextInput(attrs=attrs),
            'propietario': forms.TextInput(attrs=attrs),
            'propietarioRut': forms.TextInput(attrs=attrs_rut),
            'propietarioEmail': forms.TextInput(attrs=attrs),
            'propietarioTelefono': forms.TextInput(attrs=attrs_rut),
            'propietarioReferenceSII': forms.CheckboxInput(attrs=attrs_check),
            'visadorEmpresa': forms.TextInput(attrs=attrs),
            'visadorEmpresaMail': forms.EmailInput(attrs=attrs),
            'valorUF': forms.TextInput(attrs={'class':"form-control text-right",'lang':"es-ES"}),
            'tipoTasacion':forms.Select(choices=Appraisal.tipoTasacion_choices, attrs=attrs),
            'finalidad':forms.Select(attrs=attrs,choices=Appraisal.petitioner_choices),
            'visita':forms.Select(attrs=attrs,choices=Appraisal.visit_choices),
            'descripcionSector':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'descripcionPlanoRegulador':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'descripcionExpropiacion':forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5})
        }

class FormBuilding(forms.ModelForm):

    class Meta:
        model = Building
        fields = [
            'anoConstruccion',
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
        class_se_sm = {'class':"custom-select custom-select-sm"}

        widgets = {
            'anoConstruccion': forms.TextInput(attrs=class_bs_sm),
            'vidaUtilRemanente': forms.NumberInput(attrs=class_bs_sm),
            'avaluoFiscal': forms.NumberInput(attrs={'class':"form-control form-control-sm",'lang':"es"}),
            'dfl2': forms.Select(attrs=class_se_sm),
            'selloVerde': forms.Select(attrs=class_se_sm),
            'copropiedadInmobiliaria': forms.Select(attrs=class_se_sm),
            'ocupante': forms.Select(attrs=class_se_sm),
            'tipoBien': forms.TextInput(attrs=class_bs_sm),
            'destinoSII': forms.Select(attrs=class_se_sm),
            'usoActual': forms.Select(attrs=class_se_sm),
            'usoFuturo': forms.Select(attrs=class_se_sm),
            'permisoEdificacionNo': forms.TextInput(attrs=class_bs_sm),
            'permisoEdificacionFecha': forms.TextInput(attrs=class_bs_sm),
            'recepcionFinalNo': forms.TextInput(attrs=class_bs_sm),
            'recepcionFinalFecha': forms.DateTimeInput(attrs=class_bs_sm),
            'expropiacion': forms.Select(attrs=class_se_sm),
            'viviendaSocial': forms.Select(attrs=class_se_sm),
            'desmontable': forms.Select(attrs=class_se_sm),
            'adobe': forms.Select(attrs=class_se_sm),
            'acogidaLey': forms.Select(attrs=class_se_sm),
            'mercadoObjetivo': forms.Select(attrs=class_se_sm)
        }
        
class FormRealEstate(forms.ModelForm):

    class Meta:
        model = RealEstate
        fields = [
            'addressStreet',
            'addressNumber',
            'addressCommune',
            'addressRegion'
        ]

        class_bs = {'class':"form-control"}

        widgets = {
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs),
            'addressCommune': forms.Select(attrs=class_bs),
            'addressRegion': forms.Select(attrs=class_bs)
        }
        
    def __init__(self, *args, **kwargs):
        super(FormRealEstate, self).__init__(*args, **kwargs)

class FormApartmentBuilding(forms.ModelForm):

    class Meta:
        model = ApartmentBuilding
        fields = [
            'floors',
            'generalDescription',
            'builtSquareMeters'
        ]
        class_bs = {'class':"form-control"}
        class_bs_sm = {'class':"form-control form-control-sm"}
        widgets = {
            'floors': forms.NumberInput(attrs=class_bs),
            'generalDescription': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs)
        }

class FormApartment(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = [
            'apartment_building',
            'addressNumber2',
            'floor',
            'bedrooms',
            'bathrooms',
            'usefulSquareMeters',
            'terraceSquareMeters',
            'orientation',
            'generalDescription',
            'programa',
            'estructuraTerminaciones'
        ]
        class_bs = {'class':"form-control"}
        class_bs_sm = {'class':"form-control form-control-sm"}
        widgets = {
            'apartment_building': forms.HiddenInput(),
            'addressNumber2': forms.HiddenInput(),
            'floor': forms.NumberInput(attrs=class_bs_sm),
            'bedrooms': forms.NumberInput(attrs=class_bs_sm),
            'bathrooms': forms.NumberInput(attrs=class_bs_sm),
            'usefulSquareMeters': forms.NumberInput(attrs=class_bs_sm),
            'terraceSquareMeters': forms.NumberInput(attrs=class_bs_sm),
            'orientation': forms.Select(attrs={'class':"custom-select custom-select-sm"}),
            'generalDescription': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'programa': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
            'estructuraTerminaciones': forms.Textarea(attrs={'class':"form-control form-control-sm",'rows':5}),
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

class FormTerrain(forms.ModelForm):

    class Meta:
        model = Terrain

        fields = [
            'addressNumber2',
            'frente',
            'fondo',
            'topography',
            'shape',
            'area'
        ]
        class_bs = {'class': "form-control form-control-sm"}
        widgets = {
            'addressNumber2': forms.HiddenInput(),
            'frente': forms.NumberInput(attrs=class_bs),
            'fondo': forms.NumberInput(attrs=class_bs),
            'topography': forms.Select(attrs={'class':"custom-select custom-select-sm"}),
            'shape': forms.Select(attrs={'class':"custom-select custom-select-sm"}),
            'area': forms.NumberInput(attrs=class_bs)
        }

class FormCreateTerrain(forms.ModelForm):
    class Meta:
        model = Terrain
        fields = [
            'addressNumber2',
            'name',
            'frente',
            'fondo',
            'topography',
            'shape',
            'area',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm terrains"}
        class_bs_right = {'class':"form-control form-control-sm terrains",'style':'text-align:right;'}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'name': forms.TextInput(attrs=class_bs),
            'frente': forms.NumberInput(attrs=class_bs),
            'fondo': forms.NumberInput(attrs=class_bs),
            'topography': forms.Select(attrs=class_bs),
            'shape': forms.Select(attrs=class_bs),
            'area': forms.NumberInput(attrs=class_bs_right),
            'marketPrice': forms.NumberInput(attrs=class_bs_right)
            }

class FormCreateHouse(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'addressNumber2',
            'bedrooms',
            'bathrooms',
            'builtSquareMeters',
            'terrainSquareMeters',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm terrains"}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'terrainSquareMeters': forms.NumberInput(attrs=class_bs),
            'marketPrice': forms.NumberInput(attrs=class_bs)
            }

class FormCreateApartmentBuilding(forms.ModelForm):
    class Meta:
        model = ApartmentBuilding
        fields = [
            'addressNumber2',
            'builtSquareMeters',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'marketPrice': forms.NumberInput(attrs=class_bs)
            }

class FormCreateApartment(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'addressNumber2',
            'floor',
            'bedrooms',
            'bathrooms',
            'usefulSquareMeters',
            'terraceSquareMeters',
            'marketPrice'
            ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'addressNumber2': forms.TextInput(attrs=class_bs),
            'floor': forms.NumberInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'usefulSquareMeters': forms.NumberInput(attrs=class_bs),
            'terraceSquareMeters': forms.NumberInput(attrs=class_bs),
            'marketPrice': forms.NumberInput(attrs=class_bs)
            }

class FormCreateRealEstate(forms.ModelForm):
    class Meta:
        model = RealEstate
        fields = [
            'addressStreet',
            'addressNumber',
            'addressCommune',
            'addressRegion',
            'sourceUrl',
            'sourceName',
            'sourceId'
            ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs),
            'addressCommune': forms.Select(attrs=class_bs),
            'addressRegion': forms.Select(attrs=class_bs),
            'sourceUrl': forms.TextInput(attrs=class_bs),
            'sourceName': forms.TextInput(attrs=class_bs),
            'sourceId': forms.TextInput(attrs=class_bs)
            }

class FormCreateProperty(forms.Form):

    class_bs = {'class':"form-control form-control-sm"}

    addressRegion = forms.ChoiceField(label="Región",choices=REGION_CHOICES_SHORT)
    addressRegion.widget.attrs.update(class_bs)

    addressCommune = forms.ChoiceField(label="Comuna",choices=COMMUNE_CHOICES)
    addressCommune.widget.attrs.update(class_bs)

    addressStreet = forms.CharField(max_length=200,label="Calle")
    addressStreet.widget.attrs.update(class_bs)

    addressNumber = forms.CharField(max_length=30,label="Número")
    addressNumber.widget.attrs.update(class_bs)

    addressNumber2 = forms.CharField(max_length=30,label="Número")
    addressNumber2.widget.attrs.update(class_bs)


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

class FormEditAddress(forms.Form):

    css_class = "form-control form-control-sm"

    addressRegion = forms.ChoiceField(label="Región",choices=REGION_CHOICES_SHORT)
    addressRegion.widget.attrs.update({'class':css_class})

    addressCommune = forms.ChoiceField(label="Comuna",choices=COMMUNE_CHOICES)
    addressCommune.widget.attrs.update({'class':css_class})

    addressStreet = forms.CharField(max_length=200,label="Calle")
    addressStreet.widget.attrs.update({'class':css_class,'data-validation':"required"})

    addressNumber = forms.CharField(max_length=30,label="Número")
    addressNumber.widget.attrs.update({'class':css_class,'data-validation':"required"})

    addressLoteo = forms.CharField(max_length=200,label="Loteo",required=False)
    addressLoteo.widget.attrs.update({'class':css_class})

    addressSitio = forms.CharField(max_length=200,label="Sitio",required=False)
    addressSitio.widget.attrs.update({'class':css_class})

    addressSquare = forms.CharField(max_length=200,label="Manzana",required=False)
    addressSquare.widget.attrs.update({'class':css_class})

    addressSector = forms.CharField(max_length=200,label="Loteo / Población / Sector / Conjunto Habitacional",required=False)
    addressSector.widget.attrs.update({'class':css_class})

    def get_groups_fields(self):
        for field_name in self.fields:
            if field_name.startswith("addressCondominiumType_"):
                yield [
                    self[field_name],
                    self["addressCondominiumName_"+field_name[-1:]],
                    self["addressCondominiumId_"+field_name[-1:]]]

    def __init__(self, *args, **kwargs):
        css_class = "form-control form-control-sm"
        real_estate = kwargs.pop('real_estate')
        super().__init__(*args, **kwargs)
        for i, condominium in enumerate(real_estate.addressCondominium.all()):
            field_name = "addressCondominiumType_{}".format(i)
            self.fields[field_name] = forms.ChoiceField(label="Grupo",choices=Condominium.ctype_choices,required=False)
            self.fields[field_name].widget.attrs.update({'class':css_class})
            try:
                self.initial[field_name] = condominium.ctype
            except IndexError:
                self.initial[field_name] = ""
            field_name = "addressCondominiumName_{}".format(i)
            self.fields[field_name] = forms.CharField(max_length=200,label="Nombre grupo",required=False)
            self.fields[field_name].widget.attrs.update({'class':css_class})
            try:
                self.initial[field_name] = condominium.name
            except IndexError:
                self.initial[field_name] = ""
            field_name = "addressCondominiumId_{}".format(i)
            self.fields[field_name] = forms.IntegerField(label="Id grupo",required=False)
            try:
                self.initial[field_name] = condominium.id
            except IndexError:
                self.initial[field_name] = ""
        
        # If there are no condominiums, we add some empty fields
        if real_estate.addressCondominium.count() == 0:
            self.fields["addressCondominiumType_0"] = forms.ChoiceField(label="Grupo",choices=Condominium.ctype_choices,required=False)
            self.fields["addressCondominiumType_0"].widget.attrs.update({'class':css_class})
            self.fields["addressCondominiumName_0"] = forms.CharField(max_length=200,label="Nombre grupo",required=False)
            self.fields["addressCondominiumName_0"].widget.attrs.update({'class':css_class})


class FormAddAddress(forms.Form):

    addressRegion = forms.ChoiceField(label="Región",choices=REGION_CHOICES)
    addressRegion.widget.attrs.update({'class':"form-control"})

    addressCommune = forms.ChoiceField(label="Comuna",choices=COMMUNE_CHOICES)
    addressCommune.widget.attrs.update({'class':"form-control"})

    addressStreet = forms.CharField(max_length=200,label="Calle")
    addressStreet.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber = forms.CharField(max_length=30,label="Número")
    addressNumber.widget.attrs.update({'class':"form-control",'data-validation':"required"})

class FormAddProperty(forms.Form):

    addressRegion = forms.ChoiceField(label="Región",choices=REGION_CHOICES)
    addressRegion.widget.attrs.update({'class':"form-control"})

    addressCommune = forms.ChoiceField(label="Comuna",choices=COMMUNE_CHOICES)
    addressCommune.widget.attrs.update({'class':"form-control"})

    addressStreet = forms.CharField(max_length=200,label="Calle")
    addressStreet.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    addressNumber = forms.CharField(max_length=30,label="Número")
    addressNumber.widget.attrs.update({'class':"form-control",'data-validation':"required"})

    propertyType = forms.ChoiceField(label="Tipo propiedad",choices=Building.propertyType_choices,required=True)
    propertyType.widget.attrs.update({'class':"form-control"})

    addressNumber2 = forms.CharField(max_length=30,label="Depto.",required=False)
    addressNumber2.widget.attrs.update({'class':"form-control"})

class FormEditProperty(forms.Form):

    addressNumber2 = forms.CharField(max_length=30,label="Depto.",required=False)
    addressNumber2.widget.attrs.update({'class':"form-control"})
    appraised = forms.BooleanField(required=False)
    appraised.widget.attrs.update({'class':'form-check-input'})

class FormAddApartment(forms.Form):

    addressNumber2 = forms.CharField(max_length=30,label="Departamento",required=True)
    addressNumber2.widget.attrs.update({'class':"form-control"})

class FormAddRol(forms.ModelForm):

    code = forms.CharField(max_length=20,label="Rol",required=True)
    code.widget.attrs.update({'class':"form-control"})

class FormPhotos(forms.Form):
    class_bs = {'class':"form-control form-control-sm"}
    photos = forms.FileField(
        label="Archivo",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class':"custom-file-input",'multiple': False}))
    category = forms.ChoiceField(
        label='Categoría',
        required=True,
        choices=Photo.PHOTO_CATEGORIES,
        widget=forms.Select(attrs={'class':"form-control"}))
    description = forms.CharField(
        label='Descripción',
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'size':20,'class':"form-control"}))

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
    text = forms.CharField(label='Comentario',max_length=500,widget=forms.Textarea,required=False)
    text.widget.attrs.update({'class':"form-control form-control-sm",'rows':3})
    event = forms.ChoiceField(choices=Comment.event_choices,label='Evento',required=True)
    event.widget.attrs.update({'class':"form-control form-control-sm"})
    datetime = forms.DateTimeField(label="Fecha y hora",required=False,
        widget=forms.DateTimeInput(
            attrs={'class': "form-control form-control-sm datetimepicker-input",
                   'data-target':"#datetimepicker1"}))
    datetime.input_formats = ['%d/%m/%Y %H:%M']

class FormExpenses(forms.Form):
    description = forms.CharField(label='Descripción', max_length=500, widget=forms.Textarea, required=False)
    description.widget.attrs.update({'class': "form-control form-control-sm", 'rows': 1})
    totalPrice = forms.IntegerField(label='Precio', widget=forms.NumberInput, required=False)
    totalPrice.widget.attrs.update({'class': "form-control form-control-sm", 'rows': 1})