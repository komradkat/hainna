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
