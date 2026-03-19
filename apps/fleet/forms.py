from django import forms
from .models import Vehicle, Driver, MaintenanceLog, Route, Zone

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'make', 'model', 'year', 'vin', 'status', 'mileage', 'capacity', 'traccar_device_id']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'first_name', 'last_name', 'license_number', 'license_expiry', 'contact_number', 'status', 'rating']
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

class ServiceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['vehicle', 'driver', 'service_type', 'description', 'date', 'odometer_reading', 'cost', 'status', 'performed_by']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'origin', 'destination', 'distance_km', 'est_travel_time', 'status', 'geofence_radius_meters', 'color', 'waypoints', 'path_coordinates']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. Manila – North Port Express'}),
            'origin': forms.TextInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. Manila Hub', 'id': 'route_origin_input'}),
            'destination': forms.TextInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. North Port', 'id': 'route_destination_input'}),
            'distance_km': forms.NumberInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. 45', 'id': 'route_distance_input', 'step': '0.01'}),
            'est_travel_time': forms.TextInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. 1h 30m', 'id': 'route_time_input'}),
            'status': forms.Select(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white focus:outline-none focus:border-blue-500/50 transition-all appearance-none cursor-pointer'}),
            'geofence_radius_meters': forms.NumberInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'id': 'route_geofence_input', 'min': '10', 'max': '50000'}),
            'color': forms.HiddenInput(attrs={'id': 'route_color_input'}),
            'waypoints': forms.HiddenInput(attrs={'id': 'route_waypoints_input'}),
            'path_coordinates': forms.HiddenInput(attrs={'id': 'route_path_input'}),
        }

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'zone_type', 'coordinates']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all', 'placeholder': 'e.g. North Hub Zone'}),
            'zone_type': forms.Select(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white focus:outline-none focus:border-blue-500/50 transition-all appearance-none cursor-pointer'}),
            'coordinates': forms.Textarea(attrs={'class': 'w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm font-bold text-white placeholder:text-white/10 focus:outline-none focus:border-blue-500/50 transition-all custom-scrollbar', 'placeholder': 'e.g. [[14.5995, 120.9842], [14.6095, 120.9942], ...]', 'rows': 4}),
        }
