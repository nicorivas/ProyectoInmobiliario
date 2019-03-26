import datetime
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

class AccountingForm(forms.Form):
    accountingTimeRequest = forms.DateTimeField(label="Fecha inicial")
    accountingTimeRequest.widget = DateTimePickerInput(options={
        "format": "DD/MM/YYYY HH:MM",
        "showClose": True,
        "showClear": True,
        "showTodayButton": True
    })

    accountingTimeDue = forms.DateTimeField(label="Fecha Término")
    accountingTimeDue.widget = DateTimePickerInput(options={
        "format": "DD/MM/YYYY HH:MM",
        "showClose": True,
        "showClear": True,
        "showTodayButton": True
    })
    tasador = forms.IntegerField(label="Tasador")