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
        context['stats'] = {'active_units': 0, 'idle_units': 0, 'total_units': 0, 'efficiency': '0%', 'on_time_rate': '0%'}
        context['vehicles'] = []
        return context

class LiveTrackingView(HtmxTemplateMixin, TemplateView):
    template_name = 'tracking/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = []
        return context

class FleetVehiclesView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = []
        return context

class DriversView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = []
        context['stats'] = {'active': 0, 'off_duty': 0, 'on_leave': 0, 'total': 0}
        return context

class RoutesView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = []
        context['route_stats'] = {'total': 0, 'active': 0, 'total_km': '0 km', 'units_on_route': 0, 'avg_time': '0h 0m'}
        context['zones'] = []
        context['zone_stats'] = {'total': 0, 'active': 0, 'units_inside': 0, 'alerts': 0}
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
        monday = today - dt.timedelta(days=today.weekday())
        days = []
        day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, label in enumerate(day_labels):
            d = monday + dt.timedelta(days=i)
            days.append({'label': label, 'date': str(d.day), 'today': d == today, 'trips': []})
        context['week_days'] = days
        context['stats'] = {'total': 0, 'ongoing': 0, 'upcoming': 0, 'completed': 0}
        context['schedules'] = []
        return context

class ServiceLogsView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = []
        context['stats'] = {'completed': 0, 'pending': 0, 'overdue': 0, 'total_cost': '0'}
        return context

class FuelMonitoringView(HtmxTemplateMixin, TemplateView):
    template_name = 'fuel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doe_prices'] = {
            'week': 'Current Week',
            'types': [
                {'name': 'Diesel',    'price': '0.00', 'change': 0.00},
                {'name': 'Unleaded',  'price': '0.00', 'change': 0.00},
                {'name': 'Premium',   'price': '0.00', 'change': 0.00},
                {'name': 'Kerosene',  'price': '0.00', 'change': 0.00},
            ]
        }
        context['kpi'] = {
            'total_liters': '0', 'total_cost': '0',
            'avg_efficiency': '0.0', 'top_unit': '-',
            'top_unit_liters': '0', 'budget': '0',
            'budget_remaining': '₱0', 'over_budget': False,
        }
        context['fuel_logs'] = []
        return context

class AnalyticsView(HtmxTemplateMixin, TemplateView):
    template_name = 'analytics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kpis'] = [
            {'label': 'Total Trips', 'value': '0', 'change': '0', 'trend': 'none'},
            {'label': 'Total Distance', 'value': '0 km', 'change': '0%', 'trend': 'none'},
            {'label': 'Fuel Cost', 'value': '₱0', 'change': '0%', 'trend': 'none'},
            {'label': 'Fleet Utilization', 'value': '0%', 'change': '0%', 'trend': 'none'},
        ]
        context['trips_chart'] = [
            {'day': 'Mon', 'count': 0, 'pct': 0},
            {'day': 'Tue', 'count': 0, 'pct': 0},
            {'day': 'Wed', 'count': 0, 'pct': 0},
            {'day': 'Thu', 'count': 0, 'pct': 0},
            {'day': 'Fri', 'count': 0, 'pct': 0},
            {'day': 'Sat', 'count': 0, 'pct': 0},
            {'day': 'Sun', 'count': 0, 'pct': 0},
        ]
        context['fuel_chart'] = [
            {'month': 'Oct', 'label_k': '0', 'pct': 0},
            {'month': 'Nov', 'label_k': '0', 'pct': 0},
            {'month': 'Dec', 'label_k': '0', 'pct': 0},
            {'month': 'Jan', 'label_k': '0', 'pct': 0},
            {'month': 'Feb', 'label_k': '0', 'pct': 0},
            {'month': 'Mar', 'label_k': '0', 'pct': 0},
        ]
        context['vehicle_perf'] = []
        context['top_routes'] = []
        context['status_breakdown'] = []
        return context

class PersonnelView(HtmxTemplateMixin, TemplateView):
    template_name = 'personnel/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personnel'] = []
        context['stats'] = {'total': 0, 'active': 0, 'on_leave': 0, 'departments': 0}
        return context

class UserManagementView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = []
        context['stats'] = {'total': 0, 'active': 0, 'admins': 0, 'suspended': 0}
        return context
