from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime

class HtmxTemplateMixin(LoginRequiredMixin):
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
        from fleet.models import Vehicle, Driver, Route, Terminal, MaintenanceLog
        from booking.models import Trip, Ticket
        from users.models import CustomUser
        from django.db.models import Sum
        from django.utils import timezone

        today = timezone.localdate()
        
        # Fleet and Drivers
        total_units = Vehicle.objects.count()
        active_units = Vehicle.objects.filter(status='Active').count()
        total_drivers = Driver.objects.count()
        
        # Logistics
        total_routes = Route.objects.count()
        total_terminals = Terminal.objects.count()
        
        # Dispatch
        today_trips = Trip.objects.filter(date_added__date=today)
        active_trips = today_trips.exclude(status__in=['Completed', 'Cancelled']).count()
        total_trips_today = today_trips.count()
        
        # Revenue
        today_tickets = Ticket.objects.filter(date_added__date=today)
        today_revenue = today_tickets.aggregate(total=Sum('fare'))['total'] or 0.00
        
        # Infrastructure
        pending_maintenance = MaintenanceLog.objects.exclude(status='Resolved').count()
        
        # Personnel
        active_staff = CustomUser.objects.filter(status='Active').count()
        
        context['stats'] = {
            'active_units': active_units,
            'total_units': total_units,
            'efficiency': f"{int((active_units / total_units) * 100)}%" if total_units else "0%",
            'total_drivers': total_drivers,
            'total_routes': total_routes,
            'total_terminals': total_terminals,
            'active_trips': active_trips,
            'total_trips_today': total_trips_today,
            'today_revenue': today_revenue,
            'pending_maintenance': pending_maintenance,
            'active_staff': active_staff
        }
        
        # Vehicles in transit list
        vehicles = Vehicle.objects.filter(status='Active').select_related('driver').order_by('-last_updated')[:10]
        transit_list = []
        for v in vehicles:
            transit_list.append({
                'id': v.plate_number,
                'driver': str(v.driver) if v.driver else 'Unassigned',
                'status': 'Moving' if v.status == 'Active' else v.status,
                'eta': 'Unknown',
                'destination': 'Tracking...'
            })
        context['vehicles'] = transit_list
        
        # Spatial Map Layers Context
        context['map_terminals'] = list(Terminal.objects.values('name', 'location_lat', 'location_lng'))
        context['map_routes'] = list(Route.objects.exclude(path_coordinates='').values('name', 'path_coordinates', 'color'))
        
        return context

class LoginLoadingView(LoginRequiredMixin, TemplateView):
    template_name = 'users/loading.html'

class LiveTrackingView(HtmxTemplateMixin, TemplateView):
    template_name = 'tracking/index.html'

    def get_context_data(self, **kwargs):
        from fleet.models import Vehicle
        from fleet import traccar
        
        context = super().get_context_data(**kwargs)
        
        vehicles = Vehicle.objects.filter(
            traccar_device_id__isnull=False
        ).exclude(traccar_device_id='').select_related('driver')

        # Move live position fetching to the background (polled via JSON)
        # to prevent page hang on initial load.
        context['units'] = [{
            'id': v.plate_number,
            'vehicle_id': v.id,
            'name': str(v.driver) if v.driver else 'Unassigned',
            'plate': v.plate_number,
            'status': 'Offline', # Initially offline until first set of data arrives
            'speed': 'N/A',
            'lat': None,
            'lng': None,
            'pos': '[0, 0]',
            'battery': 'N/A',
            'has_gps': False,
        } for v in vehicles]
        
        context['traccar_ok'] = True # Assume OK until background poll proves otherwise
        context['traccar_url'] = self.request.build_absolute_uri('/live-tracking/positions/')
        return context


@login_required
def tracking_positions(request):
    """JSON endpoint polled by the live map every 5s to update vehicle positions."""
    from fleet.models import Vehicle
    from fleet import traccar
    
    positions = traccar.get_all_positions()
    traccar_ok = traccar.is_connected()
    
    vehicles = Vehicle.objects.filter(
        traccar_device_id__isnull=False
    ).exclude(traccar_device_id='').select_related('driver')
    
    units = []
    for v in vehicles:
        pos_data = positions.get(str(v.traccar_device_id), {})
        lat = pos_data.get('lat')
        lng = pos_data.get('lng')
        speed = pos_data.get('speed', 0)
        
        if not lat:
            continue  # Skip vehicles with no GPS fix
        
        if speed > 5:
            status = 'Moving'
        elif speed > 0:
            status = 'Idle'
        else:
            status = 'Stopped'
            
        units.append({
            'id': v.plate_number,
            'name': str(v.driver) if v.driver else 'Unassigned',
            'status': status,
            'speed': round(speed, 1),
            'speed_display': f"{speed:.1f} km/h",
            'lat': lat,
            'lng': lng,
        })
    
    return JsonResponse({'units': units, 'traccar_ok': traccar_ok})


@login_required
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
