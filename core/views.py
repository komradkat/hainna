from django.shortcuts import render
from django.views.generic import TemplateView
import datetime

class HtmxTemplateMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'partial_base.html' if self.request.headers.get('HX-Request') else 'base.html'
        return context

class DashboardView(HtmxTemplateMixin, TemplateView):
    template_name = 'dashboard/index.html'

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
    template_name = 'tracking/index.html'

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
    template_name = 'fleet/index.html'

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

class DriversView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = [
            {'id': 'DRV-001', 'name': 'Marco Dela Cruz', 'license': 'D01-12-345678', 'contact': '+63 912 345 6789', 'status': 'Active', 'vehicle': 'Isuzu Giga (ABC-1234)', 'trips': 142, 'rating': 4.9, 'joined': 'Jan 2022'},
            {'id': 'DRV-002', 'name': 'Juan Luna', 'license': 'D01-98-765432', 'contact': '+63 917 654 3210', 'status': 'Active', 'vehicle': 'Hino 500 (XYZ-5678)', 'trips': 98, 'rating': 4.7, 'joined': 'Mar 2023'},
            {'id': 'DRV-003', 'name': 'Elena Santos', 'license': 'D02-11-223344', 'contact': '+63 920 111 2233', 'status': 'On Leave', 'vehicle': 'Fuso Super Great (LMN-9012)', 'trips': 210, 'rating': 4.8, 'joined': 'Aug 2021'},
            {'id': 'DRV-004', 'name': 'Rico Reyes', 'license': 'D03-55-667788', 'contact': '+63 905 556 6778', 'status': 'Off Duty', 'vehicle': 'Ud Quon (QRS-3456)', 'trips': 75, 'rating': 4.5, 'joined': 'Jun 2023'},
            {'id': 'DRV-005', 'name': 'Anton Ramos', 'license': 'D01-44-556677', 'contact': '+63 918 445 5667', 'status': 'Active', 'vehicle': 'Scania R500 (JKL-7890)', 'trips': 187, 'rating': 4.6, 'joined': 'Nov 2021'},
            {'id': 'DRV-006', 'name': 'Santi Go', 'license': 'D02-33-445566', 'contact': '+63 933 334 4556', 'status': 'Active', 'vehicle': 'Isuzu Elf (DEF-1122)', 'trips': 63, 'rating': 4.3, 'joined': 'Sep 2024'},
            {'id': 'DRV-007', 'name': 'Lito Lapid', 'license': 'D01-77-889900', 'contact': '+63 922 778 8990', 'status': 'Off Duty', 'vehicle': 'Man TGX (GHI-3344)', 'trips': 301, 'rating': 4.9, 'joined': 'Feb 2020'},
            {'id': 'DRV-008', 'name': 'Bong Revilla', 'license': 'D03-22-334455', 'contact': '+63 908 223 3445', 'status': 'Active', 'vehicle': 'Fuso Canter (JKL-5566)', 'trips': 129, 'rating': 4.4, 'joined': 'Apr 2022'},
        ]
        context['stats'] = {'active': 5, 'off_duty': 2, 'on_leave': 1, 'total': 8}
        return context

class RoutesView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = [
            {'id': 'RTE-001', 'name': 'Manila – North Port Express', 'origin': 'Manila Hub', 'destination': 'North Port', 'distance': '42 km', 'est_time': '1h 20m', 'status': 'Active', 'active_units': 3},
            {'id': 'RTE-002', 'name': 'Central – Airport Connector', 'origin': 'Central Station', 'destination': 'Airport Road', 'distance': '18 km', 'est_time': '45m', 'status': 'Active', 'active_units': 2},
            {'id': 'RTE-003', 'name': 'South Terminal Loop', 'origin': 'South Terminal', 'destination': 'Quezon Service', 'distance': '31 km', 'est_time': '1h 05m', 'status': 'Active', 'active_units': 1},
            {'id': 'RTE-004', 'name': 'Cebu – Davao Trunk Line', 'origin': 'Cebu Terminal', 'destination': 'Davao Hub', 'distance': '985 km', 'est_time': '18h 00m', 'status': 'Inactive', 'active_units': 0},
            {'id': 'RTE-005', 'name': 'Depot Supply Run', 'origin': 'South Depot', 'destination': 'Manila Hub', 'distance': '27 km', 'est_time': '50m', 'status': 'Active', 'active_units': 1},
        ]
        context['route_stats'] = {
            'total': 5, 'active': 4,
            'total_km': '1,103 km', 'units_on_route': 7, 'avg_time': '4h 12m',
        }
        context['zones'] = [
            {'id': 'ZNE-001', 'name': 'Manila Hub Zone', 'type': 'Delivery Hub', 'color': '#3b82f6', 'units_inside': 4, 'radius': '3.0 km', 'alerts': 0, 'active': True},
            {'id': 'ZNE-002', 'name': 'Airport Restricted Area', 'type': 'Restricted', 'color': '#f43f5e', 'units_inside': 0, 'radius': '1.5 km', 'alerts': 2, 'active': True},
            {'id': 'ZNE-003', 'name': 'North Port Waypoint', 'type': 'Waypoint', 'color': '#10b981', 'units_inside': 2, 'radius': '0.8 km', 'alerts': 0, 'active': True},
            {'id': 'ZNE-004', 'name': 'South Depot Zone', 'type': 'Delivery Hub', 'color': '#f59e0b', 'units_inside': 1, 'radius': '2.0 km', 'alerts': 1, 'active': True},
            {'id': 'ZNE-005', 'name': 'Cebu Terminal Zone', 'type': 'Waypoint', 'color': '#8b5cf6', 'units_inside': 0, 'radius': '1.2 km', 'alerts': 0, 'active': False},
        ]
        context['zone_stats'] = {'total': 5, 'active': 4, 'units_inside': 7, 'alerts': 3}
        return context

def system_status(request):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return render(request, 'partials/status_badge.html', {'time': now})
