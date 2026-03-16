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
        # Mock recent alerts
        context['alerts'] = [
            {'unit': 'Unit #05', 'type': 'Deviation', 'priority': 'high', 'time': '5m ago'},
            {'unit': 'Unit #12', 'type': 'Stalled', 'priority': 'medium', 'time': '12m ago'},
        ]
        return context

class LiveTrackingView(HtmxTemplateMixin, TemplateView):
    template_name = 'tracking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock markers for vehicles
        context['units'] = [
            {'id': 'Unit #05', 'name': 'Marco Dela Cruz', 'pos': [11.24, 125.00]},
            {'id': 'Unit #08', 'name': 'Juan Luna', 'pos': [11.30, 124.90]},
            {'id': 'Unit #12', 'name': 'Elena Santos', 'pos': [11.15, 124.95]},
            {'id': 'Unit #03', 'name': 'Rico Reyes', 'pos': [11.25, 125.05]},
        ]
        return context

def system_status(request):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return render(request, 'partials/status_badge.html', {'time': now})
