from django import forms
from django.contrib.auth.models import User

class EvaluationForm(forms.Form):
    tasadores = forms.ModelChoiceField(
        label='Tasadores',
        queryset=User.objects.filter(groups__name__in=['tasador']),
        required=False
    )
    tasadores.widget.attrs.update({'class':"form-control"})

    onTime = forms.IntegerField(label="Puntualidad")
    completeness = forms.IntegerField(label="Completitud")
    generalQuality = forms.IntegerField(label='Calidad General')
    commentText = forms.CharField(label='Comentarios', max_length=500, widget=forms.Textarea, required=False)
    commentText.widget.attrs.update({'class': "form-control", 'rows': 2})
    commentFeedback = forms.CharField(label='Feedback', max_length=500, widget=forms.Textarea, required=False)
    commentFeedback.widget.attrs.update({'class': "form-control", 'rows': 2})