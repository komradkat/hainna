from django.db import models
from django.conf import settings

class Driver(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Off Duty', 'Off Duty'),
        ('On Leave', 'On Leave'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Driver'})
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    contact_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    rating = models.FloatField(default=5.0)

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
        ('Out of Service', 'Out of Service'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_vehicles')
    plate_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=50, blank=True, null=True, verbose_name="VIN")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    mileage = models.IntegerField(default=0)
    capacity = models.CharField(max_length=50, blank=True, null=True)
    traccar_device_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Traccar Device ID", help_text="The unique identifier of this vehicle's GPS tracker device in Traccar")
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plate_number} - {self.make} {self.model} ({self.year})"

    @property
    def status_color(self):
        if self.status == 'Active':
            return 'text-emerald-500/70 border-emerald-500/20 bg-emerald-500/10'
        elif self.status == 'Maintenance':
            return 'text-amber-500/70 border-amber-500/20 bg-amber-500/10'
        return 'text-rose-500/70 border-rose-500/20 bg-rose-500/10'

class MaintenanceLog(models.Model):
    SERVICE_TYPES = [
        ('Preventive', 'Preventive Maintenance'),
        ('Repair', 'Repair'),
        ('Inspection', 'Inspection'),
        ('Cleaning', 'Cleaning'),
    ]
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_maintenance')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    date = models.DateField()
    odometer_reading = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    performed_by = models.CharField(max_length=100, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_type} - {self.vehicle.plate_number} ({self.date})"

class Terminal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location_lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Delayed', 'Delayed'),
    ]

    name = models.CharField(max_length=100)
    origin = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='outbound_routes')
    destination = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='inbound_routes')
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total route distance in kilometers")
    est_travel_time = models.CharField(max_length=50, help_text="Estimated travel time, e.g., '1h 30m'")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    color = models.CharField(max_length=20, default="#3b82f6", blank=True, help_text="Hex color code for map rendering")
    geofence_radius_meters = models.IntegerField(default=500, help_text="Meters around each terminal point to trigger arriving alerts")
    
    # Geographic Routing Cache
    waypoints = models.JSONField(default=list, blank=True, help_text="List of lat/lng coordinates for terminal routing stops explicitly plotted")
    path_coordinates = models.JSONField(default=list, blank=True, help_text="Snap-to-road polyline coordinates generated by OSRM")

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def path_json(self):
        import json
        return json.dumps(self.path_coordinates) if self.path_coordinates else "[]"

    @property
    def waypoints_json(self):
        import json
        return json.dumps(self.waypoints) if self.waypoints else "[]"

    def __str__(self):
        return f"{self.name} ({self.origin} - {self.destination})"

class Zone(models.Model):
    TYPE_CHOICES = [
        ('Delivery Hub', 'Delivery Hub'),
        ('Restricted', 'Restricted'),
        ('Waypoint', 'Waypoint'),
    ]

    name = models.CharField(max_length=100)
    zone_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    coordinates = models.TextField()
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.zone_type})"

    @property
    def color(self):
        if self.zone_type == 'Delivery Hub':
            return '#10b981'
        elif self.zone_type == 'Restricted':
            return '#ef4444'
        return '#3b82f6'
    
    @property
    def is_active(self):
        return True
