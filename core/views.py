from django.shortcuts import render
from django.views.generic import TemplateView
import datetime

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock data for demonstration
        context['units'] = [
            {'id': 'Unit #05', 'name': 'Marco Dela Cruz', 'status': 'IN TRANSIT', 'eta': '173 min', 'status_class': 'status-in-transit'},
            {'id': 'Unit #08', 'name': 'Juan Luna', 'status': 'IN TRANSIT', 'eta': '19 min', 'status_class': 'status-in-transit'},
            {'id': 'Unit #12', 'name': 'Elena Santos', 'status': 'STALLED', 'eta': '--', 'status_class': 'status-stalled'},
            {'id': 'Unit #03', 'name': 'Rico Reyes', 'status': 'IN TRANSIT', 'eta': '136 min', 'status_class': 'status-in-transit'},
        ]
        return context

def system_status(request):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return render(request, 'partials/status_badge.html', {'time': now})
