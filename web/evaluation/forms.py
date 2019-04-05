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
            'correctSurface',
            'completeNormative',
            'homologatedReferences',
            'commentText',
            'commentFeedback'
        ]

        class_bs = {'class': 'form-check-input position-static', 'style': 'margin-left:0rem;'}
        widgets = {
            'onTime': forms.CheckboxInput(attrs=class_bs),
            'completeness': forms.CheckboxInput(attrs=class_bs),
            'generalQuality': forms.CheckboxInput(attrs=class_bs),
            'correctSurface': forms.CheckboxInput(attrs=class_bs),
            'completeNormative': forms.CheckboxInput(attrs=class_bs),
            'homologatedReferences': forms.CheckboxInput(attrs=class_bs),
            'commentText': forms.Textarea(attrs={'class':"form-control",'rows':2,'cols':80}),
            'commentFeedback': forms.Textarea(attrs={'class':"form-control",'rows':2,'cols':80})
        }