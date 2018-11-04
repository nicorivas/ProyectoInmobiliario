from .models import UserProfile
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from region.models import Region
from commune.models import Commune
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class AuthenticationFormB(AuthenticationForm):
    username = forms.CharField(max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    addressRegion = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.only('name').all(),
        required=False)
    addressRegion.widget.attrs.update({'class':"form-control"})

    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.only('name').all(),
        required=False)
    addressCommune.widget.attrs.update({'class':"form-control"})
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'addressStreet',
            'addressNumber'
        ]
        class_bs = {'class':"form-control"}
        widgets = {
            'first_name': forms.TextInput(attrs=class_bs),
            'last_name': forms.TextInput(attrs=class_bs),
            'email': forms.EmailInput(attrs=class_bs),
            'addressStreet': forms.TextInput(attrs=class_bs),
            'addressNumber': forms.TextInput(attrs=class_bs)
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EvaluationForm(forms.Form):
    tasadores = forms.ModelChoiceField(
        label='Tasadores',
        queryset=User.objects.filter(groups__name__in=['tasador']),
        required=False
    )
    tasadores.widget.attrs.update({'class':"form-control"})