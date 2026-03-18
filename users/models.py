from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Administrator', 'Administrator'),
        ('Fleet Manager', 'Fleet Manager'),
        ('Dispatcher', 'Dispatcher'),
        ('Maintenance Tech', 'Maintenance Tech'),
    )
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Pending Verify', 'Pending Verify'),
        ('Suspended', 'Suspended'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Dispatcher')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Verify')

    # Employee Record Fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    date_of_hire = models.DateField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.username:
            return self.username[:2].upper()
        return "??"

    def __str__(self):
        return self.get_full_name() or self.username
