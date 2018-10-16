from .models import UserProfile
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from region.models import Region
from commune.models import Commune


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    addressRegion = forms.ModelChoiceField(
        label="Región",
        queryset=Region.objects.all())
    addressRegion.widget.attrs.update({'class':"form-control", 'class':"col-md-4"})

    # We need all possible communes to be there initially, so that when we validate the form,
    # it finds the choice.
    addressCommune = forms.ModelChoiceField(
        label="Comuna",
        queryset=Commune.objects.all())
    addressCommune.widget.attrs.update({'class':"form-control",  'class':"col-md-4"})
    class Meta:
        model = UserProfile
        fields = (
            'addressStreet',
            'addressNumber',

        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
