from django import forms

class ExportForm(forms.Form):

    archivo = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class':"custom-file-input",'multiple': False}))

    DESTINO_SANTANDER_WEB = 1
    destinos = [
        (DESTINO_SANTANDER_WEB,'Santander Web')
    ]

    destino = forms.ChoiceField(
        label="Destino",
        choices=destinos)
    destino.widget.attrs.update({'class': "form-control"})