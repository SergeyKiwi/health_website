from django import forms
from .models import TemperatureMeasurement


class TemperatureMeasurementForm(forms.ModelForm):
    class Meta:
        model = TemperatureMeasurement
        fields = ['temperature', 'datetime_measurement']
        widgets = {
            'temperature': forms.NumberInput(attrs={
                'step': "0.1",
                'max': "50",
                'min': "16"
            }),
            'datetime_measurement': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            })
        }
