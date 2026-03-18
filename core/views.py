from django.shortcuts import render
from django.views.generic import TemplateView
import datetime

class HtmxTemplateMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'partial_base.html' if self.request.headers.get('HX-Request') else 'base.html'
        return context

class DashboardView(HtmxTemplateMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock fleet analytics data
        context['stats'] = {
            'active_units': 12,
            'idle_units': 4,
            'total_units': 16,
            'efficiency': '92%',
            'on_time_rate': '98.5%'
        }
        # Mock vehicles in transit
        context['vehicles'] = [
            {'id': 'Unit #05', 'driver': 'Marco Dela Cruz', 'status': 'Moving', 'eta': '12m', 'destination': 'North Port'},
            {'id': 'Unit #08', 'driver': 'Juan Luna', 'status': 'Moving', 'eta': '8m', 'destination': 'Central Station'},
            {'id': 'Unit #12', 'driver': 'Elena Santos', 'status': 'Delayed', 'eta': '25m', 'destination': 'South Terminal'},
            {'id': 'Unit #03', 'driver': 'Rico Reyes', 'status': 'Moving', 'eta': '5m', 'destination': 'Airport Road'},
        ]
        return context

class LiveTrackingView(HtmxTemplateMixin, TemplateView):
    template_name = 'tracking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock markers for vehicles with status and metadata
        context['units'] = [
            {'id': 'Unit #05', 'name': 'Marco Dela Cruz', 'pos': [11.24, 125.00], 'status': 'Moving', 'speed': '42 km/h', 'battery': '85%'},
            {'id': 'Unit #08', 'name': 'Juan Luna', 'pos': [11.30, 124.90], 'status': 'Idle', 'speed': '0 km/h', 'battery': '50%'},
            {'id': 'Unit #12', 'name': 'Elena Santos', 'pos': [11.15, 124.95], 'status': 'Stopped', 'speed': '0 km/h', 'battery': '12%'},
            {'id': 'Unit #03', 'name': 'Rico Reyes', 'pos': [11.25, 125.05], 'status': 'Offline', 'speed': 'N/A', 'battery': '0%'},
        ]
        return context

class FleetVehiclesView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet_vehicles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Enriched mock data for fleet management
        context['vehicles'] = [
            {'id': 'Unit #01', 'type': 'Semi-Trailer', 'make_model': 'Isuzu Giga', 'plate': 'ABC-1234', 'status': 'Active', 'location': 'Manila Hub', 'last_service': '2024-02-15', 'driver': 'Marco Dela Cruz'},
            {'id': 'Unit #02', 'type': 'Box Truck', 'make_model': 'Hino 500', 'plate': 'XYZ-5678', 'status': 'Maintenance', 'location': 'Quezon Service', 'last_service': '2024-03-10', 'driver': 'Juan Luna'},
            {'id': 'Unit #03', 'type': 'Semi-Trailer', 'make_model': 'Fuso Super Great', 'plate': 'LMN-9012', 'status': 'Active', 'location': 'Airport Road', 'last_service': '2024-01-20', 'driver': 'Elena Santos'},
            {'id': 'Unit #04', 'type': 'Flatbed', 'make_model': 'Ud Quon', 'plate': 'QRS-3456', 'status': 'Idle', 'location': 'South Depot', 'last_service': '2024-03-01', 'driver': 'Rico Reyes'},
            {'id': 'Unit #05', 'type': 'Semi-Trailer', 'make_model': 'Scania R500', 'plate': 'JKL-7890', 'status': 'Active', 'location': 'North Port', 'last_service': '2024-02-28', 'driver': 'Anton Ramos'},
            {'id': 'Unit #06', 'type': 'Box Truck', 'make_model': 'Isuzu Elf', 'plate': 'DEF-1122', 'status': 'Active', 'location': 'Cebu Terminal', 'last_service': '2024-02-10', 'driver': 'Santi Go'},
            {'id': 'Unit #07', 'type': 'Semi-Trailer', 'make_model': 'Man TGX', 'plate': 'GHI-3344', 'status': 'Maintenance', 'location': 'Davao Hub', 'last_service': '2024-03-15', 'driver': 'Lito Lapid'},
            {'id': 'Unit #08', 'type': 'Box Truck', 'make_model': 'Fuso Canter', 'plate': 'JKL-5566', 'status': 'Idle', 'location': 'Central Station', 'last_service': '2024-01-15', 'driver': 'Bong Revilla'},
        ]
        return context

def system_status(request):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return render(request, 'partials/status_badge.html', {'time': now})
