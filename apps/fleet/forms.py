from django import forms
from .models import Vehicle, Driver

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'make', 'model', 'year', 'vin', 'status', 'mileage', 'capacity']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'first_name', 'last_name', 'license_number', 'license_expiry', 'contact_number', 'status', 'rating']
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
        }
