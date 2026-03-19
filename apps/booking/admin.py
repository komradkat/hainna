from django.contrib import admin
from .models import Trip, Ticket

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'vehicle', 'dispatch_type', 'ticket_color', 'status')
    list_filter = ('dispatch_type', 'status', 'ticket_color')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'passenger_name', 'seat_number', 'status')
    list_filter = ('status', 'trip__route')
