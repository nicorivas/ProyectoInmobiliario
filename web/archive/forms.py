from django import forms
from dbase.globals import *
from appraisal.models import Appraisal
from commune.models import Commune
from region.models import Region
from bootstrap_datepicker_plus import DateTimePickerInput

class FormSearch(forms.Form):
	
	attrs = {'class': "form-control form-control-sm"}

	state = forms.ChoiceField(label="Estado",choices=Appraisal.STATES_ARCHIVE)
	state.widget.attrs.update(attrs)

	code = forms.CharField(label="ID")
	code.widget.attrs.update(attrs)

	solicitante = forms.ChoiceField(label="Cliente",choices=Appraisal.petitioner_choices)
	solicitante.widget.attrs.update(attrs)

	solicitanteCodigo = forms.CharField(label="Código")
	solicitanteCodigo.widget.attrs.update(attrs)

	addressRegion = forms.ModelChoiceField(label="Región",queryset=Region.objects.only('name').all())
	addressRegion.widget.attrs.update(attrs)

	addressCommune = forms.ModelChoiceField(label="Comuna",queryset=Commune.objects.only('name').all())
	addressCommune.widget.attrs.update(attrs)

	addressStreet = forms.CharField(label="Calle")
	addressStreet.widget.attrs.update(attrs)

	addressNumber = forms.CharField(label="Número")
	addressNumber.widget.attrs.update(attrs)

	tasador = forms.CharField(label="Tasador")
	tasador.widget.attrs.update(attrs)

	visador = forms.CharField(label="Visador")
	visador.widget.attrs.update(attrs)

	timeCreatedFrom = forms.DateTimeField(label="Creada desde")
	timeCreatedFrom.widget = DateTimePickerInput(options={
                     "format": "YYYY-MM-DD HH:MM",
                     "showClose": True,
                     "showClear": True,
                     "showTodayButton": True
                 })
	timeCreatedFrom.widget.attrs.update(attrs)
	timeCreatedUntil = forms.DateTimeField(label="Creada hasta")
	timeCreatedUntil.widget = DateTimePickerInput(options={
                     "format": "YYYY-MM-DD HH:MM",
                     "showClose": True,
                     "showClear": True,
                     "showTodayButton": True
                 })
	timeCreatedUntil.widget.attrs.update(attrs)

	timeFinishedFrom = forms.DateTimeField(label="Terminada desde")
	timeFinishedFrom.widget = DateTimePickerInput(options={
                 "format": "YYYY-MM-DD HH:MM",
                 "showClose": True,
                 "showClear": True,
                 "showTodayButton": True
             })
	timeFinishedFrom.widget.attrs.update(attrs)
	timeFinishedUntil = forms.DateTimeField(label="Terminada hasta")
	timeFinishedUntil.widget = DateTimePickerInput(options={
                 "format": "YYYY-MM-DD HH:MM",
                 "showClose": True,
                 "showClear": True,
                 "showTodayButton": True
             })
	timeFinishedUntil.widget.attrs.update(attrs)
