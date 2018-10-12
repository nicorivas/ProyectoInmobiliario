from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm, forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'addressStreet',
            'addressNumber',
            'addressRegion',
            'addressCommune',

        )

