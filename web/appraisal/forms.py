from django import forms
from apartment.models import Apartment
from appraisal.models import Appraisal
from building.models import Building
from house.models import House
from multiupload.fields import MultiImageField

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
            'permisoEdificacion',
            'permisoEdificacionDate',
            'recepcionFinal',
            'recepcionFinalDate',
            'expropiacion',
            'viviendaSocial',
            'adobe',
            'desmontable',
            'acogidaLey'
        ]

        class_bs = {'class':"form-control form-control-sm"}
        class_dp_y_bs = {'class':"form-control form-control-sm datepicker_year"}
        class_dp_m_bs = {'class':"form-control form-control-sm datepicker_month"}
        class_se_bs = {'class':"custom-select custom-select-sm"}

        widgets = {
            'anoConstruccion': forms.NumberInput(attrs=class_dp_y_bs),
            'vidaUtilRemanente': forms.NumberInput(attrs=class_bs),
            'avaluoFiscal': forms.NumberInput(attrs=class_bs),
            'dfl2': forms.NullBooleanSelect(attrs=class_se_bs),
            'selloVerde': forms.Select(attrs=class_se_bs),
            'copropiedadInmobiliaria': forms.NullBooleanSelect(attrs=class_se_bs),
            'ocupante': forms.Select(attrs=class_se_bs),
            'tipoBien': forms.TextInput(attrs=class_bs),
            'destinoSII': forms.Select(attrs=class_se_bs),
            'usoActual': forms.Select(attrs=class_se_bs),
            'usoFuturo': forms.Select(attrs=class_se_bs),
            'permisoEdificacion': forms.TextInput(attrs=class_bs),
            'permisoEdificacionDate': forms.DateTimeInput(attrs=class_dp_m_bs),
            'recepcionFinal': forms.TextInput(attrs=class_bs),
            'recepcionFinalDate': forms.DateTimeInput(attrs=class_dp_m_bs),
            'expropiacion': forms.NullBooleanSelect(attrs=class_se_bs),
            'viviendaSocial': forms.NullBooleanSelect(attrs=class_se_bs),
            'adobe': forms.NullBooleanSelect(attrs=class_se_bs),
            'desmontable': forms.NullBooleanSelect(attrs=class_se_bs),
            'acogidaLey': forms.Select(attrs=class_se_bs),
        }

class FormApartment(forms.ModelForm):

    class Meta:
        model = Apartment
        fields = [
            'floor',
            'bedrooms',
            'bathrooms',
            'builtSquareMeters',
            'usefulSquareMeters',
            'orientation',
            'generalDescription',
            'mercadoObjetivo'
        ]
        class_bs = {'class':"form-control form-control-sm"}
        widgets = {
            'floor': forms.NumberInput(attrs=class_bs),
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'usefulSquareMeters': forms.NumberInput(attrs=class_bs),
            'orientation': forms.Select(attrs={'class':"custom-select custom-select-sm"}),
            'generalDescription': forms.Textarea(attrs=class_bs),
            'mercadoObjetivo': forms.NullBooleanSelect(attrs={'class':"custom-select custom-select-sm"})
        }

class FormHouse(forms.ModelForm):

    class Meta:
        model = House

        fields = [
            'bedrooms',
            'bathrooms',
            'builtSquareMeters',
            'terrainSquareMeters',
            'generalDescription'
        ]
        class_bs = {'class': "form-control form-control-sm"}
        widgets = {
            'bedrooms': forms.NumberInput(attrs=class_bs),
            'bathrooms': forms.NumberInput(attrs=class_bs),
            'builtSquareMeters': forms.NumberInput(attrs=class_bs),
            'terrainSquareMeters': forms.NumberInput(attrs=class_bs),
            'generalDescription': forms.Textarea(attrs=class_bs),
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
            'rolAvaluo',
            'visadorEmpresa',
            'visadorEmpresaMail',
            'valorUF',
            'tipoTasacion',
            'objetivo'
        ]
        attrs = {'class':"form-control form-control-sm"}
        attrs_req = {'class':"form-control form-control-sm",'data-validation':"required"}
        attrs_rut = {'class':"form-control form-control-sm",'data-validation':"rut"}
        widgets = {

            'solicitante': forms.Select(choices=Appraisal.petitioner_choices, attrs=attrs),
            'solicitanteCodigo': forms.TextInput(attrs=attrs),
            'solicitanteSucursal': forms.TextInput(attrs=attrs),
            'solicitanteEjecutivo': forms.TextInput(attrs=attrs),
            'cliente': forms.TextInput(attrs=attrs),
            'clienteRut': forms.TextInput(attrs=attrs_rut),
            'propietario': forms.TextInput(attrs=attrs),
            'propietarioRut': forms.TextInput(attrs=attrs_rut),
            'rolAvaluo': forms.TextInput(attrs=attrs),
            'visadorEmpresa': forms.TextInput(attrs=attrs),
            'visadorEmpresaMail': forms.EmailInput(attrs=attrs),
            'valorUF': forms.TextInput(attrs=attrs),
            'tipoTasacion':forms.Select(choices=Appraisal.tipoTasacion_choices, attrs=attrs),
            'objetivo':forms.Select(attrs=attrs,choices=Appraisal.petitioner_choices),

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

class FormComment(forms.Form):
    commentText = forms.CharField(label='Comment',max_length=500,widget=forms.Textarea,required=False)
    commentConflict = forms.BooleanField(label='Conflict',required=False)
    commentText.widget.attrs.update({'class':"form-control",'rows':3})
