from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.views import HtmxTemplateMixin
from .models import Trip, Ticket
from fleet.models import Route, Vehicle, Terminal

@login_required
def select_terminal(request):
    terminals = Terminal.objects.all().order_by('name')
    base_template = 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
    return render(request, 'booking/select_terminal.html', {
        'terminals': terminals,
        'base_template': base_template
    })

@login_required
def set_terminal(request, terminal_id):
    from django.urls import reverse
    terminal = get_object_or_404(Terminal, id=terminal_id)
    request.session['active_terminal_id'] = terminal.id
    request.session['active_terminal_name'] = terminal.name
    
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('booking:pos')
    return redirect(next_url)

class BookingPOSView(HtmxTemplateMixin, TemplateView):
    template_name = 'booking/pos.html'

    def dispatch(self, request, *args, **kwargs):
        terminal_id = request.session.get('active_terminal_id')
        if not terminal_id or not Terminal.objects.filter(id=terminal_id).exists():
            from django.urls import reverse
            return redirect(f"{reverse('booking:select_terminal')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terminal_id = self.request.session.get('active_terminal_id')
        terminal = Terminal.objects.filter(id=terminal_id).first()
        
        if terminal and terminal.is_master_hub:
            context['routes'] = Route.objects.filter(status='Active')
            context['active_trips'] = Trip.objects.exclude(status__in=['Completed', 'Cancelled']).order_by('date_added')
            context['is_master'] = True
        else:
            context['routes'] = Route.objects.filter(origin_id=terminal_id, status='Active')
            context['active_trips'] = Trip.objects.filter(route__origin_id=terminal_id).exclude(status__in=['Completed', 'Cancelled']).order_by('date_added')
            context['is_master'] = False
            
        return context

@login_required
def trip_details_htmx(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    tickets = trip.tickets.all()
    taken_seats = [t.seat_number for t in tickets if t.status != 'Cancelled']
    
    capacity = 15
    if trip.vehicle and trip.vehicle.capacity:
        try:
            numbers = ''.join(filter(str.isdigit, trip.vehicle.capacity))
            if numbers:
                capacity = int(numbers)
        except:
            pass
            
    capacity = min(capacity, 24) # Cap capacity to a hard limit of 24
    seats = []
    for i in range(1, capacity + 1):
        seats.append({
            'number': str(i),
            'is_taken': str(i) in taken_seats
        })
        
    return render(request, 'booking/partials/trip_details.html', {
        'trip': trip,
        'seats': seats,
        'available_count': capacity - len(taken_seats)
    })

@login_required
def issue_ticket(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        seat_number = request.POST.get('seat_number')
        passenger_name = request.POST.get('passenger_name', '')
        
        trip = get_object_or_404(Trip, id=trip_id)
        
        if trip.tickets.filter(seat_number=seat_number, status__in=['Waiting', 'Boarded']).exists():
            return HttpResponse(f"<div class='text-red-500 font-bold p-3 bg-red-500/10 rounded-lg'>Error: Seat {seat_number} already taken!</div>")
            
        ticket = Ticket.objects.create(
            trip=trip,
            passenger_name=passenger_name,
            seat_number=seat_number,
            fare=150.00,
            status='Waiting'
        )
        
        return redirect(request.META.get('HTTP_REFERER', 'booking:dispatch'))
    return HttpResponse("Invalid Request")

class PublicBoardView(TemplateView):
    template_name = 'booking/public_board.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import urllib.parse
        context['terminal_name'] = urllib.parse.unquote(self.kwargs.get('terminal_name', 'Terminal'))
        return context

def public_board_feed(request, terminal_name):
    import urllib.parse, datetime
    term = urllib.parse.unquote(terminal_name)
    
    outbound = Trip.objects.filter(route__origin__name__iexact=term)
    loading = outbound.filter(status='Loading').order_by('last_updated')
    standing_by = outbound.filter(status='Standing By').order_by('last_updated')
    
    inbound_arriving = list(Trip.objects.filter(
        route__destination__name__iexact=term,
        status='Dispatched'
    ).select_related('route'))
    
    def calculate_eta(trip):
        try:
            # Assuming van avgs 60 km/h to compute transit duration accurately
            hours = float(trip.route.distance_km) / 60.0
            return trip.last_updated + datetime.timedelta(hours=hours)
        except:
            return trip.last_updated

    inbound_arriving.sort(key=calculate_eta)
    
    return render(request, 'booking/partials/board_feed.html', {
        'loading': loading,
        'standing_by': standing_by,
        'arriving': inbound_arriving,
        'terminal_name': term
    })

class DispatchBoardView(HtmxTemplateMixin, TemplateView):
    template_name = 'booking/dispatch.html'

    def dispatch(self, request, *args, **kwargs):
        terminal_id = request.session.get('active_terminal_id')
        if not terminal_id or not Terminal.objects.filter(id=terminal_id).exists():
            from django.urls import reverse
            return redirect(f"{reverse('booking:select_terminal')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terminal_id = self.request.session.get('active_terminal_id')
        terminal = Terminal.objects.filter(id=terminal_id).first()
        
        if terminal and terminal.is_master_hub:
            context['active_trips'] = Trip.objects.exclude(status__in=['Completed', 'Cancelled', 'Dispatched']).order_by('date_added')
            context['inbound_trips'] = Trip.objects.filter(status='Dispatched').order_by('last_updated')
            context['is_master_board'] = True
        else:
            context['active_trips'] = Trip.objects.filter(route__origin_id=terminal_id).exclude(status__in=['Completed', 'Cancelled', 'Dispatched']).order_by('date_added')
            context['inbound_trips'] = Trip.objects.filter(route__destination_id=terminal_id, status='Dispatched').order_by('last_updated')
            context['is_master_board'] = False
            
        return context

@login_required
def update_trip_status(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        new_status = request.POST.get('status')
        if new_status in dict(Trip.STATUS_CHOICES):
            old_status = trip.status
            trip.status = new_status
            trip.save()
            
            if new_status == 'Dispatched':
                trip.tickets.exclude(status='Cancelled').update(status='Boarded')
            elif new_status == 'Completed' and old_status != 'Completed':
                if trip.vehicle:
                    # Auto-queue return trip
                    reverse_route = Route.objects.filter(
                        origin=trip.route.destination,
                        destination=trip.route.origin
                    ).first()
                    
                    if reverse_route:
                        Trip.objects.create(
                            route=reverse_route,
                            vehicle=trip.vehicle,
                            status='Standing By',
                            dispatch_type=trip.dispatch_type
                        )
                
    return redirect('booking:dispatch')
