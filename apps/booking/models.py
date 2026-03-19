from django.db import models
from fleet.models import Route, Vehicle

class Trip(models.Model):
    DISPATCH_TYPES = [
        ('Fill-up', 'Until Full'),
        ('Scheduled', 'Scheduled Time'),
    ]
    STATUS_CHOICES = [
        ('Pending Vehicle', 'Waiting for Van'),
        ('Standing By', 'Standing By'),
        ('Loading', 'Calling Passengers'),
        ('Dispatched', 'Dispatched / In Transit'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='trips', help_text="Can be unassigned if van is Arriving Soon")
    
    dispatch_type = models.CharField(max_length=50, choices=DISPATCH_TYPES, default='Fill-up')
    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="Strict departure trigger if Scheduled")
    ticket_color = models.CharField(max_length=50, default="Blue", help_text="e.g., Blue, Red, Yellow for passenger calling groups")
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Vehicle')
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        v = self.vehicle.plate_number if self.vehicle else "No Van Assigned"
        return f"{self.route.name} - [{self.ticket_color}] ({v})"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting in Terminal'),
        ('Boarded', 'Boarded'),
        ('Cancelled', 'Cancelled / No Show'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets')
    passenger_name = models.CharField(max_length=150, blank=True, help_text="Optional Passenger Name")
    seat_number = models.CharField(max_length=20, help_text="Assigned matrix seat")
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Waiting')
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        p = self.passenger_name if self.passenger_name else "Walk-in Guest"
        return f"Tck-{self.id}: {p} (Seat {self.seat_number})"
