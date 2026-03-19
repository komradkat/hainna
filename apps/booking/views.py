from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from core.views import HtmxTemplateMixin
from .models import Trip, Ticket
from fleet.models import Route, Vehicle

class BookingPOSView(HtmxTemplateMixin, TemplateView):
    template_name = 'booking/pos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Route.objects.filter(status='Active')
        context['active_trips'] = Trip.objects.exclude(status__in=['Completed', 'Cancelled']).order_by('-date_added')
        return context

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

def public_board_feed(request):
    trips = Trip.objects.filter(status__in=['Pending Vehicle', 'Standing By', 'Loading']).order_by('-last_updated')
    
    loading = trips.filter(status='Loading')
    standing_by = trips.filter(status='Standing By')
    arriving = trips.filter(status='Pending Vehicle')
    
    return render(request, 'booking/partials/board_feed.html', {
        'loading': loading,
        'standing_by': standing_by,
        'arriving': arriving
    })

class DispatchBoardView(HtmxTemplateMixin, TemplateView):
    template_name = 'booking/dispatch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_trips'] = Trip.objects.exclude(status__in=['Completed', 'Cancelled']).order_by('date_added')
        return context

def update_trip_status(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        new_status = request.POST.get('status')
        if new_status in dict(Trip.STATUS_CHOICES):
            trip.status = new_status
            trip.save()
            
            if new_status == 'Dispatched':
                trip.tickets.exclude(status='Cancelled').update(status='Boarded')
                
    return redirect('booking:dispatch')
