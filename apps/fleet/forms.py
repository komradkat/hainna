from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'make', 'model', 'year', 'vin', 'status', 'mileage', 'capacity']
