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

class SchedulesView(HtmxTemplateMixin, TemplateView):
    template_name = 'schedules/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import datetime as dt
        today = dt.date.today()
        # Build week days starting Monday
        monday = today - dt.timedelta(days=today.weekday())
        days = []
        day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        # Sample trips per day index (0=Mon … 6=Sun)
        sample_trips = {
            0: [
                {'unit': 'Unit #05', 'route': 'Manila – North Port', 'time': '06:00 – 08:20', 'status': 'Completed'},
                {'unit': 'Unit #03', 'route': 'South Terminal Loop', 'time': '14:00 – 15:05', 'status': 'Completed'},
            ],
            1: [
                {'unit': 'Unit #08', 'route': 'Central – Airport', 'time': '07:30 – 08:15', 'status': 'Completed'},
            ],
            2: [
                {'unit': 'Unit #12', 'route': 'Manila – North Port', 'time': '06:00 – 08:20', 'status': 'Ongoing'},
                {'unit': 'Unit #05', 'route': 'Depot Supply Run', 'time': '10:00 – 10:50', 'status': 'Upcoming'},
                {'unit': 'Unit #03', 'route': 'Central – Airport', 'time': '15:00 – 15:45', 'status': 'Upcoming'},
            ],
            3: [
                {'unit': 'Unit #08', 'route': 'South Terminal Loop', 'time': '08:00 – 09:05', 'status': 'Upcoming'},
                {'unit': 'Unit #01', 'route': 'Manila – North Port', 'time': '12:00 – 14:20', 'status': 'Upcoming'},
            ],
            4: [
                {'unit': 'Unit #05', 'route': 'Central – Airport', 'time': '09:00 – 09:45', 'status': 'Upcoming'},
            ],
            5: [], 6: [],
        }
        for i, label in enumerate(day_labels):
            d = monday + dt.timedelta(days=i)
            days.append({'label': label, 'date': str(d.day), 'today': d == today, 'trips': sample_trips.get(i, [])})
        context['week_days'] = days
        context['stats'] = {'total': 9, 'ongoing': 1, 'upcoming': 5, 'completed': 3}
        context['schedules'] = [
            {'id': 'TRP-001', 'unit': 'Unit #05', 'driver': 'Marco Dela Cruz', 'origin': 'Manila Hub', 'destination': 'North Port', 'departure': '06:00', 'date': 'Mon Mar 18', 'eta': '08:20', 'status': 'Completed'},
            {'id': 'TRP-002', 'unit': 'Unit #08', 'driver': 'Juan Luna', 'origin': 'Central Station', 'destination': 'Airport Road', 'departure': '07:30', 'date': 'Tue Mar 19', 'eta': '08:15', 'status': 'Completed'},
            {'id': 'TRP-003', 'unit': 'Unit #03', 'driver': 'Rico Reyes', 'origin': 'South Terminal', 'destination': 'Quezon Service', 'departure': '14:00', 'date': 'Mon Mar 18', 'eta': '15:05', 'status': 'Completed'},
            {'id': 'TRP-004', 'unit': 'Unit #12', 'driver': 'Elena Santos', 'origin': 'Manila Hub', 'destination': 'North Port', 'departure': '06:00', 'date': 'Wed Mar 20', 'eta': '08:20', 'status': 'Ongoing'},
            {'id': 'TRP-005', 'unit': 'Unit #05', 'driver': 'Marco Dela Cruz', 'origin': 'South Depot', 'destination': 'Manila Hub', 'departure': '10:00', 'date': 'Wed Mar 20', 'eta': '10:50', 'status': 'Upcoming'},
            {'id': 'TRP-006', 'unit': 'Unit #03', 'driver': 'Rico Reyes', 'origin': 'Central Station', 'destination': 'Airport Road', 'departure': '15:00', 'date': 'Wed Mar 20', 'eta': '15:45', 'status': 'Upcoming'},
            {'id': 'TRP-007', 'unit': 'Unit #08', 'driver': 'Juan Luna', 'origin': 'South Terminal', 'destination': 'Quezon Service', 'departure': '08:00', 'date': 'Thu Mar 21', 'eta': '09:05', 'status': 'Upcoming'},
            {'id': 'TRP-008', 'unit': 'Unit #01', 'driver': 'Lito Lapid', 'origin': 'Manila Hub', 'destination': 'North Port', 'departure': '12:00', 'date': 'Thu Mar 21', 'eta': '14:20', 'status': 'Upcoming'},
            {'id': 'TRP-009', 'unit': 'Unit #05', 'driver': 'Marco Dela Cruz', 'origin': 'Central Station', 'destination': 'Airport Road', 'departure': '09:00', 'date': 'Fri Mar 22', 'eta': '09:45', 'status': 'Upcoming'},
        ]
        return context

class ServiceLogsView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = [
            {'id': 'SVC-001', 'vehicle': 'Unit #02', 'plate': 'XYZ-5678', 'type': 'Oil Change', 'technician': 'Ben Santos', 'date': 'Mar 15, 2026', 'cost': '3,500', 'status': 'Completed'},
            {'id': 'SVC-002', 'vehicle': 'Unit #07', 'plate': 'GHI-3344', 'type': 'Brake Service', 'technician': 'Carlo Reyes', 'date': 'Mar 14, 2026', 'cost': '8,200', 'status': 'Completed'},
            {'id': 'SVC-003', 'vehicle': 'Unit #04', 'plate': 'QRS-3456', 'type': 'Tire Replacement', 'technician': 'Ben Santos', 'date': 'Mar 18, 2026', 'cost': '12,000', 'status': 'Pending'},
            {'id': 'SVC-004', 'vehicle': 'Unit #01', 'plate': 'ABC-1234', 'type': 'General Inspection', 'technician': 'Rodel Cruz', 'date': 'Mar 10, 2026', 'cost': '1,500', 'status': 'Completed'},
            {'id': 'SVC-005', 'vehicle': 'Unit #08', 'plate': 'JKL-5566', 'type': 'Oil Change', 'technician': 'Carlo Reyes', 'date': 'Mar 05, 2026', 'cost': '3,500', 'status': 'Completed'},
            {'id': 'SVC-006', 'vehicle': 'Unit #03', 'plate': 'LMN-9012', 'type': 'Engine Overhaul', 'technician': 'Rodel Cruz', 'date': 'Mar 20, 2026', 'cost': '45,000', 'status': 'Pending'},
            {'id': 'SVC-007', 'vehicle': 'Unit #05', 'plate': 'JKL-7890', 'type': 'Oil Change', 'technician': 'Ben Santos', 'date': 'Feb 20, 2026', 'cost': '3,500', 'status': 'Overdue'},
            {'id': 'SVC-008', 'vehicle': 'Unit #06', 'plate': 'DEF-1122', 'type': 'Brake Service', 'technician': 'Carlo Reyes', 'date': 'Feb 15, 2026', 'cost': '7,800', 'status': 'Overdue'},
        ]
        context['stats'] = {'completed': 5, 'pending': 2, 'overdue': 2, 'total_cost': '84,500'}
        return context

class FuelMonitoringView(HtmxTemplateMixin, TemplateView):
    template_name = 'fuel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # DOE Oil Price Bulletin — Week of Mar 18, 2026 (reference data, no public API)
        context['doe_prices'] = {
            'week': 'Mar 18 – 24, 2026',
            'types': [
                {'name': 'Diesel',    'price': '58.35', 'change': -0.50},
                {'name': 'Unleaded',  'price': '64.80', 'change': 0.00},
                {'name': 'Premium',   'price': '71.20', 'change': 0.80},
                {'name': 'Kerosene',  'price': '52.10', 'change': -0.30},
            ]
        }
        context['kpi'] = {
            'total_liters': '2,841', 'total_cost': '165,769',
            'avg_efficiency': '6.8', 'top_unit': 'Unit #07',
            'top_unit_liters': '412', 'budget': '200,000',
            'budget_remaining': '₱34,231', 'over_budget': False,
        }
        context['fuel_logs'] = [
            {'id': 'FUL-001', 'unit': 'Unit #05', 'driver': 'Marco Dela Cruz', 'fuel_type': 'Diesel', 'liters': 95.0, 'price_per_liter': '58.35', 'total_cost': '5,543', 'odometer': '45,821', 'efficiency': 7.2, 'date': 'Mar 18, 2026'},
            {'id': 'FUL-002', 'unit': 'Unit #08', 'driver': 'Juan Luna', 'fuel_type': 'Diesel', 'liters': 80.0, 'price_per_liter': '58.35', 'total_cost': '4,668', 'odometer': '22,103', 'efficiency': 6.5, 'date': 'Mar 18, 2026'},
            {'id': 'FUL-003', 'unit': 'Unit #07', 'driver': 'Lito Lapid', 'fuel_type': 'Diesel', 'liters': 120.0, 'price_per_liter': '58.35', 'total_cost': '7,002', 'odometer': '88,420', 'efficiency': 5.9, 'date': 'Mar 17, 2026'},
            {'id': 'FUL-004', 'unit': 'Unit #01', 'driver': 'Marco Dela Cruz', 'fuel_type': 'Diesel', 'liters': 100.0, 'price_per_liter': '58.85', 'total_cost': '5,885', 'odometer': '31,200', 'efficiency': 7.8, 'date': 'Mar 16, 2026'},
            {'id': 'FUL-005', 'unit': 'Unit #03', 'driver': 'Elena Santos', 'fuel_type': 'Diesel', 'liters': 85.0, 'price_per_liter': '58.85', 'total_cost': '5,002', 'odometer': '54,780', 'efficiency': 6.1, 'date': 'Mar 15, 2026'},
            {'id': 'FUL-006', 'unit': 'Unit #06', 'driver': 'Santi Go', 'fuel_type': 'Unleaded', 'liters': 45.0, 'price_per_liter': '64.80', 'total_cost': '2,916', 'odometer': '18,330', 'efficiency': 9.4, 'date': 'Mar 15, 2026'},
            {'id': 'FUL-007', 'unit': 'Unit #05', 'driver': 'Marco Dela Cruz', 'fuel_type': 'Diesel', 'liters': 90.0, 'price_per_liter': '58.85', 'total_cost': '5,297', 'odometer': '45,280', 'efficiency': 7.0, 'date': 'Mar 12, 2026'},
        ]
        return context

class AnalyticsView(HtmxTemplateMixin, TemplateView):
    template_name = 'analytics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kpis'] = [
            {'label': 'Total Trips', 'value': '184', 'change': '+12', 'trend': 'up'},
            {'label': 'Total Distance', 'value': '9,241 km', 'change': '+8%', 'trend': 'up'},
            {'label': 'Fuel Cost', 'value': '₱165,769', 'change': '-3%', 'trend': 'down'},
            {'label': 'Fleet Utilization', 'value': '78%', 'change': '+5%', 'trend': 'up'},
        ]
        context['trips_chart'] = [
            {'day': 'Mon', 'count': 12, 'pct': 67},
            {'day': 'Tue', 'count': 18, 'pct': 100},
            {'day': 'Wed', 'count': 15, 'pct': 83},
            {'day': 'Thu', 'count': 10, 'pct': 56},
            {'day': 'Fri', 'count': 14, 'pct': 78},
            {'day': 'Sat', 'count': 6, 'pct': 33},
            {'day': 'Sun', 'count': 3, 'pct': 17},
        ]
        context['fuel_chart'] = [
            {'month': 'Oct', 'label_k': '148', 'pct': 76},
            {'month': 'Nov', 'label_k': '162', 'pct': 83},
            {'month': 'Dec', 'label_k': '195', 'pct': 100},
            {'month': 'Jan', 'label_k': '171', 'pct': 88},
            {'month': 'Feb', 'label_k': '158', 'pct': 81},
            {'month': 'Mar', 'label_k': '166', 'pct': 85},
        ]
        context['vehicle_perf'] = [
            {'unit': 'Unit #12', 'plate': 'MNO-2345', 'driver': 'Elena Santos', 'trips': 28, 'distance': '1,420 km', 'fuel': 198, 'eff': 7.2, 'util': 92},
            {'unit': 'Unit #05', 'plate': 'JKL-7890', 'driver': 'Marco Dela Cruz', 'trips': 25, 'distance': '1,260 km', 'fuel': 175, 'eff': 7.2, 'util': 84},
            {'unit': 'Unit #07', 'plate': 'GHI-3344', 'driver': 'Lito Lapid', 'trips': 23, 'distance': '1,840 km', 'fuel': 312, 'eff': 5.9, 'util': 79},
            {'unit': 'Unit #08', 'plate': 'JKL-5566', 'driver': 'Juan Luna', 'trips': 20, 'distance': '980 km', 'fuel': 151, 'eff': 6.5, 'util': 71},
            {'unit': 'Unit #03', 'plate': 'LMN-9012', 'driver': 'Rico Reyes', 'trips': 18, 'distance': '870 km', 'fuel': 143, 'eff': 6.1, 'util': 63},
        ]
        context['top_routes'] = [
            {'name': 'Manila – North Port Express', 'trips': 54, 'pct': 100, 'color': '#3b82f6'},
            {'name': 'Central – Airport Connector', 'trips': 41, 'pct': 76, 'color': '#10b981'},
            {'name': 'South Terminal Loop', 'trips': 37, 'pct': 69, 'color': '#f59e0b'},
            {'name': 'Depot Supply Run', 'trips': 29, 'pct': 54, 'color': '#8b5cf6'},
            {'name': 'Cebu – Davao Trunk Line', 'trips': 7, 'pct': 13, 'color': '#f43f5e'},
        ]
        context['status_breakdown'] = [
            {'label': 'Completed', 'count': 148, 'pct': 80, 'color': '#10b981'},
            {'label': 'Ongoing', 'count': 12, 'pct': 7, 'color': '#3b82f6'},
            {'label': 'Upcoming', 'count': 18, 'pct': 10, 'color': '#8b5cf6'},
            {'label': 'Cancelled', 'count': 6, 'pct': 3, 'color': '#f43f5e'},
        ]
        return context

class PersonnelView(HtmxTemplateMixin, TemplateView):
    template_name = 'personnel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personnel'] = [
            {'name': 'Rafael Mendoza', 'initials': 'RM', 'role': 'Fleet Manager', 'department': 'Operations', 'dept_color': 'from-blue-600 to-blue-800', 'contact': '+63 917 123 4567', 'since': 'Jan 2020', 'status': 'Active'},
            {'name': 'Carla Santos', 'initials': 'CS', 'role': 'Dispatcher', 'department': 'Operations', 'dept_color': 'from-blue-600 to-blue-800', 'contact': '+63 918 234 5678', 'since': 'Mar 2021', 'status': 'Active'},
            {'name': 'Ben Reyes', 'initials': 'BR', 'role': 'Lead Technician', 'department': 'Maintenance', 'dept_color': 'from-amber-600 to-amber-800', 'contact': '+63 922 345 6789', 'since': 'Jun 2019', 'status': 'Active'},
            {'name': 'Ana Cruz', 'initials': 'AC', 'role': 'Logistics Coordinator', 'department': 'Logistics', 'dept_color': 'from-emerald-600 to-emerald-800', 'contact': '+63 926 456 7890', 'since': 'Sep 2022', 'status': 'Active'},
            {'name': 'Tony Ramos', 'initials': 'TR', 'role': 'Mechanic', 'department': 'Maintenance', 'dept_color': 'from-amber-600 to-amber-800', 'contact': '+63 927 567 8901', 'since': 'Feb 2021', 'status': 'On Leave'},
            {'name': 'Lena Flores', 'initials': 'LF', 'role': 'Finance Officer', 'department': 'Finance', 'dept_color': 'from-purple-600 to-purple-800', 'contact': '+63 929 678 9012', 'since': 'Apr 2020', 'status': 'Active'},
            {'name': 'Marco Vega', 'initials': 'MV', 'role': 'Route Planner', 'department': 'Logistics', 'dept_color': 'from-emerald-600 to-emerald-800', 'contact': '+63 931 789 0123', 'since': 'Jul 2023', 'status': 'Active'},
            {'name': 'Sonia Go', 'initials': 'SG', 'role': 'HR Officer', 'department': 'Administration', 'dept_color': 'from-rose-600 to-rose-800', 'contact': '+63 933 890 1234', 'since': 'Nov 2021', 'status': 'On Leave'},
            {'name': 'Carlo Reyes', 'initials': 'CR', 'role': 'Mechanic', 'department': 'Maintenance', 'dept_color': 'from-amber-600 to-amber-800', 'contact': '+63 935 901 2345', 'since': 'Aug 2020', 'status': 'Active'},
            {'name': 'Diana Lim', 'initials': 'DL', 'role': 'Admin Assistant', 'department': 'Administration', 'dept_color': 'from-rose-600 to-rose-800', 'contact': '+63 936 012 3456', 'since': 'Jan 2024', 'status': 'Active'},
        ]
        context['stats'] = {'total': 10, 'active': 8, 'on_leave': 2, 'departments': 5}
        return context
