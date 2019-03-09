from .models import UserProfile
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from region.models import Region
from commune.models import Commune
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



UserModel = get_user_model()

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

class PasswordResetForm(forms.Form):

    email = forms.EmailField(label="Email", max_length=254)
    email.widget.attrs.update({'class':"form-control"})

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='user/password_reset_subject.txt',
             email_template_name='user/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )