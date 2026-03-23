from django.test import TestCase, Client
from django.urls import reverse
from .models import Vehicle, Driver
from users.models import CustomUser

class FleetModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            first_name="John",
            last_name="Doe",
            license_number="LICENSE123",
            license_expiry="2030-01-01",
            contact_number="1234567890"
        )
        self.vehicle = Vehicle.objects.create(
            plate_number="PLATE123",
            make="Toyota",
            model="Hiace",
            year=2022,
            driver=self.driver
        )

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), "PLATE123 - Toyota Hiace (2022)")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "John Doe")
