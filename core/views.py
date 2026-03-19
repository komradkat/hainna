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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'requires_password_change', False):
            from django.shortcuts import redirect
            return redirect('change_password')
        return super().get(request, *args, **kwargs)

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

class AddVehicleView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet/form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = FleetVehiclesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class DriversView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = []
        context['stats'] = {'active': 0, 'off_duty': 0, 'on_leave': 0, 'total': 0}
        return context

class AddDriverView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/form.html'
    
    def post(self, request, *args, **kwargs):
        # Return to drivers list after mock submission
        list_view = DriversView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class RoutesView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = []
        context['route_stats'] = {'total': 0, 'active': 0, 'total_km': '0 km', 'units_on_route': 0, 'avg_time': '0h 0m'}
        context['zones'] = []
        context['zone_stats'] = {'total': 0, 'active': 0, 'units_inside': 0, 'alerts': 0}
        return context

class AddRouteView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = RoutesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class AddZoneView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/zone_form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = RoutesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

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

class AddScheduleView(HtmxTemplateMixin, TemplateView):
    template_name = 'schedules/form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = SchedulesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class ServiceLogsView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = []
        context['stats'] = {'completed': 0, 'pending': 0, 'overdue': 0, 'total_cost': '0'}
        return context

class AddServiceLogView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = ServiceLogsView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

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

class AddFuelView(HtmxTemplateMixin, TemplateView):
    template_name = 'fuel/form.html'
    
    def post(self, request, *args, **kwargs):
        list_view = FuelMonitoringView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

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
        from users.models import CustomUser
        users = CustomUser.objects.all().order_by('last_name')
        
        personnel_list = []
        for u in users:
            # Map roles to some colors for the UI
            dept_colors = {
                'Logistics': 'from-blue-600 to-indigo-600',
                'Operations': 'from-emerald-600 to-teal-600',
                'Maintenance': 'from-orange-600 to-red-600',
                'Admin': 'from-purple-600 to-pink-600',
            }
            color = dept_colors.get(u.department, 'from-gray-600 to-slate-600')
            
            personnel_list.append({
                'pk': u.pk,
                'initials': u.initials,
                'name': u.get_full_name() or u.username,
                'role': u.role,
                'department': u.department or 'Unassigned',
                'dept_color': color,
                'contact': u.phone_number or u.email,
                'since': u.date_of_hire.strftime('%Y') if u.date_of_hire else 'N/A',
                'status': u.status,
            })
            
        context['personnel'] = personnel_list
        context['stats'] = {
            'total': users.count(),
            'active': users.filter(status='Active').count(),
            'on_leave': users.filter(status='On Leave').count(), # Status choices only has Active, Pending Verify, Suspended but template has On Leave
            'departments': users.values('department').distinct().count()
        }
        return context

class AddPersonnelView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from users.forms import UserForm
        context['form'] = UserForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        from users.forms import UserForm
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = PersonnelView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })
