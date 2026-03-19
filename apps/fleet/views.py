from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import HtmxTemplateMixin
from .models import Vehicle, Driver, MaintenanceLog, Route, Zone
from .forms import VehicleForm, DriverForm, ServiceLogForm, RouteForm, ZoneForm

class FleetVehiclesView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all().order_by('-date_added')
        return context

class AddVehicleView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VehicleForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = FleetVehiclesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditVehicleView(HtmxTemplateMixin, TemplateView):
    template_name = 'fleet/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('pk'))
        context['form'] = VehicleForm(instance=vehicle)
        context['is_edit'] = True
        context['vehicle'] = vehicle
        return context

    def post(self, request, *args, **kwargs):
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('pk'))
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            list_view = FleetVehiclesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'vehicle': vehicle,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteVehicleView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        vehicle = get_object_or_404(Vehicle, pk=self.kwargs.get('pk'))
        vehicle.delete()
        
        list_view = FleetVehiclesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class DriversView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all().order_by('-date_added')
        context['stats'] = {
            'active': Driver.objects.filter(status='Active').count(),
            'off_duty': Driver.objects.filter(status='Off Duty').count(),
            'on_leave': Driver.objects.filter(status='On Leave').count(),
            'total': Driver.objects.count()
        }
        return context

class AddDriverView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DriverForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = DriversView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditDriverView(HtmxTemplateMixin, TemplateView):
    template_name = 'drivers/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver = get_object_or_404(Driver, pk=self.kwargs.get('pk'))
        context['form'] = DriverForm(instance=driver)
        context['is_edit'] = True
        context['driver'] = driver
        return context

    def post(self, request, *args, **kwargs):
        driver = get_object_or_404(Driver, pk=self.kwargs.get('pk'))
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            list_view = DriversView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'driver': driver,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteDriverView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        driver = get_object_or_404(Driver, pk=self.kwargs.get('pk'))
        driver.delete()
        
        list_view = DriversView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class ServiceLogsView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = MaintenanceLog.objects.all().order_by('-date')
        from django.db.models import Sum
        context['stats'] = {
            'total_cost': MaintenanceLog.objects.aggregate(Sum('cost'))['cost__sum'] or 0,
            'scheduled': MaintenanceLog.objects.filter(status='Scheduled').count(),
            'in_progress': MaintenanceLog.objects.filter(status='In Progress').count(),
            'completed': MaintenanceLog.objects.filter(status='Completed').count(),
        }
        return context

class AddServiceLogView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceLogForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = ServiceLogForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = ServiceLogsView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditServiceLogView(HtmxTemplateMixin, TemplateView):
    template_name = 'service_logs/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log = get_object_or_404(MaintenanceLog, pk=self.kwargs.get('pk'))
        context['form'] = ServiceLogForm(instance=log)
        context['is_edit'] = True
        context['log'] = log
        return context

    def post(self, request, *args, **kwargs):
        log = get_object_or_404(MaintenanceLog, pk=self.kwargs.get('pk'))
        form = ServiceLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            list_view = ServiceLogsView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'log': log,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteServiceLogView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        log = get_object_or_404(MaintenanceLog, pk=self.kwargs.get('pk'))
        log.delete()
        
        list_view = ServiceLogsView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class RoutesView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Route.objects.all().order_by('-date_added')
        
        from django.db.models import Sum
        total_km = Route.objects.aggregate(Sum('distance_km'))['distance_km__sum'] or 0

        context['route_stats'] = {
            'total': Route.objects.count(),
            'active': Route.objects.filter(status='Active').count(),
            'total_km': f"{total_km} km",
            'units_on_route': 0,
            'avg_time': '0h 0m'
        }
        
        context['zones'] = Zone.objects.all().order_by('-date_added')
        context['zone_stats'] = {
            'total': Zone.objects.count(),
            'active': Zone.objects.count(),
            'units_inside': 0,
            'alerts': 0
        }
        return context

class AddRouteView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RouteForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = RoutesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditRouteView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = get_object_or_404(Route, pk=self.kwargs.get('pk'))
        context['form'] = RouteForm(instance=route)
        context['is_edit'] = True
        context['route'] = route
        return context

    def post(self, request, *args, **kwargs):
        route = get_object_or_404(Route, pk=self.kwargs.get('pk'))
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            list_view = RoutesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'route': route,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteRouteView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        route = get_object_or_404(Route, pk=self.kwargs.get('pk'))
        route.delete()
        list_view = RoutesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class AddZoneView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/zone_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ZoneForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            list_view = RoutesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditZoneView(HtmxTemplateMixin, TemplateView):
    template_name = 'routes/zone_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zone = get_object_or_404(Zone, pk=self.kwargs.get('pk'))
        context['form'] = ZoneForm(instance=zone)
        context['is_edit'] = True
        context['zone'] = zone
        return context

    def post(self, request, *args, **kwargs):
        zone = get_object_or_404(Zone, pk=self.kwargs.get('pk'))
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            list_view = RoutesView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'zone': zone,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteZoneView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        zone = get_object_or_404(Zone, pk=self.kwargs.get('pk'))
        zone.delete()
        list_view = RoutesView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)
