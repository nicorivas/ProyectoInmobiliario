from django import forms
from django.contrib.auth.models import User
from appraisal.models import AppraisalEvaluation

class EvaluationForm(forms.ModelForm):

    class Meta:
        model = AppraisalEvaluation
        fields = [
            'onTime',
            'completeness',
            'generalQuality',
        ]

        class_bs = {'class':"form-control"}
        widgets = {
            'onTime': forms.NumberInput(attrs=class_bs),
            'completeness': forms.NumberInput(attrs=class_bs),
            'generalQuality': forms.NumberInput(attrs=class_bs),

        }
    commentText = forms.CharField(label='Comentarios', max_length=500, widget=forms.Textarea, required=False)
    commentText.widget.attrs.update({'class': "form-control", 'rows': 2})
    commentFeedback = forms.CharField(label='Feedback', max_length=500, widget=forms.Textarea, required=False)
    commentFeedback.widget.attrs.update({'class': "form-control", 'rows': 2})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

